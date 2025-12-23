#!/usr/bin/env python3
"""
Example script demonstrating the Fractal Fantasy World generation
"""

from fractal_world import FractalWorld, WorldConfig, BiomeType
from visual_effects import (
    MagicalEffects, LightingSystem, AnimationSystem, 
    TextureSystem, create_post_processing_stack
)
import json


def example_basic_world():
    """Generate a basic fantasy world"""
    print("\n" + "="*70)
    print("Example 1: Basic Fantasy World Generation")
    print("="*70)
    
    config = WorldConfig(
        seed=12345,
        world_size=128,
        fractal_iterations=6,
        terrain_roughness=0.5,
        tree_density=0.4,
        creature_density=0.1,
        magic_intensity=0.6
    )
    
    world = FractalWorld(config)
    world.generate_world()
    world.print_world_summary()
    world.save_world("example_basic_world.json")


def example_high_magic_world():
    """Generate a world with high magic intensity"""
    print("\n" + "="*70)
    print("Example 2: High Magic Fantasy World")
    print("="*70)
    
    config = WorldConfig(
        seed=99999,
        world_size=256,
        fractal_iterations=8,
        terrain_roughness=0.7,
        tree_density=0.6,
        creature_density=0.2,
        magic_intensity=1.0,  # Maximum magic
        lighting_quality="cinematic"
    )
    
    world = FractalWorld(config)
    world.generate_world()
    world.print_world_summary()
    
    # Add extra magical effects
    print("\n🌟 Adding Enhanced Magical Effects...")
    magic = MagicalEffects(magic_intensity=1.0)
    
    # Add magical effects to structures
    for structure in world.structures[:5]:
        pos = structure['position']
        glow = magic.create_glow_effect(
            position=pos,
            color=structure['glow_color'],
            intensity=structure['glow_intensity'],
            radius=structure['base_size'] * 2
        )
        print(f"  ✨ Added glow to {structure['type']} at {pos[:2]}")
    
    world.save_world("example_high_magic_world.json")


def example_creature_showcase():
    """Showcase creature generation with geometric patterns"""
    print("\n" + "="*70)
    print("Example 3: Creature Showcase")
    print("="*70)
    
    config = WorldConfig(
        seed=77777,
        world_size=128,
        creature_density=0.3,  # High creature density
        magic_intensity=0.8
    )
    
    world = FractalWorld(config)
    world.generate_world()
    
    print(f"\n🐉 Generated {len(world.creatures)} Creatures:\n")
    
    # Group creatures by type
    creature_types = {}
    for creature in world.creatures:
        ctype = creature['type']
        if ctype not in creature_types:
            creature_types[ctype] = []
        creature_types[ctype].append(creature)
    
    # Display creature information
    for ctype, creatures in creature_types.items():
        print(f"\n{ctype} (Count: {len(creatures)})")
        example = creatures[0]
        print(f"  Pattern: {example['pattern']}")
        print(f"  Size: {example['size']}")
        print(f"  Geometric Complexity: {example['geometric_complexity']}")
        print(f"  Magic Level: {example['magic_level']:.2f}")
        print(f"  Color Palette: {example['color_palette']}")
        print(f"  Movement: {example['movement_pattern']['type']}")
    
    world.save_world("example_creature_showcase.json")


