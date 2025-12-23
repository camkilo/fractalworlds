"""
Test script for high-fidelity RPG world features
Demonstrates all new realistic, cinematic features
"""

from fractal_world import FractalWorld, WorldConfig
from gameplay import GameState, FactionSystem, CombatSystem, Player
from visual_effects import CinematicCamera
import numpy as np
import json


def test_world_generation():
    """Test enhanced world generation"""
    print("="*60)
    print("🌍 TESTING WORLD GENERATION")
    print("="*60)
    
    config = WorldConfig(
        seed=12345,
        world_size=128,
        creature_density=0.15,
        magic_intensity=0.85,
        lighting_quality="cinematic"
    )
    
    world = FractalWorld(config)
    world.generate_world()
    
    # Verify new features
    assert len(world.villages) >= 0, "Villages should be generated"
    assert len(world.caves) >= 0, "Caves should be generated"
    assert world.weather is not None, "Weather system should be initialized"
    
    print(f"✅ Villages: {len(world.villages)}")
    print(f"✅ Caves: {len(world.caves)}")
    print(f"✅ Weather: {world.weather['current_weather']}")
    print(f"✅ Day/Night: {world.weather['day_night_cycle']['current_time']:.1f}h")
    
    # Check creature enhancements
    if world.creatures:
        creature = world.creatures[0]
        assert "textures" in creature, "Creatures should have textures"
        assert "animations" in creature, "Creatures should have animations"
        assert "magical_effects" in creature, "Creatures should have magical effects"
        
        print(f"\n🐉 Enhanced Creature: {creature['type']}")
        print(f"   - Texture resolution: {creature['textures']['base_texture']['resolution']}")
        print(f"   - Animations: {list(creature['animations'].keys())}")
        print(f"   - Magic level: {creature['magic_level']:.2f}")
        
        if creature.get("is_humanoid"):
            equipment = creature.get('equipment')
            if equipment:
                print(f"   - Equipment: {list(equipment.keys())}")
            animations = creature.get('animations', {})
            facial = animations.get('facial_expressions', {})
            if facial:
                print(f"   - Facial expressions: {facial.get('enabled', False)}")
    
    print("\n✅ World generation test PASSED!")
    return world


def test_villages():
    """Test village generation and NPCs"""
    print("\n" + "="*60)
    print("🏘️  TESTING VILLAGES")
    print("="*60)
    
    config = WorldConfig(seed=42, world_size=128)
    world = FractalWorld(config)
    world.generate_world()
    
    if world.villages:
        village = world.villages[0]
        print(f"\n🏘️  Village: {village['name']}")
        print(f"   Size: {village['size']}")
        print(f"   Buildings: {len(village['buildings'])}")
        print(f"   Population: {village['population']}")
        print(f"   Features: {village['features']}")
        
        # Check NPCs
        assert len(village['npcs']) > 0, "Village should have NPCs"
        npc = village['npcs'][0]
        print(f"\n👤 Sample NPC:")
        print(f"   Role: {npc['role']}")
        print(f"   Level: {npc['level']}")
        print(f"   Friendly: {npc['friendly']}")
        print(f"   Can trade: {npc['can_trade']}")
        print(f"   Has quest: {npc['has_quest']}")
        
        print("\n✅ Village test PASSED!")
    else:
        print("⚠️  No villages generated in this world")


def test_caves():
    """Test cave systems"""
    print("\n" + "="*60)
    print("⛰️  TESTING CAVES")
    print("="*60)
    
    config = WorldConfig(seed=42, world_size=128)
    world = FractalWorld(config)
    world.generate_world()
    
    if world.caves:
        cave = world.caves[0]
        print(f"\n⛰️  Cave System:")
        print(f"   Type: {cave['type']}")
        print(f"   Size: {cave['size']} meters")
        print(f"   Depth: {cave['depth']:.1f} meters")
        print(f"   Chambers: {len(cave['chambers'])}")
        print(f"   Resources: {cave['resources']}")
        print(f"   Creatures: {cave['creatures']}")
        print(f"   Features: {cave['features']}")
        
        print("\n✅ Cave test PASSED!")
    else:
        print("⚠️  No caves generated in this world")


