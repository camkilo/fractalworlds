"""
Flask Web Server for Fractal Worlds RPG
========================================
Provides web API endpoints for the game, enabling deployment to Render and similar platforms.
"""

from flask import Flask, jsonify, request
from game_integration import FractalRPG
from fractal_world import WorldConfig
import os
import uuid

app = Flask(__name__, static_folder='.')

# Store active game sessions (in production, use Redis or similar)
game_sessions = {}

@app.route('/')
def home():
    """Serve the main HTML page"""
    try:
        with open('index.html', 'r') as f:
            return f.read()
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
            'inventory_count': len(player.inventory)
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'service': 'fractalworlds'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
