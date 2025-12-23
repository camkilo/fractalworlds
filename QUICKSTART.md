# Fractal Fantasy World - Quick Start Guide

Welcome to the Fractal Fantasy World generator! This guide will help you get started quickly.

## Installation

```bash
# Clone the repository
git clone https://github.com/camkilo/fractalworlds.git
cd fractalworlds

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Generate Your First World

```bash
python fractal_world.py
```

This will generate a complete fantasy world with default settings and save it to `fractal_world.json`.

### 2. Run Interactive Examples

```bash
python examples.py
```

Choose from 5 different examples:
- Basic world generation
- High magic world
- Creature showcase
- Visual effects demo
- Custom configuration

### 3. Customize Your World

Edit `config.json` to customize world settings:

```json
{
  "world_settings": {
    "seed": 42,              // Change for different worlds
    "world_size": 256,       // Map size (128-512 recommended)
    "magic_intensity": 0.8   // 0.0 to 1.0
  }
}
```

## Code Examples

### Generate a World in Python

```python
from fractal_world import FractalWorld, WorldConfig

# Create and generate world
world = FractalWorld()
world.generate_world()
world.print_world_summary()
world.save_world("my_world.json")
```

### Custom Configuration

```python
config = WorldConfig(
    seed=12345,
    world_size=256,
    magic_intensity=0.9,
    creature_density=0.2
)

world = FractalWorld(config)
world.generate_world()
```

### Access World Data

```python
# After generation
print(f"Forests: {len(world.forests)}")
print(f"Creatures: {len(world.creatures)}")
print(f"Structures: {len(world.structures)}")

# Iterate through creatures
for creature in world.creatures:
    print(f"{creature['type']} at {creature['position']}")
```

## Key Features

✨ **Fractal Terrain** - Multi-octave noise for realistic landscapes
🌲 **Procedural Forests** - L-system tree generation
🐉 **Geometric Creatures** - 6 unique creature types with patterns
🏰 **Fractal Structures** - Sacred geometry architecture
💫 **Magical Effects** - Glowing particles and auras
💡 **Cinematic Lighting** - Advanced lighting system
🌌 **Dynamic Sky** - Clouds, auroras, stars

## World Features

Generated worlds include:
- 7 biome types (forest, mountains, plains, desert, swamp, tundra, magical groves)
- Procedural forests with L-system trees
- Rivers that flow from mountains to sea
- Creatures with mathematical patterns
- Structures with fractal geometry
- Dynamic lighting and effects

## Output Format

The generated `fractal_world.json` contains:
- Terrain data and statistics
- All forest locations and tree details
- River paths and flow properties
- Creature positions and attributes
- Structure locations and designs
- Lighting configuration
- Sky and weather settings

## Integration

Import the JSON data into your game engine:

```python
import json

with open("fractal_world.json", "r") as f:
    world = json.load(f)

# Access data
creatures = world["creatures"]
terrain = world["terrain_stats"]
```

## Troubleshooting

**Problem**: Module not found error
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Problem**: Slow generation
**Solution**: Reduce `world_size` in config (try 128 or 64)

**Problem**: No rivers generated
**Solution**: This can happen randomly. Try different seeds or increase world size

## Next Steps

1. Experiment with different seeds and settings
2. Export world data to your game engine
3. Customize creature types in `fractal_world.py`
4. Add new biomes or structure types
5. Integrate with Unity, Unreal, or Godot

## Resources

- Full documentation: See README.md
- Examples: Run `python examples.py`
- Visual effects: See `visual_effects.py`
- Configuration: Edit `config.json`

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review the examples in examples.py
- Open an issue on GitHub

---

**Happy World Building! 🌍✨**
