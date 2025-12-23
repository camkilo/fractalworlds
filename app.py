"""
Flask Web Server for Fractal Worlds RPG
========================================
Provides web API endpoints for the game, enabling deployment to Render and similar platforms.
"""

from flask import Flask, jsonify, request, send_from_directory
from game_integration import FractalRPG
from fractal_world import WorldConfig
import os
import uuid
import numpy as np

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Store active game sessions (in production, use Redis or similar)
game_sessions = {}

@app.route('/')
def home():
    """Serve the main HTML page"""
    try:
        with open('index.html', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    except FileNotFoundError:
        return jsonify({'error': 'index.html not found'}), 404

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Initialize a new game session"""
    data = request.json or {}
    player_name = data.get('player_name', 'Adventurer')
    seed = data.get('seed', 12345)
    
    config = WorldConfig(
        seed=seed,
        world_size=256,
        fractal_iterations=8,
        creature_density=0.15,
        magic_intensity=0.85
    )
    
    game = FractalRPG(config, player_name)
    game.initialize_game()
    
    session_id = f"game_{uuid.uuid4().hex[:8]}"
    game_sessions[session_id] = game
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': f'Game initialized for {player_name}'
    })

@app.route('/api/game/<session_id>/status', methods=['GET'])
def game_status(session_id):
    """Get current game status"""
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Game session not found'}), 404
    
    game = game_sessions[session_id]
    player = game.game_state.player
    
    # Get biome at player position
    x, y = int(player.position[0]), int(player.position[1])
    x = np.clip(x, 0, game.world.config.world_size - 1)
    y = np.clip(y, 0, game.world.config.world_size - 1)
    biome = game.world.biomes[y, x] if game.world_generated else 'unknown'
    
    return jsonify({
        'success': True,
        'player': {
            'name': player.name,
            'position': player.position.tolist(),
            'level': player.level,
            'experience': player.experience,
            'health': player.stats.health,
            'max_health': player.stats.max_health,
            'mana': player.stats.mana,
            'max_mana': player.stats.max_mana,
            'stamina': player.stats.stamina,
            'max_stamina': player.stats.max_stamina,
            'stats': {
                'strength': player.stats.strength,
                'intelligence': player.stats.intelligence,
                'agility': player.stats.agility,
                'logic_mastery': player.stats.logic_mastery
            },
            'inventory_count': len(player.inventory),
            'inventory': [
                {
                    'name': item.name,
                    'type': item.item_type,
                    'element': item.element.value if item.element else None,
                    'power': item.power,
                    'quantity': item.quantity
                }
                for item in player.inventory[:20]  # Limit to first 20 items
            ],
            'biome': biome
        }
    })

@app.route('/api/game/<session_id>/move', methods=['POST'])
def move_player(session_id):
    """Move player in a direction"""
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Game session not found'}), 404
    
    data = request.json or {}
    direction = data.get('direction', 'north')
    
    game = game_sessions[session_id]
    player = game.game_state.player
    
    # Direction vectors
    directions = {
        'north': np.array([0, -5, 0]),
        'south': np.array([0, 5, 0]),
        'east': np.array([5, 0, 0]),
        'west': np.array([-5, 0, 0])
    }
    
    if direction not in directions:
        return jsonify({'success': False, 'message': 'Invalid direction'})
    
    # Move player
    move_vec = directions[direction]
    success = player.move(move_vec, distance=5.0)
    
    if not success:
        return jsonify({'success': False, 'message': 'Not enough stamina'})
    
    # Clamp position to world bounds
    world_size = game.world.config.world_size
    player.position[0] = np.clip(player.position[0], 0, world_size - 1)
    player.position[1] = np.clip(player.position[1], 0, world_size - 1)
    
    # Update player position height based on terrain
    x, y = int(player.position[0]), int(player.position[1])
    x = np.clip(x, 0, world_size - 1)
    y = np.clip(y, 0, world_size - 1)
    terrain_height = game.world.terrain[y, x] * 100.0
    player.position[2] = terrain_height
    
    # Get biome
    biome = game.world.biomes[y, x]
    
    # Check for random encounter
    encounter = None
    if np.random.random() < 0.1:  # 10% chance
        nearby_creatures = [c for c in game.game_state.ecosystem.creatures 
                          if np.linalg.norm(np.array(c['position'][:2]) - player.position[:2]) < 20]
        if nearby_creatures:
            creature = nearby_creatures[0]
            encounter = {
                'enemy_name': creature['type'],
                'enemy_level': 1,
                'description': f'A wild {creature["type"]} appears!'
            }
    
    return jsonify({
        'success': True,
        'message': f'Moved {direction}',
        'player': {
            'name': player.name,
            'position': player.position.tolist(),
            'level': player.level,
            'experience': player.experience,
            'health': player.stats.health,
            'max_health': player.stats.max_health,
            'mana': player.stats.mana,
            'max_mana': player.stats.max_mana,
            'stamina': player.stats.stamina,
            'max_stamina': player.stats.max_stamina,
            'stats': {
                'strength': player.stats.strength,
                'intelligence': player.stats.intelligence,
                'agility': player.stats.agility,
                'logic_mastery': player.stats.logic_mastery
            },
            'inventory_count': len(player.inventory),
            'biome': biome
        },
        'encounter': encounter
    })

@app.route('/api/game/<session_id>/action', methods=['POST'])
def perform_action(session_id):
    """Perform a game action"""
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Game session not found'}), 404
    
    data = request.json or {}
    action = data.get('action', 'interact')
    
    game = game_sessions[session_id]
    player = game.game_state.player
    
    result = {'success': True, 'message': f'Performed {action}'}
    
    if action == 'attack':
        # Simple combat
        damage = player.stats.strength * 2
        result['message'] = f'You attack for {damage} damage!'
        result['combat_result'] = {
            'damage': damage,
            'player_victory': True,
            'message': 'Enemy defeated!'
        }
        player.gain_experience(50, player.skills['COMBAT'] if hasattr(player.skills, '__getitem__') else 1)
        
    elif action == 'gather':
        # Try to gather resources
        if player.stats.stamina >= 5:
            player.stats.stamina -= 5
            if np.random.random() < 0.7:
                result['message'] = 'You gathered some resources!'
                player.gain_experience(10, player.skills.get('EXPLORATION', 1))
            else:
                result['message'] = 'Nothing to gather here.'
        else:
            result['success'] = False
            result['message'] = 'Not enough stamina to gather.'
            
    elif action == 'flee':
        result['message'] = 'You fled from combat!'
        result['combat_result'] = {'player_victory': False, 'message': 'You escaped safely.'}
        
    elif action == 'spell':
        if player.stats.mana >= 10:
            player.stats.mana -= 10
            damage = player.stats.intelligence * 3
            result['message'] = f'You cast a spell for {damage} damage!'
            result['combat_result'] = {
                'damage': damage,
                'player_victory': True,
                'message': 'Enemy defeated by magic!'
            }
        else:
            result['success'] = False
            result['message'] = 'Not enough mana!'
    
    # Get updated player data
    x, y = int(player.position[0]), int(player.position[1])
    x = np.clip(x, 0, game.world.config.world_size - 1)
    y = np.clip(y, 0, game.world.config.world_size - 1)
    biome = game.world.biomes[y, x]
    
    result['player'] = {
        'name': player.name,
        'position': player.position.tolist(),
        'level': player.level,
        'experience': player.experience,
        'health': player.stats.health,
        'max_health': player.stats.max_health,
        'mana': player.stats.mana,
        'max_mana': player.stats.max_mana,
        'stamina': player.stats.stamina,
        'max_stamina': player.stats.max_stamina,
        'stats': {
            'strength': player.stats.strength,
            'intelligence': player.stats.intelligence,
            'agility': player.stats.agility,
            'logic_mastery': player.stats.logic_mastery
        },
        'inventory_count': len(player.inventory),
        'biome': biome
    }
    
    return jsonify(result)

@app.route('/api/game/<session_id>/save', methods=['POST'])
def save_game(session_id):
    """Save game state"""
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Game session not found'}), 404
    
    game = game_sessions[session_id]
    
    try:
        filename = f'saves/{session_id}.json'
        os.makedirs('saves', exist_ok=True)
        game.game_state.save_game(filename)
        return jsonify({'success': True, 'message': 'Game saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to save: {str(e)}'})

@app.route('/landing.html')
def landing():
    """Serve the landing page"""
    try:
        with open('landing.html', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    except FileNotFoundError:
        return jsonify({'error': 'landing.html not found'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'service': 'fractalworlds'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