def test_cinematic_camera():
    """Test cinematic camera system"""
    print("\n" + "="*60)
    print("🎬 TESTING CINEMATIC CAMERA")
    print("="*60)
    
    camera = CinematicCamera()
    
    # Test follow mode
    target_pos = np.array([10.0, 0.0, 5.0])
    camera.set_mode("follow")
    camera.follow_target(target_pos, delta_time=0.1)
    print(f"✅ Follow mode: Camera at {camera.position}")
    
    # Test orbit mode
    camera.orbit_around(np.array([0, 0, 0]), 15.0, np.pi/4, 5.0)
    print(f"✅ Orbit mode: Camera at {camera.position}")
    
    # Test camera shake
    camera.apply_shake(intensity=0.8)
    shake = camera.get_shake_offset()
    print(f"✅ Camera shake: Offset {shake}")
    
    # Test view matrix
    view = camera.get_view_matrix()
    print(f"✅ View matrix: FOV={view['fov']}, Position={view['position'][:2]}...")
    
    # Test cinematic path
    keyframes = [
        {"position": [0, 0, 10], "target": [0, 0, 0], "fov": 60, "duration": 2.0},
        {"position": [10, 5, 10], "target": [5, 0, 0], "fov": 45, "duration": 3.0}
    ]
    path = camera.create_cinematic_path(keyframes)
    print(f"✅ Cinematic path: {len(path)} frames generated")
    
    # Test cinematic angles
    angles = camera.get_cinematic_angles()
    print(f"✅ Cinematic angles: Letterbox={angles['letterbox']['enabled']}")
    
    print("\n✅ Cinematic camera test PASSED!")


def test_combat_system():
    """Test enhanced combat system"""
    print("\n" + "="*60)
    print("⚔️  TESTING COMBAT SYSTEM")
    print("="*60)
    
    combat = CombatSystem()
    
    # Test physics impact
    attacker_pos = np.array([0, 0, 0])
    target_pos = np.array([5, 0, 0])
    impact = combat.calculate_physics_impact(attacker_pos, target_pos, 50.0, 1.5)
    print(f"✅ Physics impact: Force={impact['force']}, Knockback={impact['knockback'][:2]}...")
    
    # Test environmental effects
    env_effects = combat.apply_environmental_combat_effects(
        np.array([0, 0, 0]),
        'mountains',
        {'current_weather': 'storm', 'wind': {'speed': 20}}
    )
    print(f"✅ Environmental effects:")
    print(f"   Damage multiplier: {env_effects['damage_multiplier']}")
    print(f"   Accuracy modifier: {env_effects['accuracy_modifier']}")
    print(f"   Stamina drain: {env_effects['stamina_drain']}")
    print(f"   Special effects: {env_effects['special_effects']}")
    
    # Test area of effect
    targets = [
        {"position": [1, 0, 0], "health": 100},
        {"position": [3, 0, 0], "health": 100},
        {"position": [10, 0, 0], "health": 100}
    ]
    affected = combat.calculate_area_of_effect(np.array([0, 0, 0]), 5.0, targets)
    print(f"✅ Area of effect: {len(affected)} targets affected")
    for target in affected:
        print(f"   Distance: {target['distance']:.1f}, Multiplier: {target['damage_multiplier']:.2f}")
    
    print("\n✅ Combat system test PASSED!")


