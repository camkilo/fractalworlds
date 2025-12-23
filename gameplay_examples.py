"""
Fractal Worlds RPG - Interactive Gameplay Examples
===================================================
Demonstrates all gameplay features with interactive examples
"""

from game_integration import FractalRPG
from fractal_world import WorldConfig
import json


def example_exploration():
    """Example: Exploring the procedural world"""
    print("\n" + "="*70)
    print("EXAMPLE 1: EXPLORATION & RESOURCE GATHERING")
    print("="*70)
    
    config = WorldConfig(seed=12345, world_size=256, creature_density=0.1)
    game = FractalRPG(config, "Explorer")
    game.initialize_game()
    
    # Explore the area
    print("\n📍 Exploring the world...")
    game.print_nearby(radius=50.0)
    
    # Move around
    print("\n🚶 Moving north...")
    result = game.play_turn("move", direction=(0, 10, 0), distance=15.0)
    print(f"  {result['message']}")
    
    print("\n🚶 Moving east...")
    result = game.play_turn("move", direction=(10, 0, 0), distance=15.0)
    print(f"  {result['message']}")
    
    # Check surroundings again
    game.print_nearby(radius=50.0)
    
    # Try gathering resources
    print("\n⛏️  Attempting to gather resources...")
    for i in range(5):
        result = game.play_turn("gather")
        if result['success']:
            print(f"  ✓ {result['message']} - {result.get('item', 'Unknown')}")
        else:
            print(f"  ✗ {result['message']}")
        
        # Move a bit
        game.play_turn("move", direction=(2, 2, 0), distance=3.0)
    
    game.print_status()
    print("\n✨ Exploration complete!")


def example_crafting():
    """Example: Logic-based crafting system"""
    print("\n" + "="*70)
    print("EXAMPLE 2: CRAFTING SYSTEM")
    print("="*70)
    
    config = WorldConfig(seed=99, world_size=128)
    game = FractalRPG(config, "Crafter")
    game.initialize_game()
    
    # Give player materials
    from gameplay import Item, ElementType
    print("\n📦 Adding crafting materials to inventory...")
    materials = [
        Item("Fire Essence", "resource", ElementType.FIRE, quantity=5),
        Item("Earth Crystal", "resource", ElementType.EARTH, quantity=5),
        Item("Water Gem", "resource", ElementType.WATER, quantity=5),
        Item("Arcane Dust", "resource", ElementType.ARCANE, quantity=5),
        Item("Nature Seed", "resource", ElementType.NATURE, quantity=5),
        Item("Air Wisp", "resource", ElementType.AIR, quantity=5),
        Item("Light Shard", "resource", ElementType.LIGHT, quantity=3),
        Item("Dark Essence", "resource", ElementType.DARK, quantity=3)
    ]
    
    for item in materials:
        game.game_state.player.add_to_inventory(item)
    
    print(f"  Added {len(materials)} types of materials")
    
    # Try crafting different items
    print("\n🔨 Attempting to craft items...")
    recipes = ["Fire Sword", "Ice Staff", "Nature Bow", "Crystal Armor", "Arcane Rune"]
    
    for recipe in recipes:
        result = game.play_turn("craft", recipe=recipe)
        if result['success']:
            print(f"  ✓ {result['message']}")
        else:
            print(f"  ✗ {result['message']}")
    
    game.print_status()
    print("\n✨ Crafting demo complete!")


def example_magic():
    """Example: Pattern-based spell casting"""
    print("\n" + "="*70)
    print("EXAMPLE 3: SPELL CASTING SYSTEM")
    print("="*70)
    
    config = WorldConfig(seed=777, world_size=256, magic_intensity=0.9)
    game = FractalRPG(config, "Mage")
    game.initialize_game()
    
    # Learn all available spells
    print("\n📚 Learning advanced spells...")
    spell_names = [
        "Lightning Chain", "Shadow Step", "Fractal Storm",
        "Earth Wall", "Nature's Wrath"
    ]
    
    for spell_name in spell_names:
        # Boost magic skill to learn advanced spells
        game.game_state.player.skills[game.game_state.player.skills.__class__.__dict__['__annotations__'].keys().__iter__().__next__()] = 6.0
        from gameplay import SkillType
        game.game_state.player.skills[SkillType.MAGIC] = 6.0
        
        success, msg = game.game_state.spells.learn_spell(
            game.game_state.player, spell_name
        )
        if success:
            print(f"  ✓ {msg}")
    
    # Cast different spells
    print("\n🔮 Casting spells with different patterns...")
    player_pos = game.game_state.player.position
    
    spells_to_cast = ["Fireball", "Ice Shard", "Lightning Chain", "Healing Light"]
    
    for i, spell_name in enumerate(spells_to_cast):
        # Cast at different positions
        target = (player_pos[0] + i*10, player_pos[1] + i*5, player_pos[2])
        result = game.play_turn("cast_spell", spell=spell_name, target=target)
        
        if result['success']:
            print(f"\n  ✓ {result['message']}")
            print(f"    Power: {result['power']:.1f}")
            visuals = result.get('visuals', {})
            print(f"    Particles: {visuals.get('particle_count', 0)}")
            print(f"    Pattern: {visuals.get('pattern', 'unknown')}")
        
        # Rest to recover mana
        game.play_turn("rest")
    
    game.print_status()
    print("\n✨ Magic demo complete!")


