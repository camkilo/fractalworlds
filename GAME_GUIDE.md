# Fractal Worlds RPG - Player's Guide

## Welcome, Adventurer!

Welcome to **Fractal Worlds**, a fully playable RPG where mathematics, logic, and fractals shape an ever-changing fantasy realm. This guide will help you master the game's systems and become a legendary hero.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Character & Stats](#character--stats)
3. [Exploration](#exploration)
4. [Combat System](#combat-system)
5. [Magic & Spells](#magic--spells)
6. [Crafting](#crafting)
7. [Puzzles](#puzzles)
8. [Ecosystem & Creatures](#ecosystem--creatures)
9. [Advanced Tips](#advanced-tips)

---

## Getting Started

### Installation & First Run

```bash
# Install and start your adventure
pip install -r requirements.txt
python game_integration.py
```

### Creating Your Character

```python
from game_integration import FractalRPG
from fractal_world import WorldConfig

# Customize your world
config = WorldConfig(
    seed=12345,              # Unique world seed
    world_size=256,          # Bigger = more to explore
    creature_density=0.15,   # More creatures = more challenge
    magic_intensity=0.8      # Higher = more magical effects
)

# Start your adventure
game = FractalRPG(config, player_name="YourName")
game.initialize_game()
```

---

## Character & Stats

### Core Statistics

Your character has six primary stats that determine your effectiveness:

| Stat | Description | Affects |
|------|-------------|---------|
| **Health** | Life force | Survival in combat |
| **Mana** | Magical energy | Spell casting capacity |
| **Stamina** | Physical endurance | Movement, attacks, gathering |
| **Strength** | Physical power | Melee damage |
| **Intelligence** | Mental prowess | Spell power |
| **Agility** | Speed and reflexes | Hit chance, dodge |
| **Logic Mastery** | Problem-solving | Spell power, puzzle solving |

### Skills

Five skills that improve through use:

1. **Combat** - Improves with fighting, increases critical chance
2. **Magic** - Improves with spellcasting, unlocks advanced spells
3. **Crafting** - Improves with item creation, unlocks complex recipes
4. **Exploration** - Improves with resource gathering, increases success rate
5. **Logic** - Improves with puzzle solving, enhances spell patterns

### Leveling Up

- Gain experience through actions (combat, magic, crafting, puzzles)
- Level up increases all base stats
- New spells and recipes unlock at higher levels
- Logic Mastery increases, making spells more powerful

---

## Exploration

### Movement

```python
# Move in any direction
game.play_turn("move", direction=(x, y, z), distance=10.0)

# Examples:
game.play_turn("move", direction=(10, 0, 0), distance=5.0)   # East
game.play_turn("move", direction=(0, 10, 0), distance=5.0)   # North
game.play_turn("move", direction=(-5, -5, 0), distance=7.0)  # Southwest
```

**Tips:**
- Movement costs stamina (0.1 per unit distance)
- Rest to recover stamina
- Explore systematically to map the world

### Discovering Your Surroundings

```python
# Check what's nearby
game.print_nearby(radius=50.0)  # Shows entities within 50 units

# View your status
game.print_status()

# Check specific status
result = game.play_turn("status")
```

### Resource Gathering

Resources are essential for crafting:

```python
# Gather from nearby resource nodes
game.play_turn("gather")
```

**Resource Types:**
- **Wood** (Nature element) - Found in forests
- **Crystals** (Earth element) - Near mountains
- **Arcane Crystals** (Arcane element) - Near magical structures
- **Elemental Essences** - Various locations

**Gathering Tips:**
- Success rate: 50% + (Exploration Skill × 10%)
- Costs 5 stamina per attempt
- Resources regenerate slowly over time
- Move around to find more nodes

---

## Combat System

### Basic Combat

```python
# Attack nearest enemy
game.play_turn("attack")
```

### Combat Mechanics

**Hit Calculation:**
```
Base Hit Chance = 70% + (Agility / 200)
Dodge Chance = Target Agility / 200
Final Hit = Base Hit - Dodge
```

**Damage Calculation:**
```
Base Damage = Weapon Power or (Strength / 2)
Multiplier = 1 + (Strength / 100)
Final Damage = Base × Multiplier
```

**Critical Hits:**
```
Crit Chance = 10% + (Combat Skill × 5%)
Crit Damage = Normal Damage × 2
```

### Elemental Advantages

Master the element wheel for maximum damage:

**Strong Against (1.5× damage):**
- 🔥 Fire → 🌿 Nature, 🪨 Earth
- 💧 Water → 🔥 Fire
- 🪨 Earth → 💨 Air, 💧 Water
- 💨 Air → 🔥 Fire
- ☀️ Light → 🌙 Dark
- 🌙 Dark → ☀️ Light
- 🌿 Nature → 💧 Water, 🪨 Earth

### Combat Tips

1. **Equip Proper Gear**
   ```python
   # Weapons increase damage
   # Armor reduces incoming damage
   ```

2. **Manage Stamina**
   - Each attack costs 10 stamina
   - Rest when stamina is low

3. **Use Elemental Weapons**
   - Craft weapons with advantageous elements
   - Check creature types before engaging

4. **Tactical Retreat**
   - If health is low, move away and rest
   - Stamina regenerates faster than health

---

## Magic & Spells

### Spell Casting

```python
# Cast a spell at a target location
target = (x, y, z)
game.play_turn("cast_spell", spell="Fireball", target=target)
```

### Available Spells

#### Basic Spells (Vector Pattern)
- **Fireball** - 30 power, 15 mana
  - Direct fire damage
- **Ice Shard** - 25 power, 12 mana
  - Ranged ice projectile
- **Earth Wall** - 35 power, 20 mana
  - Defensive barrier

#### Intermediate Spells (Sequence Pattern)
- **Lightning Chain** - 35 power, 20 mana
  - Chains between multiple targets
- **Nature's Wrath** - 45 power, 28 mana
  - Entangles enemies with vines

#### Advanced Spells (Symbolic Logic)
- **Healing Light** - 40 power, 25 mana
  - Restores health
- **Shadow Step** - 20 power, 18 mana
  - Teleportation ability

#### Master Spell (Fractal Pattern)
- **Fractal Storm** - 80 power, 50 mana
  - Devastating area effect
  - Requires Magic Skill 5.0+

### Spell Power Formula

```
Spell Power = Base Power × (1 + Intelligence/100) × Logic Mastery × Pattern Bonus

Pattern Bonuses:
- Vector: 1.0×
- Sequence: 1.2×
- Symbolic Logic: 1.5×
- Fractal: 2.0×
```

### Learning Spells

```python
# Some spells are learned automatically
# Others require finding spell tomes or solving puzzles

# Check if you can learn a spell
spell_system = game.game_state.spells
success, message = spell_system.learn_spell(game.game_state.player, "Fractal Storm")
```

### Magic Tips

1. **Manage Mana Carefully**
   - Rest to regenerate mana (5 per second)
   - Don't spam expensive spells

2. **Match Elements**
   - Use fire spells against nature creatures
   - Use water spells against fire creatures

3. **Upgrade Intelligence**
   - Higher intelligence = more spell power
   - Level up to increase stats

4. **Master Logic**
   - Logic Mastery increases with puzzle solving
   - Higher logic = stronger spells

---

## Crafting

### How to Craft

```python
# Craft an item using a recipe
game.play_turn("craft", recipe="Fire Sword")
```

### Crafting Recipes

#### Weapons

**Fire Sword**
- Pattern: Element Fusion
- Materials: Fire (3), Earth (2)
- Result: 25 damage weapon with fire element
- Required Crafting Skill: 2.0

**Ice Staff**
- Pattern: Element Fusion
- Materials: Water (3), Arcane (2)
- Result: 30 magic damage staff
- Required Crafting Skill: 3.0

**Nature Bow**
- Pattern: Element Fusion
- Materials: Nature (4), Air (1)
- Result: 20 damage, 50 range, poison effect
- Required Crafting Skill: 2.5

#### Armor

**Crystal Armor**
- Pattern: Geometric Fusion
- Materials: Earth (5), Light (2)
- Result: 40 defense armor
- Required Crafting Skill: 4.0

#### Special Items

**Arcane Rune**
- Pattern: Symbolic Logic
- Materials: Arcane (2), Light (1), Dark (1)
- Result: 1.5× spell power bonus
- Required Crafting Skill: 5.0

### Recipe Discovery

Experiment with element combinations to discover new recipes:

```python
# Try combining different elements
# If the combination matches a recipe, you'll discover it!
```

### Crafting Tips

1. **Gather Materials First**
   - Explore to find resource nodes
   - Different biomes have different resources

2. **Level Up Crafting Skill**
   - Craft simple items first
   - Gain experience to unlock advanced recipes

3. **Understand Logic Patterns**
   - Element Fusion: A AND B WHERE A > B
   - Geometric Fusion: A AND B WHERE A > B×2
   - Symbolic Logic: A AND (B XOR C)

---

## Puzzles

### Types of Puzzles

#### Sequence Puzzles
**Fibonacci Lock**
```
Description: Enter the next 3 numbers
Sequence: 1, 1, 2, 3, 5, 8, 13, ?, ?, ?
Solution: [21, 34, 55]
```

#### Logic Puzzles
**Element Balance**
```
Description: Balance Fire + Water + Earth
Answer: "A" (Air)
```

**Logic Circuit**
```
Description: Solve (A AND B) OR (NOT C)
Given: A=True, B=False, C=True
Solution: [False]
```

#### Mathematical Puzzles
**Prime Gate**
```
Description: Enter the 10th prime number
Solution: [29]
```

#### Pattern Puzzles
**Fractal Pattern**
```
Description: Complete the fractal sequence
Pattern: △ ▲ △△ ▲▲ △△△ ?
Solution: ["▲▲▲"]
```

### Solving Puzzles

```python
# Attempt to solve a puzzle
game.play_turn("solve_puzzle", 
               puzzle="Fibonacci Lock", 
               answer=[21, 34, 55])
```

### Puzzle Rewards

- **Experience Points** - 80-200 XP for Logic skill
- **Items** - Quest items, keys, gems
- **Spells** - Advanced spells like Fractal Storm
- **Unlocks** - Hidden areas and secrets

### Puzzle Tips

1. **Think Mathematically**
   - Most puzzles use math sequences or logic
   - Look for patterns

2. **Increase Logic Mastery**
   - Higher logic helps with future puzzles
   - Some puzzles give hints

3. **Write It Down**
   - Keep notes on puzzle solutions
   - Some puzzles have multiple solutions

---

## Ecosystem & Creatures

### Creature Types

Each creature has unique AI based on DNA-like traits:

#### Fractal Dragon
- **Aggression**: 0.8 (Very aggressive)
- **Intelligence**: 0.9 (Very smart)
- **Predator**: 1.0 (Top predator)
- **Behavior**: Hunts other creatures and defends territory

#### Geometric Wolf
- **Aggression**: 0.6 (Moderate)
- **Social**: 0.8 (Pack animal)
- **Predator**: 0.9 (Strong predator)
- **Behavior**: Hunts in groups, social interactions

#### Spiral Serpent
- **Aggression**: 0.5 (Moderate)
- **Predator**: 0.7
- **Prey**: 0.4
- **Behavior**: Opportunistic hunter, sometimes flees

#### Crystal Spider
- **Territorial**: 0.7 (Defensive)
- **Social**: 0.1 (Solitary)
- **Behavior**: Defends territory, builds webs

#### Pattern Bird
- **Social**: 0.9 (Highly social)
- **Prey**: 0.8 (Often hunted)
- **Behavior**: Flocks together, flees from predators

#### Golden Bear
- **Aggression**: 0.7 (Aggressive)
- **Territorial**: 0.8 (Highly territorial)
- **Behavior**: Defends large territories

### Creature Behaviors

Creatures make decisions based on their DNA:

- **Hunt**: Pursue prey creatures
- **Flee**: Escape from predators
- **Defend**: Protect territory from intruders
- **Socialize**: Interact with same species
- **Wander**: Explore when safe

### Ecosystem Dynamics

- **Predator-Prey**: Predators hunt prey species
- **Population Control**: Ecosystem self-regulates
- **Territory**: Creatures defend home areas
- **Social Bonds**: Some species group together

---

## Advanced Tips

### Efficient Exploration

1. **Systematic Scanning**
   ```python
   # Move in a grid pattern
   for x in range(0, 100, 20):
       game.play_turn("move", direction=(20, 0, 0), distance=20)
       game.print_nearby(radius=30)
       game.play_turn("move", direction=(0, 20, 0), distance=20)
   ```

2. **Resource Mapping**
   - Note where resource types appear
   - Forests = Nature resources
   - Mountains = Earth resources
   - Structures = Arcane resources

### Combat Strategies

1. **Elemental Mastery**
   - Craft multiple weapons with different elements
   - Switch based on enemy type

2. **Buff Before Battle**
   - Ensure full health, mana, stamina
   - Equip best gear

3. **Spell Combos**
   - Earth Wall for defense
   - Lightning Chain for multiple enemies
   - Healing Light when injured

### Crafting Optimization

1. **Farm Resources Efficiently**
   - Find high-density resource areas
   - Return after resources regenerate

2. **Progressive Crafting**
   - Start with basic weapons
   - Upgrade as crafting skill increases
   - Save rare materials for advanced items

### Character Development

1. **Balanced Build**
   - Don't neglect any skill
   - All skills are useful

2. **Specialization**
   - Focus on combat OR magic for power
   - Or balance both for versatility

3. **Logic is King**
   - Logic Mastery affects everything
   - Solve puzzles to boost logic quickly

### Save Game Strategy

```python
# Save often!
game.save_game("my_progress.json")

# Save before risky actions
game.save_game("before_boss.json")

# Keep multiple saves
game.save_game(f"save_level_{player.level}.json")
```

---

## Quick Reference

### Action Commands

| Action | Command | Example |
|--------|---------|---------|
| Move | `play_turn("move", direction=(x,y,z), distance=d)` | `game.play_turn("move", direction=(10,0,0), distance=5)` |
| Gather | `play_turn("gather")` | `game.play_turn("gather")` |
| Craft | `play_turn("craft", recipe="name")` | `game.play_turn("craft", recipe="Fire Sword")` |
| Cast | `play_turn("cast_spell", spell="name", target=(x,y,z))` | `game.play_turn("cast_spell", spell="Fireball", target=(100,100,50))` |
| Attack | `play_turn("attack")` | `game.play_turn("attack")` |
| Rest | `play_turn("rest")` | `game.play_turn("rest")` |
| Puzzle | `play_turn("solve_puzzle", puzzle="name", answer=ans)` | `game.play_turn("solve_puzzle", puzzle="Prime Gate", answer=[29])` |
| Status | `play_turn("status")` | `game.play_turn("status")` |

### Regeneration Rates

- **Health**: 2.0 per second
- **Mana**: 5.0 per second
- **Stamina**: 10.0 per second
- **Resources**: 0.1 per second (resource nodes)

### Cost Reference

| Action | Cost |
|--------|------|
| Movement | 0.1 stamina per unit |
| Attack | 10 stamina |
| Gathering | 5 stamina |
| Spell Casting | Varies (12-50 mana) |
| Resting | Free (accelerates regen) |

---

## Troubleshooting

**Q: No resources nearby?**
A: Move around more. Resources are clustered near forests and structures.

**Q: Can't learn a spell?**
A: Check if your Magic skill is high enough. Some spells require skill 2.0-5.0.

**Q: Crafting failed?**
A: Make sure you have enough of each required element and sufficient crafting skill.

**Q: Taking too much damage?**
A: Craft better armor, level up, and use elemental advantages.

**Q: Running out of mana?**
A: Rest frequently, level up for more max mana, use mana-efficient spells.

---

## Conclusion

You now have all the knowledge to become a master of Fractal Worlds! Remember:

- **Explore** systematically and thoroughly
- **Gather** resources for crafting
- **Craft** powerful equipment
- **Learn** magic and master spells
- **Fight** strategically with elemental advantages
- **Solve** puzzles to increase logic mastery
- **Level** up through experience

The fractal world is yours to conquer. Good luck, adventurer!

---

*For technical documentation, see README.md*
*For quick examples, run `python gameplay_examples.py`*
*For full game demo, run `python game_integration.py`*
