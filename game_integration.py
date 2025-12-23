"""
Fractal Fantasy World - Game Integration
=========================================
Integrates gameplay systems with world generation to create a fully
playable RPG experience.
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from fractal_world import FractalWorld, WorldConfig
from gameplay import (
    Player, GameState, CraftingSystem, SpellSystem, CombatSystem,
    EcosystemSimulator, PuzzleSystem, InteractiveEnvironment,
    ElementType, Item
)
from visual_effects import MagicalEffects, LightingSystem


class FractalRPG:
    """Main RPG game integrating world generation with gameplay"""
    
    def __init__(self, config: WorldConfig = None, player_name: str = "Adventurer"):
        self.world = FractalWorld(config)
        self.game_state = None
        self.player_name = player_name
        self.world_generated = False
        
    def initialize_game(self):
        """Initialize the game world and systems"""
        print("\n" + "="*60)
        print("🎮 FRACTAL WORLDS RPG - INITIALIZATION")
        print("="*60)
        
        # Generate world
        print("\n🌍 Generating procedural world...")
        self.world.generate_world()
        self.world_generated = True
        
        # Create game state
        world_data = self._get_world_data()
        self.game_state = GameState(world_data)
        
        # Setup player
        self.game_state.player = Player(self.player_name, self._get_spawn_position())
        
        # Populate environment with resources
        self._populate_resources()
        
        # Give player starter items
        self._give_starter_kit()
        
        # Teach basic spells
        self._teach_starter_spells()
        
        print("\n✅ Game initialized successfully!")
        self._print_game_intro()
        
    def _get_world_data(self) -> Dict[str, Any]:
        """Extract world data for game state"""
        return self.world.get_world_data()
    
    def _get_spawn_position(self) -> Tuple[float, float, float]:
        """Find a suitable spawn position for the player"""
        # Start in a plains or forest biome if possible
        size = self.world.config.world_size
        
        for _ in range(100):  # Try 100 random positions
            x = np.random.randint(0, size)
            y = np.random.randint(0, size)
            
            biome = self.world.biomes[x, y]
            elevation = self.world.terrain[x, y]
            
            # Suitable spawn: not water, reasonable elevation
            if biome != "water" and 0.3 < elevation < 0.7:
                # Convert to world coordinates with height
                z = elevation * 100.0  # Scale elevation
                return (float(x), float(y), z)
        
        # Fallback to center
        center = size // 2
        return (float(center), float(center), 50.0)
    
    def _populate_resources(self):
        """Populate world with resource nodes"""
        print("  ⛏️  Populating resource nodes...")
        
        # Create resource nodes in forests
        for forest in self.world.forests:
            center = forest["center"]
            # Get elevation at forest center
            cx, cy = int(center[0]), int(center[1])
            cx = np.clip(cx, 0, self.world.config.world_size - 1)
            cy = np.clip(cy, 0, self.world.config.world_size - 1)
            elevation = self.world.terrain[cy, cx] * 100.0  # Scale to world height
            
            # Create multiple resource nodes per forest
            for _ in range(np.random.randint(2, 5)):
                offset_x = np.random.uniform(-10, 10)
                offset_y = np.random.uniform(-10, 10)
                position = (center[0] + offset_x, center[1] + offset_y, elevation)
                
                # Random element type
                element = np.random.choice([
                    ElementType.NATURE,
                    ElementType.EARTH,
                    ElementType.WATER
                ])
                
                self.game_state.environment.create_resource_node(
                    position, "Wood" if element == ElementType.NATURE else "Crystal", element
                )
        
        # Create resource nodes near structures
        for structure in self.world.structures:
            position = structure["position"]
            
            # Magical structures have magical resources
            if "magic" in structure["type"].lower() or "crystal" in structure["type"].lower():
                for _ in range(np.random.randint(3, 6)):
                    offset_x = np.random.uniform(-15, 15)
                    offset_y = np.random.uniform(-15, 15)
                    node_pos = (position[0] + offset_x, position[1] + offset_y, position[2])
                    
                    element = np.random.choice([
                        ElementType.ARCANE,
                        ElementType.LIGHT,
                        ElementType.DARK
                    ])
                    
                    self.game_state.environment.create_resource_node(
                        node_pos, "Arcane Crystal", element
                    )
        
        print(f"  ✓ Created {len(self.game_state.environment.resource_nodes)} resource nodes")
    
    def _give_starter_kit(self):
        """Give player starting items"""
        starter_items = [
            Item("Basic Sword", "weapon", None, 10.0, {"damage": 10}),
            Item("Cloth Armor", "armor", None, 5.0, {"defense": 5}),
            Item("Health Potion", "consumable", None, 1.0, {"heal": 50}, quantity=3),
            Item("Mana Potion", "consumable", None, 1.0, {"mana": 50}, quantity=3)
        ]
        
        for item in starter_items:
            self.game_state.player.add_to_inventory(item)
        
        # Equip weapon and armor
        self.game_state.player.equipped["weapon"] = starter_items[0]
        self.game_state.player.equipped["armor"] = starter_items[1]
    
    def _teach_starter_spells(self):
        """Teach player basic starting spells"""
        starter_spells = ["Fireball", "Ice Shard", "Healing Light"]
        
        for spell_name in starter_spells:
            success, msg = self.game_state.spells.learn_spell(
                self.game_state.player, spell_name
            )
            if success:
                print(f"  📖 Learned spell: {spell_name}")
    
    def _print_game_intro(self):
        """Print game introduction"""
        print("\n" + "="*60)
        print("🌟 WELCOME TO FRACTAL WORLDS 🌟")
        print("="*60)
        print(f"\n👤 Player: {self.game_state.player.name}")
        print(f"📍 Spawn Position: ({self.game_state.player.position[0]:.1f}, "
              f"{self.game_state.player.position[1]:.1f}, {self.game_state.player.position[2]:.1f})")
        print(f"\n❤️  Health: {self.game_state.player.stats.health}/{self.game_state.player.stats.max_health}")
        print(f"🔮 Mana: {self.game_state.player.stats.mana}/{self.game_state.player.stats.max_mana}")
        print(f"⚡ Stamina: {self.game_state.player.stats.stamina}/{self.game_state.player.stats.max_stamina}")
        print(f"\n🎒 Inventory: {len(self.game_state.player.inventory)} items")
        print(f"📚 Known Spells: {len(self.game_state.player.known_spells)}")
        print(f"🌍 World Size: {self.world.config.world_size}x{self.world.config.world_size}")
        print(f"🐉 Creatures: {len(self.world.creatures)}")
        print(f"🏰 Structures: {len(self.world.structures)}")
        print(f"🌲 Forests: {len(self.world.forests)}")
        print(f"⛏️  Resources: {len(self.game_state.environment.resource_nodes)}")
        print("\n" + "="*60)
    
    def play_turn(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a player action (turn-based gameplay)"""
        if not self.world_generated or not self.game_state:
            return {"success": False, "message": "Game not initialized"}
        
        result = {"success": False, "message": "Unknown action"}
        
        # Process action
        if action == "move":
            direction = kwargs.get("direction", (1, 0, 0))
            distance = kwargs.get("distance", 1.0)
            direction_array = np.array(direction)
            
            if self.game_state.player.move(direction_array, distance):
                result = {
                    "success": True,
                    "message": f"Moved to {tuple(self.game_state.player.position)}",
                    "new_position": tuple(self.game_state.player.position)
                }
            else:
                result = {"success": False, "message": "Not enough stamina"}
        
        elif action == "gather":
            # Find nearby resources
            nearby = self.game_state.environment.get_nearby_resources(
                tuple(self.game_state.player.position), radius=5.0
            )
            
            if nearby:
                node = nearby[0]
                item = self.game_state.player.gather_resource(node)
                if item:
                    self.game_state.environment.harvest_resource(node)
                    result = {
                        "success": True,
                        "message": f"Gathered {item.name}",
                        "item": item.name,
                        "element": item.element.value if item.element else None
                    }
                else:
                    result = {"success": False, "message": "Gathering failed (low stamina or bad luck)"}
            else:
                result = {"success": False, "message": "No resources nearby"}
        
        elif action == "craft":
            recipe_name = kwargs.get("recipe", "")
            success, message, item = self.game_state.crafting.craft_item(
                self.game_state.player, recipe_name
            )
            result = {
                "success": success,
                "message": message,
                "item": item.name if item else None
            }
        
        elif action == "cast_spell":
            spell_name = kwargs.get("spell", "")
            target_pos = kwargs.get("target", (0, 0, 0))
            
            # Find spell
            spell = None
            for s in self.game_state.player.known_spells:
                if s.name == spell_name:
                    spell = s
                    break
            
            if spell:
                spell_result = self.game_state.player.cast_spell(spell, target_pos)
                result = {
                    "success": spell_result.get("success", False),
                    "message": f"Cast {spell_name}",
                    "power": spell_result.get("power", 0),
                    "visuals": spell_result.get("visual_effects", {})
                }
            else:
                result = {"success": False, "message": f"Spell {spell_name} not known"}
        
        elif action == "attack":
            # Find nearest creature
            nearest_creature = self._find_nearest_creature()
            if nearest_creature:
                attack_result = self.game_state.combat.calculate_attack(
                    self.game_state.player, nearest_creature
                )
                result = {
                    "success": True,
                    "message": f"Attacked {nearest_creature.get('type', 'creature')}",
                    "hit": attack_result["hit"],
                    "damage": attack_result["damage"],
                    "critical": attack_result.get("critical", False)
                }
            else:
                result = {"success": False, "message": "No enemies nearby"}
        
        elif action == "rest":
            # Fast regeneration
            self.game_state.player.stats.regenerate(10.0)
            result = {
                "success": True,
                "message": "Rested and recovered",
                "health": self.game_state.player.stats.health,
                "mana": self.game_state.player.stats.mana,
                "stamina": self.game_state.player.stats.stamina
            }
        
        elif action == "solve_puzzle":
            puzzle_name = kwargs.get("puzzle", "")
            answer = kwargs.get("answer", None)
            success, message, rewards = self.game_state.puzzles.attempt_puzzle(
                self.game_state.player, puzzle_name, answer
            )
            result = {
                "success": success,
                "message": message,
                "rewards": rewards
            }
        
        elif action == "status":
            result = self._get_player_status()
        
        # Tick the game world
        self.game_state.tick(1.0)
        
        return result
    
    def _find_nearest_creature(self) -> Optional[Dict[str, Any]]:
        """Find nearest creature to player"""
        if not self.game_state.ecosystem.creatures:
            return None
        
        player_pos = self.game_state.player.position
        nearest = None
        min_distance = float('inf')
        
        for creature in self.game_state.ecosystem.creatures:
            creature_pos = np.array(creature["position"])
            distance = np.linalg.norm(player_pos - creature_pos)
            
            if distance < min_distance and distance < 20.0:  # Within 20 units
                min_distance = distance
                nearest = creature
        
        return nearest
    
    def _get_player_status(self) -> Dict[str, Any]:
        """Get current player status"""
        player = self.game_state.player
        
        return {
            "success": True,
            "name": player.name,
            "level": player.level,
            "experience": player.experience,
            "position": tuple(player.position),
            "stats": {
                "health": f"{player.stats.health:.1f}/{player.stats.max_health:.1f}",
                "mana": f"{player.stats.mana:.1f}/{player.stats.max_mana:.1f}",
                "stamina": f"{player.stats.stamina:.1f}/{player.stats.max_stamina:.1f}",
                "strength": player.stats.strength,
                "intelligence": player.stats.intelligence,
                "agility": player.stats.agility,
                "logic_mastery": player.stats.logic_mastery
            },
            "skills": {k.value: f"{v:.2f}" for k, v in player.skills.items()},
            "inventory_count": len(player.inventory),
            "known_spells": [s.name for s in player.known_spells],
            "equipped": {
                k: v.name if v else "None" 
                for k, v in player.equipped.items()
            }
        }
    
    def get_nearby_entities(self, radius: float = 50.0) -> Dict[str, List[Dict[str, Any]]]:
        """Get entities near the player"""
        player_pos = self.game_state.player.position
        
        nearby = {
            "creatures": [],
            "structures": [],
            "resources": [],
            "forests": []
        }
        
        # Creatures
        for creature in self.game_state.ecosystem.creatures:
            creature_pos = np.array(creature["position"])
            distance = np.linalg.norm(player_pos - creature_pos)
            if distance <= radius:
                nearby["creatures"].append({
                    "type": creature.get("type"),
                    "position": creature["position"],
                    "distance": float(distance)
                })
        
        # Structures
        for structure in self.world.structures:
            structure_pos = np.array(structure["position"])
            distance = np.linalg.norm(player_pos - structure_pos)
            if distance <= radius:
                nearby["structures"].append({
                    "type": structure.get("type"),
                    "position": structure["position"],
                    "distance": float(distance)
                })
        
        # Resources
        for node in self.game_state.environment.resource_nodes:
            node_pos = np.array(node["position"])
            distance = np.linalg.norm(player_pos - node_pos)
            if distance <= radius:
                nearby["resources"].append({
                    "type": node.get("type"),
                    "element": node.get("element"),
                    "quantity": node.get("quantity"),
                    "position": node["position"],
                    "distance": float(distance)
                })
        
        # Forests
        for forest in self.world.forests:
            forest_pos = np.array(forest["center"][:2])
            player_pos_2d = player_pos[:2]
            distance = np.linalg.norm(player_pos_2d - forest_pos)
            if distance <= radius:
                nearby["forests"].append({
                    "tree_count": len(forest.get("trees", [])),
                    "position": forest["center"],
                    "distance": float(distance)
                })
        
        return nearby
    
    def print_status(self):
        """Print current game status"""
        status = self._get_player_status()
        
        print("\n" + "="*60)
        print(f"👤 {status['name']} - Level {status['level']}")
        print("="*60)
        print(f"\n📍 Position: ({status['position'][0]:.1f}, {status['position'][1]:.1f}, {status['position'][2]:.1f})")
        print(f"\n💪 Stats:")
        print(f"  ❤️  Health: {status['stats']['health']}")
        print(f"  🔮 Mana: {status['stats']['mana']}")
        print(f"  ⚡ Stamina: {status['stats']['stamina']}")
        print(f"  💪 Strength: {status['stats']['strength']}")
        print(f"  🧠 Intelligence: {status['stats']['intelligence']}")
        print(f"  🏃 Agility: {status['stats']['agility']}")
        print(f"  🧩 Logic Mastery: {status['stats']['logic_mastery']:.2f}")
        
        print(f"\n🎯 Skills:")
        for skill, value in status['skills'].items():
            print(f"  • {skill.title()}: {value}")
        
        print(f"\n🎒 Inventory: {status['inventory_count']} items")
        print(f"⚔️  Equipped Weapon: {status['equipped']['weapon']}")
        print(f"🛡️  Equipped Armor: {status['equipped']['armor']}")
        
        print(f"\n📚 Known Spells ({len(status['known_spells'])}):")
        for spell in status['known_spells']:
            print(f"  • {spell}")
        
        print("\n" + "="*60)
    
    def print_nearby(self, radius: float = 30.0):
        """Print nearby entities"""
        nearby = self.get_nearby_entities(radius)
        
        print(f"\n🔍 Entities within {radius} units:")
        print("="*60)
        
        if nearby["creatures"]:
            print(f"\n🐉 Creatures ({len(nearby['creatures'])}):")
            for creature in sorted(nearby["creatures"], key=lambda x: x["distance"])[:5]:
                print(f"  • {creature['type']} - {creature['distance']:.1f} units away")
        
        if nearby["structures"]:
            print(f"\n🏰 Structures ({len(nearby['structures'])}):")
            for structure in sorted(nearby["structures"], key=lambda x: x["distance"])[:5]:
                print(f"  • {structure['type']} - {structure['distance']:.1f} units away")
        
        if nearby["resources"]:
            print(f"\n⛏️  Resources ({len(nearby['resources'])}):")
            for resource in sorted(nearby["resources"], key=lambda x: x["distance"])[:5]:
                print(f"  • {resource['type']} ({resource['element']}) x{resource['quantity']} - {resource['distance']:.1f} units away")
        
        if nearby["forests"]:
            print(f"\n🌲 Forests ({len(nearby['forests'])}):")
            for forest in sorted(nearby["forests"], key=lambda x: x["distance"])[:3]:
                print(f"  • Forest with {forest['tree_count']} trees - {forest['distance']:.1f} units away")
        
        if not any(nearby.values()):
            print("  Nothing nearby. Try exploring!")
        
        print("\n" + "="*60)
    
    def save_game(self, filename: str = "fractal_rpg_save.json"):
        """Save the game state"""
        self.game_state.save_game(filename)
        print(f"\n💾 Game saved to {filename}")
    
    def demo_gameplay(self):
        """Run a demo of gameplay mechanics"""
        print("\n" + "="*60)
        print("🎮 FRACTAL WORLDS RPG - GAMEPLAY DEMO")
        print("="*60)
        
        # Show initial status
        self.print_status()
        self.print_nearby()
        
        # Demo: Movement
        print("\n📍 Action: Moving forward...")
        result = self.play_turn("move", direction=(10, 0, 0), distance=10.0)
        print(f"  Result: {result['message']}")
        
        # Demo: Gathering
        print("\n⛏️  Action: Gathering resources...")
        result = self.play_turn("gather")
        print(f"  Result: {result['message']}")
        if result['success']:
            print(f"  Gathered: {result.get('item', 'Unknown')} ({result.get('element', 'None')})")
        
        # Demo: Spell casting
        print("\n🔮 Action: Casting Fireball spell...")
        target = (self.game_state.player.position[0] + 20, 
                 self.game_state.player.position[1], 
                 self.game_state.player.position[2])
        result = self.play_turn("cast_spell", spell="Fireball", target=target)
        print(f"  Result: {result['message']}")
        if result['success']:
            print(f"  Power: {result['power']:.1f}")
        
        # Demo: Rest
        print("\n😴 Action: Resting...")
        result = self.play_turn("rest")
        print(f"  Result: {result['message']}")
        print(f"  Health: {result['health']:.1f}, Mana: {result['mana']:.1f}, Stamina: {result['stamina']:.1f}")
        
        # Demo: Status check
        print("\n📊 Final Status:")
        self.print_status()
        
        print("\n" + "="*60)
        print("✨ Demo complete! Game is fully playable.")
        print("="*60)


def main():
    """Main function to demonstrate the full RPG system"""
    # Create RPG with custom configuration
    config = WorldConfig(
        seed=42,
        world_size=256,
        fractal_iterations=8,
        terrain_roughness=0.6,
        water_level=0.3,
        tree_density=0.5,
        creature_density=0.15,
        magic_intensity=0.8,
        lighting_quality="cinematic",
        enable_animations=True
    )
    
    # Initialize game
    game = FractalRPG(config, player_name="Hero")
    game.initialize_game()
    
    # Run gameplay demo
    game.demo_gameplay()
    
    # Save game
    game.save_game("fractal_rpg_demo.json")
    
    print("\n✅ Full RPG system is operational!")
    print("🎮 Ready for immersive gameplay!")


if __name__ == "__main__":
    main()