def example_combat():
    """Example: Emergent combat system"""
    print("\n" + "="*70)
    print("EXAMPLE 4: COMBAT SYSTEM")
    print("="*70)
    
    config = WorldConfig(seed=444, world_size=256, creature_density=0.3)
    game = FractalRPG(config, "Warrior")
    game.initialize_game()
    
    # Equip better weapon
    from gameplay import Item, ElementType
    weapon = Item("Dragon Blade", "weapon", ElementType.FIRE, 50.0, {"damage": 50})
    game.game_state.player.equipped["weapon"] = weapon
    game.game_state.player.add_to_inventory(weapon)
    
    # Boost combat stats
    game.game_state.player.stats.strength = 30.0
    game.game_state.player.stats.agility = 25.0
    
    print("\n⚔️  Preparing for combat...")
    print(f"  Weapon: {weapon.name} (Power: {weapon.power})")
    print(f"  Strength: {game.game_state.player.stats.strength}")
    print(f"  Agility: {game.game_state.player.stats.agility}")
    
    # Find creatures
    game.print_nearby(radius=100.0)
    
    # Simulate combat
    print("\n⚔️  Engaging in combat...")
    for i in range(5):
        result = game.play_turn("attack")
        
        if result['success']:
            print(f"\n  Round {i+1}:")
            print(f"    Hit: {result['hit']}")
            if result['hit']:
                print(f"    Damage: {result['damage']:.1f}")
                print(f"    Critical: {result.get('critical', False)}")
        else:
            print(f"\n  Round {i+1}: {result['message']}")
            break
        
        # Rest briefly
        game.play_turn("rest")
    
    game.print_status()
    print("\n✨ Combat demo complete!")


def example_ecosystem():
    """Example: Dynamic ecosystem simulation"""
    print("\n" + "="*70)
    print("EXAMPLE 5: ECOSYSTEM SIMULATION")
    print("="*70)
    
    config = WorldConfig(seed=555, world_size=256, creature_density=0.25)
    game = FractalRPG(config, "Observer")
    game.initialize_game()
    
    print("\n🌍 Observing ecosystem dynamics...")
    
    # Initial state
    initial_creatures = len(game.game_state.ecosystem.creatures)
    print(f"\n📊 Initial creature count: {initial_creatures}")
    
    # Simulate time passing
    print("\n⏰ Simulating 10 time steps...")
    for t in range(10):
        game.game_state.tick(delta_time=1.0)
        
        current_count = len(game.game_state.ecosystem.creatures)
        print(f"  Step {t+1}: {current_count} creatures")
        
        # Check creature behaviors
        if t % 3 == 0:
            creature = game.game_state.ecosystem.creatures[0] if game.game_state.ecosystem.creatures else None
            if creature:
                ai = game.game_state.ecosystem.ai_controllers.get(creature["id"])
                if ai:
                    print(f"    Sample creature behavior: {ai.behavior_state}")
    
    print(f"\n📊 Final creature count: {len(game.game_state.ecosystem.creatures)}")
    
    # Show population history
    if game.game_state.ecosystem.population_history:
        print("\n📈 Population trends:")
        history = game.game_state.ecosystem.population_history[-5:]
        for i, pop in enumerate(history):
            print(f"  Step {len(game.game_state.ecosystem.population_history)-5+i}: {pop}")
    
    print("\n✨ Ecosystem simulation complete!")