def example_visual_effects():
    """Demonstrate visual effects system"""
    print("\n" + "="*70)
    print("Example 4: Visual Effects Showcase")
    print("="*70)
    
    # Initialize systems
    magic = MagicalEffects(magic_intensity=0.9)
    lighting = LightingSystem(quality="cinematic")
    animation = AnimationSystem()
    textures = TextureSystem()
    
    print("\n💫 Creating Magical Effects:")
    
    # Create various particle effects
    effects = [
        ("Magical Sparkles", magic.create_particle_system((0, 0, 10), "magical_sparkles")),
        ("Mystical Aura", magic.create_particle_system((10, 10, 10), "mystical_aura")),
        ("Energy Burst", magic.create_particle_system((20, 20, 10), "energy_burst")),
        ("Fairy Dust", magic.create_particle_system((30, 30, 10), "fairy_dust")),
    ]
    
    for name, effect in effects:
        print(f"  ✨ {name}: {effect.particle_count} particles, {effect.pattern} pattern")
    
    print("\n💡 Setting up Lighting:")
    
    # Add various lights
    lighting.add_point_light((50, 50, 20), (255, 250, 205), 1.0, 30.0)
    lighting.add_point_light((100, 100, 15), (138, 43, 226), 0.8, 20.0)
    lighting.add_spot_light((75, 75, 50), (0, 0, -1), (255, 255, 255), 1.2, 45, 40.0)
    
    print(f"  💡 Added {len(lighting.lights)} lights")
    
    env_lighting = lighting.setup_environment_lighting()
    print(f"  🌍 Environment lighting: AO enabled, GI {'enabled' if env_lighting['global_illumination']['enabled'] else 'disabled'}")
    
    volumetric = lighting.create_volumetric_lighting()
    print(f"  🌫️ Volumetric effects: Fog density {volumetric['volumetric_fog']['density']}")
    
    print("\n🎬 Animation Systems:")
    
    # Create animations
    tree_anim = animation.create_idle_animation("tree")
    print(f"  🌳 Tree animation: sway {tree_anim['tree']['sway']['enabled']}, leaves rustle {tree_anim['tree']['leaf_rustle']['enabled']}")
    
    creature_anim = animation.create_idle_animation("creature")
    print(f"  🐉 Creature animation: breathing {creature_anim['creature']['breathing']['enabled']}, idle fidget {creature_anim['creature']['idle_fidget']['enabled']}")
    
    wind = animation.create_wind_animation(0.6)
    print(f"  💨 Wind: intensity {wind['intensity']}, affects {wind['affects']}")
    
    print("\n🎨 Texture Generation:")
    
    # Generate textures
    forest_tex = textures.generate_terrain_texture("forest", 0.4, 0.7)
    print(f"  🌲 Forest: color {forest_tex['base_color']}, roughness {forest_tex['roughness']:.2f}")
    
    mountain_tex = textures.generate_terrain_texture("mountains", 0.9, 0.3)
    print(f"  ⛰️ Mountains: color {mountain_tex['base_color']}, roughness {mountain_tex['roughness']:.2f}")
    
    print("\n📹 Post-Processing:")
    
    post = create_post_processing_stack("cinematic")
    print(f"  ✓ Bloom: threshold {post['bloom']['threshold']}, intensity {post['bloom']['intensity']}")
    print(f"  ✓ Depth of Field: {'enabled' if post['depth_of_field']['enabled'] else 'disabled'}")
    print(f"  ✓ Motion Blur: {post['motion_blur']['samples']} samples")
    print(f"  ✓ Color Grading: contrast {post['color_grading']['contrast']}, saturation {post['color_grading']['saturation']}")
    print(f"  ✓ Anti-aliasing: {post['anti_aliasing']['method']}")


def example_custom_config():
    """Generate world from custom configuration file"""
    print("\n" + "="*70)
    print("Example 5: Custom Configuration")
    print("="*70)
    
    # Load config
    with open("config.json", "r") as f:
        cfg = json.load(f)
    
    world_settings = cfg["world_settings"]
    
    config = WorldConfig(
        seed=world_settings["seed"],
        world_size=world_settings["world_size"],
        fractal_iterations=world_settings["fractal_iterations"],
        terrain_roughness=world_settings["terrain_roughness"],
        water_level=world_settings["water_level"],
        tree_density=world_settings["tree_density"],
        creature_density=world_settings["creature_density"],
        magic_intensity=world_settings["magic_intensity"],
        lighting_quality=cfg["rendering"]["lighting_quality"],
        enable_animations=cfg["rendering"]["enable_animations"]
    )
    
    print(f"📄 Loaded configuration from config.json")
    print(f"   World size: {config.world_size}x{config.world_size}")
    print(f"   Magic intensity: {config.magic_intensity}")
    print(f"   Lighting quality: {config.lighting_quality}")
    
    world = FractalWorld(config)
    world.generate_world()
    world.print_world_summary()
    world.save_world("example_custom_world.json")


def main():
    """Run all examples"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║          FRACTAL FANTASY WORLD - EXAMPLE DEMONSTRATIONS           ║
    ║                                                                   ║
    ║  Epic, immersive fantasy world where nature, creatures, and      ║
    ║  structures are generated by fractals, logic, and math patterns  ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    examples = [
        ("1", "Basic World Generation", example_basic_world),
        ("2", "High Magic World", example_high_magic_world),
        ("3", "Creature Showcase", example_creature_showcase),
        ("4", "Visual Effects Demo", example_visual_effects),
        ("5", "Custom Configuration", example_custom_config),
    ]
    
    print("Available Examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print("  0. Run all examples")
    
    choice = input("\nSelect example (0-5): ").strip()
    
    if choice == "0":
        for _, _, example_func in examples:
            example_func()
            print("\n" + "-"*70 + "\n")
    else:
        for num, _, example_func in examples:
            if choice == num:
                example_func()
                break
        else:
            print("Invalid choice!")
    
    print("\n✅ Examples completed!")
    print("📁 Generated world data saved to JSON files")
    print("🎮 Ready to integrate with your RPG engine!")


if __name__ == "__main__":
    main()