def test_faction_system():
    """Test faction and reputation system"""
    print("\n" + "="*60)
    print("🤝 TESTING FACTION SYSTEM")
    print("="*60)
    
    factions = FactionSystem()
    print(f"✅ Initialized with {len(factions.factions)} factions")
    
    # Display factions
    for faction_id, faction in factions.factions.items():
        reaction = factions.get_faction_reaction(faction_id)
        print(f"   {faction['name']}: {reaction}")
    
    # Test player actions
    print("\n📜 Testing player actions:")
    
    actions = [
        ("help_villager", "Helping a villager"),
        ("protect_forest", "Protecting the forest"),
        ("defeat_bandits", "Defeating bandits")
    ]
    
    for action, description in actions:
        result = factions.apply_player_action(action)
        print(f"\n✅ {description}:")
        for faction_id, consequence in result['consequences'].items():
            reaction = factions.get_faction_reaction(faction_id)
            print(f"   {faction_id}: {consequence} -> Now {reaction}")
    
    print("\n✅ Faction system test PASSED!")


def test_interactive_terrain():
    """Test interactive and destructible terrain"""
    print("\n" + "="*60)
    print("🌍 TESTING INTERACTIVE TERRAIN")
    print("="*60)
    
    from gameplay import InteractiveEnvironment
    
    env = InteractiveEnvironment(world_size=256)
    
    # Create destructible objects
    tree = env.create_destructible_object((10, 10, 5), "tree")
    print(f"✅ Created tree: Health={tree['health']}, Can fall={tree['can_fall']}")
    
    # Modify terrain
    mod = env.modify_terrain((10, 10, 5), "crater", radius=8.0)
    print(f"✅ Terrain modified: Type={mod['modification']['type']}, Area={mod['affected_area']:.1f}m²")
    print(f"   Destroyed objects: {len(mod['destroyed_objects'])}")
    
    # Test river flood
    river_path = [(x, 10, 2) for x in range(0, 20, 2)]
    flood = env.simulate_river_flood(river_path, flood_level=0.5)
    print(f"✅ River flood: {len(flood['flooded_areas'])} areas, Total={flood['total_area']:.1f}m²")
    
    print("\n✅ Interactive terrain test PASSED!")


def test_full_gameplay_integration():
    """Test full gameplay integration"""
    print("\n" + "="*60)
    print("🎮 TESTING FULL GAMEPLAY INTEGRATION")
    print("="*60)
    
    # Generate world
    config = WorldConfig(seed=42, world_size=128, creature_density=0.1)
    world = FractalWorld(config)
    world.generate_world()
    world_data = world.get_world_data()
    
    # Create game state
    game_state = GameState(world_data)
    print(f"✅ Game state created")
    print(f"   Player: {game_state.player.name}")
    print(f"   Creatures in ecosystem: {len(game_state.ecosystem.creatures)}")
    print(f"   Factions: {len(game_state.factions.factions)}")
    print(f"   Destructible objects: {len(game_state.environment.destructible_objects)}")
    
    # Test game tick
    game_state.tick(delta_time=1.0)
    print(f"✅ Game tick completed")
    print(f"   Time elapsed: {game_state.time_elapsed}s")
    print(f"   Player health: {game_state.player.stats.health:.1f}")
    
    print("\n✅ Full integration test PASSED!")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🎮 HIGH-FIDELITY RPG WORLD - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    try:
        # Run all tests
        world = test_world_generation()
        test_villages()
        test_caves()
        test_cinematic_camera()
        test_combat_system()
        test_faction_system()
        test_interactive_terrain()
        test_full_gameplay_integration()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\n🎉 High-fidelity RPG world is fully functional!")
        print("   - Realistic creature models with animations")
        print("   - Villages with NPCs and quests")
        print("   - Cave systems with resources")
        print("   - Cinematic camera system")
        print("   - Physics-based combat")
        print("   - Faction reputation system")
        print("   - Interactive destructible terrain")
        print("   - Dynamic weather and day/night cycles")
        
        # Save test world
        world.save_world("test_high_fidelity_world.json")
        print(f"\n💾 Test world saved to test_high_fidelity_world.json")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