def example_puzzles():
    """Example: Algorithmic puzzle solving"""
    print("\n" + "="*70)
    print("EXAMPLE 6: PUZZLE SYSTEM")
    print("="*70)
    
    config = WorldConfig(seed=888, world_size=128)
    game = FractalRPG(config, "Scholar")
    game.initialize_game()
    
    # Get available puzzles
    puzzles = game.game_state.puzzles.puzzles
    
    print(f"\n🧩 Found {len(puzzles)} puzzles to solve")
    
    # Try solving puzzles
    test_solutions = {
        "Fibonacci Lock": [21, 34, 55],
        "Prime Gate": [29],
        "Logic Circuit": [False],
        "Element Balance": ["A"]
    }
    
    for puzzle_name, answer in test_solutions.items():
        puzzle = next((p for p in puzzles if p["name"] == puzzle_name), None)
        if puzzle:
            print(f"\n🧩 Puzzle: {puzzle_name}")
            print(f"   Description: {puzzle['description']}")
            print(f"   Attempting solution: {answer}")
            
            result = game.play_turn("solve_puzzle", puzzle=puzzle_name, answer=answer)
            
            if result['success']:
                print(f"   ✓ {result['message']}")
                print(f"   Rewards: {result.get('rewards', {})}")
            else:
                print(f"   ✗ {result['message']}")
    
    game.print_status()
    print("\n✨ Puzzle solving complete!")


def example_full_adventure():
    """Example: Complete adventure showcase"""
    print("\n" + "="*70)
    print("EXAMPLE 7: FULL ADVENTURE")
    print("="*70)
    
    config = WorldConfig(
        seed=12345,
        world_size=256,
        fractal_iterations=8,
        terrain_roughness=0.7,
        creature_density=0.15,
        magic_intensity=0.85
    )
    
    game = FractalRPG(config, "Adventurer")
    game.initialize_game()
    
    print("\n🎮 Starting adventure...")
    
    # Phase 1: Exploration
    print("\n--- Phase 1: Exploration ---")
    for _ in range(3):
        game.play_turn("move", direction=(5, 5, 0), distance=10.0)
    game.print_nearby(radius=40.0)
    
    # Phase 2: Gathering
    print("\n--- Phase 2: Resource Gathering ---")
    gathered = 0
    for _ in range(5):
        result = game.play_turn("gather")
        if result['success']:
            gathered += 1
        game.play_turn("move", direction=(3, 0, 0), distance=5.0)
    print(f"  Gathered {gathered} resources")
    
    # Phase 3: Magic
    print("\n--- Phase 3: Spell Casting ---")
    pos = game.game_state.player.position
    game.play_turn("cast_spell", spell="Fireball", target=(pos[0]+20, pos[1], pos[2]))
    game.play_turn("rest")
    
    # Phase 4: Combat
    print("\n--- Phase 4: Combat ---")
    game.play_turn("attack")
    
    # Phase 5: Status
    print("\n--- Phase 5: Final Status ---")
    game.print_status()
    
    # Save the adventure
    game.save_game("full_adventure_save.json")
    
    print("\n✨ Full adventure complete!")


def interactive_menu():
    """Interactive menu for running examples"""
    print("\n" + "="*70)
    print("FRACTAL WORLDS RPG - INTERACTIVE EXAMPLES")
    print("="*70)
    print("\nChoose an example to run:")
    print("  1. Exploration & Resource Gathering")
    print("  2. Crafting System")
    print("  3. Spell Casting")
    print("  4. Combat System")
    print("  5. Ecosystem Simulation")
    print("  6. Puzzle Solving")
    print("  7. Full Adventure")
    print("  8. Run All Examples")
    print("  0. Exit")
    
    try:
        choice = input("\nEnter choice (0-8): ").strip()
        
        if choice == "1":
            example_exploration()
        elif choice == "2":
            example_crafting()
        elif choice == "3":
            example_magic()
        elif choice == "4":
            example_combat()
        elif choice == "5":
            example_ecosystem()
        elif choice == "6":
            example_puzzles()
        elif choice == "7":
            example_full_adventure()
        elif choice == "8":
            print("\n🎮 Running all examples...\n")
            example_exploration()
            example_crafting()
            example_magic()
            example_combat()
            example_ecosystem()
            example_puzzles()
            example_full_adventure()
            print("\n✅ All examples completed!")
        elif choice == "0":
            print("\nGoodbye! Thanks for playing Fractal Worlds RPG!")
            return
        else:
            print("\nInvalid choice. Please try again.")
            interactive_menu()
    except KeyboardInterrupt:
        print("\n\nExiting. Thanks for playing Fractal Worlds RPG!")
        return
    except EOFError:
        print("\n\nNo input detected. Running all examples in non-interactive mode...")
        example_exploration()
        example_crafting()
        example_magic()
        example_combat()
        example_ecosystem()
        example_puzzles()
        example_full_adventure()
        print("\n✅ All examples completed!")
        return


if __name__ == "__main__":
    interactive_menu()
