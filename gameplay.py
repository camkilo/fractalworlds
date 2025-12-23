"""
Fractal Fantasy World - Gameplay Systems
=========================================
Implements player mechanics, combat, crafting, spells, AI, and interactive gameplay
for the fully playable RPG experience.
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class ElementType(Enum):
    """Elements for crafting and magic"""
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    LIGHT = "light"
    DARK = "dark"
    NATURE = "nature"
    ARCANE = "arcane"


class SkillType(Enum):
    """Player skill categories"""
    COMBAT = "combat"
    MAGIC = "magic"
    CRAFTING = "crafting"
    EXPLORATION = "exploration"
    LOGIC = "logic"


@dataclass
class PlayerStats:
    """Player attributes and statistics"""
    health: float = 100.0
    max_health: float = 100.0
    mana: float = 100.0
    max_mana: float = 100.0
    stamina: float = 100.0
    max_stamina: float = 100.0
    strength: float = 10.0
    intelligence: float = 10.0
    agility: float = 10.0
    logic_mastery: float = 1.0  # Multiplier for spell power and puzzle solving (1.0-10.0)
    
    def regenerate(self, delta_time: float):
        """Regenerate health, mana, and stamina"""
        self.health = min(self.max_health, self.health + 2.0 * delta_time)
        self.mana = min(self.max_mana, self.mana + 5.0 * delta_time)
        self.stamina = min(self.max_stamina, self.stamina + 10.0 * delta_time)


@dataclass
class Item:
    """Inventory item"""
    name: str
    item_type: str  # resource, weapon, armor, spell_rune, crafted
    element: Optional[ElementType] = None
    power: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    quantity: int = 1


@dataclass
class Spell:
    """Spell definition with pattern-based mechanics"""
    name: str
    pattern: str  # vector, sequence, symbolic_logic, fractal
    elements: List[ElementType]
    formula: str  # Mathematical formula for spell power
    base_power: float
    mana_cost: float
    description: str
    
    def calculate_power(self, caster_intelligence: float, caster_logic: float) -> float:
        """Calculate spell power based on caster's stats"""
        # Base power scaled by intelligence and logic mastery
        power = self.base_power * (1 + caster_intelligence / 100.0) * caster_logic
        # Add pattern complexity bonus
        pattern_bonus = {
            "vector": 1.0,
            "sequence": 1.2,
            "symbolic_logic": 1.5,
            "fractal": 2.0
        }.get(self.pattern, 1.0)
        return power * pattern_bonus


class Player:
    """Main player character with full RPG mechanics"""
    
    def __init__(self, name: str = "Adventurer", position: Tuple[float, float, float] = (0, 0, 0)):
        self.name = name
        self.position = np.array(position, dtype=float)
        self.stats = PlayerStats()
        self.inventory: List[Item] = []
        self.equipped: Dict[str, Optional[Item]] = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.skills: Dict[SkillType, float] = {
            SkillType.COMBAT: 1.0,
            SkillType.MAGIC: 1.0,
            SkillType.CRAFTING: 1.0,
            SkillType.EXPLORATION: 1.0,
            SkillType.LOGIC: 1.0
        }
        self.known_spells: List[Spell] = []
        self.experience: int = 0
        self.level: int = 1
        
    def move(self, direction: np.ndarray, distance: float = 1.0):
        """Move player in a direction"""
        if self.stats.stamina >= distance * 0.1:
            normalized = direction / (np.linalg.norm(direction) + 1e-10)
            self.position += normalized * distance
            self.stats.stamina -= distance * 0.1
            return True
        return False
    
    def gather_resource(self, resource_node: Dict[str, Any]) -> Optional[Item]:
        """Gather resources from the environment"""
        if self.stats.stamina < 5.0:
            return None
        
        self.stats.stamina -= 5.0
        # Success based on exploration skill
        if np.random.random() < 0.5 + self.skills[SkillType.EXPLORATION] * 0.1:
            item = Item(
                name=resource_node.get("type", "Unknown Resource"),
                item_type="resource",
                element=ElementType[resource_node.get("element", "EARTH").upper()],
                properties=resource_node.get("properties", {})
            )
            self.add_to_inventory(item)
            self.gain_experience(10, SkillType.EXPLORATION)
            return item
        return None
    
    def add_to_inventory(self, item: Item):
        """Add item to inventory"""
        # Stack similar items
        for inv_item in self.inventory:
            if inv_item.name == item.name and inv_item.item_type == item.item_type:
                inv_item.quantity += item.quantity
                return
        self.inventory.append(item)
    
    def cast_spell(self, spell: Spell, target_position: Tuple[float, float, float]) -> Dict[str, Any]:
        """Cast a spell with pattern-based mechanics"""
        if self.stats.mana < spell.mana_cost:
            return {"success": False, "message": "Not enough mana"}
        
        # Calculate spell power
        power = spell.calculate_power(self.stats.intelligence, self.stats.logic_mastery)
        
        # Create spell effect
        effect = {
            "success": True,
            "spell": spell.name,
            "power": power,
            "position": target_position,
            "caster_position": tuple(self.position),
            "elements": [e.value for e in spell.elements],
            "pattern": spell.pattern,
            "visual_effects": self._generate_spell_visuals(spell, power)
        }
        
        self.stats.mana -= spell.mana_cost
        self.gain_experience(int(power * 5), SkillType.MAGIC)
        
        return effect
    
    def _generate_spell_visuals(self, spell: Spell, power: float) -> Dict[str, Any]:
        """Generate visual effects for spell casting"""
        colors = {
            ElementType.FIRE: (255, 69, 0),
            ElementType.WATER: (0, 191, 255),
            ElementType.EARTH: (139, 69, 19),
            ElementType.AIR: (240, 255, 255),
            ElementType.LIGHT: (255, 255, 224),
            ElementType.DARK: (75, 0, 130),
            ElementType.NATURE: (34, 139, 34),
            ElementType.ARCANE: (138, 43, 226)
        }
        
        primary_color = colors.get(spell.elements[0], (255, 255, 255))
        
        return {
            "particle_count": int(100 * power),
            "color": primary_color,
            "pattern": spell.pattern,
            "intensity": min(1.0, power / 100.0),
            "duration": 2.0 + power / 50.0
        }
    
    def gain_experience(self, amount: int, skill: SkillType):
        """Gain experience and level up skills"""
        self.experience += amount
        self.skills[skill] = min(10.0, self.skills[skill] + amount / 1000.0)
        
        # Level up
        required_xp = self.level * 100
        if self.experience >= required_xp:
            self.level_up()
    
    def level_up(self):
        """Level up and increase stats"""
        self.level += 1
        self.stats.max_health += 10.0
        self.stats.max_mana += 10.0
        self.stats.max_stamina += 5.0
        self.stats.strength += 2.0
        self.stats.intelligence += 2.0
        self.stats.agility += 2.0
        self.stats.logic_mastery += 0.1
        
        # Restore to full
        self.stats.health = self.stats.max_health
        self.stats.mana = self.stats.max_mana
        self.stats.stamina = self.stats.max_stamina


class CraftingSystem:
    """Logic-based crafting system"""
    
    def __init__(self):
        self.recipes: List[Dict[str, Any]] = []
        self.discovered_recipes: List[str] = []
        self._initialize_recipes()
    
    def _initialize_recipes(self):
        """Initialize crafting recipes with logic patterns"""
        # Basic weapon recipes
        self.recipes.extend([
            {
                "name": "Fire Sword",
                "pattern": "element_fusion",
                "inputs": [
                    {"element": ElementType.FIRE, "quantity": 3},
                    {"element": ElementType.EARTH, "quantity": 2}
                ],
                "logic_sequence": "A AND B WHERE A > B",
                "output": Item(
                    name="Fire Sword",
                    item_type="weapon",
                    element=ElementType.FIRE,
                    power=25.0,
                    properties={"damage": 25, "fire_damage": 10}
                ),
                "required_skill": 2.0
            },
            {
                "name": "Ice Staff",
                "pattern": "element_fusion",
                "inputs": [
                    {"element": ElementType.WATER, "quantity": 3},
                    {"element": ElementType.ARCANE, "quantity": 2}
                ],
                "logic_sequence": "A AND B WHERE A > B",
                "output": Item(
                    name="Ice Staff",
                    item_type="weapon",
                    element=ElementType.WATER,
                    power=30.0,
                    properties={"magic_damage": 30, "ice_damage": 15}
                ),
                "required_skill": 3.0
            },
            {
                "name": "Nature Bow",
                "pattern": "element_fusion",
                "inputs": [
                    {"element": ElementType.NATURE, "quantity": 4},
                    {"element": ElementType.AIR, "quantity": 1}
                ],
                "logic_sequence": "A AND B WHERE A > B*2",
                "output": Item(
                    name="Nature Bow",
                    item_type="weapon",
                    element=ElementType.NATURE,
                    power=20.0,
                    properties={"range": 50, "poison_chance": 0.3}
                ),
                "required_skill": 2.5
            },
            {
                "name": "Crystal Armor",
                "pattern": "geometric_fusion",
                "inputs": [
                    {"element": ElementType.EARTH, "quantity": 5},
                    {"element": ElementType.LIGHT, "quantity": 2}
                ],
                "logic_sequence": "A AND B WHERE A > B*2",
                "output": Item(
                    name="Crystal Armor",
                    item_type="armor",
                    element=ElementType.EARTH,
                    power=40.0,
                    properties={"defense": 40, "light_resistance": 0.5}
                ),
                "required_skill": 4.0
            },
            {
                "name": "Arcane Rune",
                "pattern": "symbolic_logic",
                "inputs": [
                    {"element": ElementType.ARCANE, "quantity": 2},
                    {"element": ElementType.LIGHT, "quantity": 1},
                    {"element": ElementType.DARK, "quantity": 1}
                ],
                "logic_sequence": "A AND (B XOR C)",
                "output": Item(
                    name="Arcane Rune",
                    item_type="spell_rune",
                    element=ElementType.ARCANE,
                    power=50.0,
                    properties={"spell_power_bonus": 1.5}
                ),
                "required_skill": 5.0
            }
        ])
    
    def craft_item(self, player: Player, recipe_name: str) -> Tuple[bool, str, Optional[Item]]:
        """Attempt to craft an item using a recipe"""
        recipe = None
        for r in self.recipes:
            if r["name"] == recipe_name:
                recipe = r
                break
        
        if not recipe:
            return False, "Recipe not found", None
        
        # Check crafting skill
        if player.skills[SkillType.CRAFTING] < recipe["required_skill"]:
            return False, f"Crafting skill too low (need {recipe['required_skill']})", None
        
        # Check and consume ingredients
        element_counts = {}
        for item in player.inventory:
            if item.element:
                element_counts[item.element] = element_counts.get(item.element, 0) + item.quantity
        
        # Verify ingredients
        for ingredient in recipe["inputs"]:
            element = ingredient["element"]
            required = ingredient["quantity"]
            if element_counts.get(element, 0) < required:
                return False, f"Not enough {element.value} (need {required})", None
        
        # Consume ingredients
        for ingredient in recipe["inputs"]:
            element = ingredient["element"]
            required = ingredient["quantity"]
            self._consume_ingredient(player, element, required)
        
        # Create output item
        output_item = Item(
            name=recipe["output"].name,
            item_type=recipe["output"].item_type,
            element=recipe["output"].element,
            power=recipe["output"].power,
            properties=recipe["output"].properties.copy()
        )
        
        player.add_to_inventory(output_item)
        
        # Add to discovered recipes
        if recipe_name not in self.discovered_recipes:
            self.discovered_recipes.append(recipe_name)
        
        # Grant experience
        player.gain_experience(int(recipe["required_skill"] * 20), SkillType.CRAFTING)
        
        return True, f"Crafted {recipe_name}!", output_item
    
    def _consume_ingredient(self, player: Player, element: ElementType, quantity: int):
        """Remove ingredients from inventory"""
        remaining = quantity
        for item in player.inventory[:]:
            if item.element == element:
                if item.quantity <= remaining:
                    remaining -= item.quantity
                    player.inventory.remove(item)
                else:
                    item.quantity -= remaining
                    remaining = 0
                
                if remaining == 0:
                    break
    
    def discover_recipe(self, player: Player, items_combined: List[Item]) -> Optional[str]:
        """Attempt to discover a recipe through experimentation"""
        # Check elements in combination
        element_counts = {}
        for item in items_combined:
            if item.element:
                element_counts[item.element] = element_counts.get(item.element, 0) + item.quantity
        
        # Check against recipes
        for recipe in self.recipes:
            if recipe["name"] in self.discovered_recipes:
                continue
            
            recipe_elements = {}
            for ingredient in recipe["inputs"]:
                recipe_elements[ingredient["element"]] = ingredient["quantity"]
            
            # Match elements
            if recipe_elements == element_counts:
                self.discovered_recipes.append(recipe["name"])
                player.gain_experience(50, SkillType.LOGIC)
                return recipe["name"]
        
        return None


class SpellSystem:
    """Pattern-based spell casting system"""
    
    def __init__(self):
        self.spells: List[Spell] = []
        self._initialize_spells()
    
    def _initialize_spells(self):
        """Initialize spell library"""
        self.spells.extend([
            Spell(
                name="Fireball",
                pattern="vector",
                elements=[ElementType.FIRE],
                formula="power = base * (1 + int/100) * logic",
                base_power=30.0,
                mana_cost=15.0,
                description="Hurls a ball of fire in a direction"
            ),
            Spell(
                name="Ice Shard",
                pattern="vector",
                elements=[ElementType.WATER],
                formula="power = base * (1 + int/100) * logic",
                base_power=25.0,
                mana_cost=12.0,
                description="Shoots sharp ice projectiles"
            ),
            Spell(
                name="Lightning Chain",
                pattern="sequence",
                elements=[ElementType.AIR, ElementType.ARCANE],
                formula="power = base * (1 + int/100) * logic * 1.2",
                base_power=35.0,
                mana_cost=20.0,
                description="Lightning that chains between targets"
            ),
            Spell(
                name="Healing Light",
                pattern="symbolic_logic",
                elements=[ElementType.LIGHT, ElementType.NATURE],
                formula="power = base * (1 + int/100) * logic * 1.5",
                base_power=40.0,
                mana_cost=25.0,
                description="Restores health using light and nature"
            ),
            Spell(
                name="Shadow Step",
                pattern="symbolic_logic",
                elements=[ElementType.DARK, ElementType.AIR],
                formula="power = base * (1 + int/100) * logic * 1.5",
                base_power=20.0,
                mana_cost=18.0,
                description="Teleport through shadows"
            ),
            Spell(
                name="Fractal Storm",
                pattern="fractal",
                elements=[ElementType.ARCANE, ElementType.AIR, ElementType.WATER],
                formula="power = base * (1 + int/100) * logic * 2.0",
                base_power=80.0,
                mana_cost=50.0,
                description="Devastating recursive storm pattern"
            ),
            Spell(
                name="Earth Wall",
                pattern="vector",
                elements=[ElementType.EARTH],
                formula="power = base * (1 + int/100) * logic",
                base_power=35.0,
                mana_cost=20.0,
                description="Raises a protective wall of earth"
            ),
            Spell(
                name="Nature's Wrath",
                pattern="sequence",
                elements=[ElementType.NATURE, ElementType.EARTH],
                formula="power = base * (1 + int/100) * logic * 1.2",
                base_power=45.0,
                mana_cost=28.0,
                description="Summons thorny vines to entangle enemies"
            )
        ])
    
    def learn_spell(self, player: Player, spell_name: str) -> Tuple[bool, str]:
        """Learn a new spell"""
        spell = None
        for s in self.spells:
            if s.name == spell_name:
                spell = s
                break
        
        if not spell:
            return False, "Spell not found"
        
        # Check if already known
        for known in player.known_spells:
            if known.name == spell_name:
                return False, "Spell already known"
        
        # Check requirements based on pattern complexity
        required_magic = {
            "vector": 1.0,
            "sequence": 2.0,
            "symbolic_logic": 3.5,
            "fractal": 5.0
        }.get(spell.pattern, 1.0)
        
        if player.skills[SkillType.MAGIC] < required_magic:
            return False, f"Magic skill too low (need {required_magic})"
        
        player.known_spells.append(spell)
        return True, f"Learned {spell_name}!"
    
    def get_spell(self, spell_name: str) -> Optional[Spell]:
        """Get spell by name"""
        for spell in self.spells:
            if spell.name == spell_name:
                return spell
        return None


class CombatSystem:
    """Emergent physics-based combat system"""
    
    def __init__(self):
        self.active_combats: List[Dict[str, Any]] = []
    
    def calculate_attack(self, attacker: Player, target: Dict[str, Any], 
                        attack_type: str = "melee") -> Dict[str, Any]:
        """Calculate attack with physics and probability"""
        result = {
            "hit": False,
            "damage": 0.0,
            "critical": False,
            "effects": []
        }
        
        # Calculate hit chance based on agility
        hit_chance = 0.7 + (attacker.stats.agility / 200.0)
        target_dodge = target.get("agility", 10.0) / 200.0
        
        if np.random.random() < (hit_chance - target_dodge):
            result["hit"] = True
            
            # Base damage
            weapon = attacker.equipped.get("weapon")
            if weapon:
                base_damage = weapon.power
            else:
                base_damage = attacker.stats.strength / 2.0
            
            # Physical damage formula
            damage_multiplier = 1.0 + (attacker.stats.strength / 100.0)
            damage = base_damage * damage_multiplier
            
            # Critical hit
            crit_chance = 0.1 + (attacker.skills[SkillType.COMBAT] * 0.05)
            if np.random.random() < crit_chance:
                damage *= 2.0
                result["critical"] = True
            
            # Apply elemental effects
            if weapon and weapon.element:
                elemental_bonus = self._calculate_elemental_effect(
                    weapon.element,
                    target.get("element", ElementType.EARTH)
                )
                damage *= elemental_bonus
                result["effects"].append({
                    "type": "elemental",
                    "element": weapon.element.value,
                    "bonus": elemental_bonus
                })
            
            # Environmental factors
            terrain_modifier = target.get("terrain_modifier", 1.0)
            damage *= terrain_modifier
            
            result["damage"] = damage
            attacker.stats.stamina -= 10.0
            attacker.gain_experience(int(damage), SkillType.COMBAT)
        
        return result
    
    def _calculate_elemental_effect(self, attack_element: ElementType, 
                                    target_element: ElementType) -> float:
        """Calculate elemental advantage/disadvantage"""
        # Element interaction matrix
        advantages = {
            ElementType.FIRE: [ElementType.NATURE, ElementType.EARTH],
            ElementType.WATER: [ElementType.FIRE],
            ElementType.EARTH: [ElementType.AIR, ElementType.WATER],
            ElementType.AIR: [ElementType.FIRE],
            ElementType.LIGHT: [ElementType.DARK],
            ElementType.DARK: [ElementType.LIGHT],
            ElementType.NATURE: [ElementType.WATER, ElementType.EARTH],
            ElementType.ARCANE: []
        }
        
        if target_element in advantages.get(attack_element, []):
            return 1.5  # Advantage
        elif attack_element in advantages.get(target_element, []):
            return 0.75  # Disadvantage
        return 1.0  # Neutral
    
    def cast_spell_in_combat(self, caster: Player, spell: Spell, 
                            target: Dict[str, Any]) -> Dict[str, Any]:
        """Cast spell during combat"""
        spell_effect = caster.cast_spell(spell, tuple(target.get("position", (0, 0, 0))))
        
        if not spell_effect["success"]:
            return spell_effect
        
        # Calculate spell damage/effect
        power = spell_effect["power"]
        
        # Elemental advantages
        elemental_mult = 1.0
        for element in spell.elements:
            elemental_mult *= self._calculate_elemental_effect(
                element,
                target.get("element", ElementType.EARTH)
            )
        
        damage = power * elemental_mult
        
        # Special spell effects
        if "healing" in spell.name.lower():
            caster.stats.health = min(caster.stats.max_health, 
                                     caster.stats.health + damage)
            spell_effect["healed"] = damage
            spell_effect["damage"] = 0
        else:
            spell_effect["damage"] = damage
        
        spell_effect["elemental_multiplier"] = elemental_mult
        
        return spell_effect


class CreatureAI:
    """Algorithmic AI for creatures with DNA-like patterns"""
    
    def __init__(self, creature_data: Dict[str, Any]):
        self.creature = creature_data
        self.dna = self._generate_dna()
        self.behavior_state = "idle"
        self.target = None
        self.home_position = np.array(creature_data.get("position", [0, 0, 0]))
    
    def _generate_dna(self) -> Dict[str, float]:
        """Generate DNA-like behavioral pattern"""
        creature_type = self.creature.get("type", "Unknown")
        
        # Base DNA patterns by creature type
        dna_patterns = {
            "Fractal Dragon": {
                "aggression": 0.8,
                "intelligence": 0.9,
                "social": 0.3,
                "territorial": 0.9,
                "predator": 1.0,
                "prey": 0.0
            },
            "Geometric Wolf": {
                "aggression": 0.6,
                "intelligence": 0.7,
                "social": 0.8,
                "territorial": 0.6,
                "predator": 0.9,
                "prey": 0.2
            },
            "Spiral Serpent": {
                "aggression": 0.5,
                "intelligence": 0.5,
                "social": 0.2,
                "territorial": 0.4,
                "predator": 0.7,
                "prey": 0.4
            },
            "Crystal Spider": {
                "aggression": 0.4,
                "intelligence": 0.6,
                "social": 0.1,
                "territorial": 0.7,
                "predator": 0.6,
                "prey": 0.5
            },
            "Pattern Bird": {
                "aggression": 0.2,
                "intelligence": 0.7,
                "social": 0.9,
                "territorial": 0.3,
                "predator": 0.3,
                "prey": 0.8
            },
            "Golden Bear": {
                "aggression": 0.7,
                "intelligence": 0.6,
                "social": 0.4,
                "territorial": 0.8,
                "predator": 0.8,
                "prey": 0.3
            }
        }
        
        base_dna = dna_patterns.get(creature_type, {
            "aggression": 0.5,
            "intelligence": 0.5,
            "social": 0.5,
            "territorial": 0.5,
            "predator": 0.5,
            "prey": 0.5
        })
        
        # Add random variation (±10%)
        for key in base_dna:
            variation = np.random.uniform(-0.1, 0.1)
            base_dna[key] = np.clip(base_dna[key] + variation, 0.0, 1.0)
        
        return base_dna
    
    def decide_action(self, nearby_entities: List[Dict[str, Any]], 
                     player: Optional[Player] = None) -> str:
        """Decide creature action based on AI and environment"""
        # Check for threats
        threats = []
        prey = []
        allies = []
        
        for entity in nearby_entities:
            if entity.get("type") == "player":
                # Decide if player is threat or prey
                if self.dna["aggression"] > 0.6 and self.dna["predator"] > 0.5:
                    threats.append(entity)
                elif self.dna["prey"] > 0.5:
                    self.behavior_state = "flee"
                    return "flee"
            elif entity.get("is_creature"):
                entity_dna = entity.get("dna", {})
                # Predator-prey relationship
                if self.dna["predator"] > entity_dna.get("predator", 0.5):
                    prey.append(entity)
                elif entity_dna.get("predator", 0.5) > self.dna["predator"]:
                    threats.append(entity)
                # Social bonding
                elif entity.get("type") == self.creature.get("type"):
                    if self.dna["social"] > 0.5:
                        allies.append(entity)
        
        # Decision tree based on DNA
        if threats and self.dna["prey"] > 0.5:
            self.behavior_state = "flee"
            self.target = threats[0]
            return "flee"
        
        if prey and self.dna["predator"] > 0.6:
            self.behavior_state = "hunt"
            self.target = prey[0]
            return "hunt"
        
        if allies and self.dna["social"] > 0.7:
            self.behavior_state = "social"
            self.target = allies[0]
            return "socialize"
        
        # Territorial behavior
        if player and self.dna["territorial"] > 0.7:
            player_pos = player.position
            distance = np.linalg.norm(player_pos - self.home_position)
            if distance < 20.0:  # Territory radius
                self.behavior_state = "defend"
                self.target = {"position": player_pos, "type": "player"}
                return "defend"
        
        # Default: wander
        self.behavior_state = "wander"
        return "wander"
    
    def execute_movement(self, action: str, delta_time: float) -> np.ndarray:
        """Execute movement based on action"""
        current_pos = np.array(self.creature.get("position", [0, 0, 0]))
        
        if action == "flee" and self.target:
            # Move away from threat
            threat_pos = np.array(self.target.get("position", current_pos))
            direction = current_pos - threat_pos
            speed = 3.0 * delta_time
        elif action in ["hunt", "defend"] and self.target:
            # Move toward target
            target_pos = np.array(self.target.get("position", current_pos))
            direction = target_pos - current_pos
            speed = 2.0 * delta_time
        elif action == "socialize" and self.target:
            # Move toward ally
            ally_pos = np.array(self.target.get("position", current_pos))
            direction = ally_pos - current_pos
            speed = 1.0 * delta_time
        else:  # wander
            # Random walk with bias toward home
            direction = np.random.randn(3)
            home_bias = (self.home_position - current_pos) * 0.1
            direction += home_bias
            speed = 1.0 * delta_time
        
        # Normalize and apply speed
        direction_norm = np.linalg.norm(direction)
        if direction_norm > 1e-6:
            direction = (direction / direction_norm) * speed
        
        return direction


class EcosystemSimulator:
    """Simulates dynamic ecosystem with predator-prey relationships"""
    
    def __init__(self):
        self.creatures: List[Dict[str, Any]] = []
        self.ai_controllers: Dict[int, CreatureAI] = {}
        self.population_history: List[Dict[str, int]] = []
    
    def add_creature(self, creature: Dict[str, Any]):
        """Add creature to ecosystem"""
        creature_id = len(self.creatures)
        creature["id"] = creature_id
        creature["is_creature"] = True
        self.creatures.append(creature)
        self.ai_controllers[creature_id] = CreatureAI(creature)
    
    def simulate_tick(self, delta_time: float, player: Optional[Player] = None):
        """Simulate one tick of the ecosystem"""
        # Track populations
        populations = {}
        
        for creature in self.creatures[:]:  # Copy to allow removal
            creature_type = creature.get("type", "Unknown")
            populations[creature_type] = populations.get(creature_type, 0) + 1
            
            creature_id = creature["id"]
            ai = self.ai_controllers[creature_id]
            
            # Find nearby entities (within 50 units)
            current_pos = np.array(creature["position"])
            nearby = []
            
            for other in self.creatures:
                if other["id"] == creature_id:
                    continue
                other_pos = np.array(other["position"])
                if np.linalg.norm(current_pos - other_pos) < 50.0:
                    nearby.append(other)
            
            # Add player if nearby
            if player:
                player_dist = np.linalg.norm(player.position - current_pos)
                if player_dist < 50.0:
                    nearby.append({
                        "position": tuple(player.position),
                        "type": "player",
                        "is_creature": False
                    })
            
            # Decide action
            action = ai.decide_action(nearby, player)
            
            # Execute movement
            movement = ai.execute_movement(action, delta_time)
            creature["position"] = (current_pos + movement).tolist()
            
            # Predator-prey interactions
            if action == "hunt" and ai.target:
                target_id = ai.target.get("id")
                if target_id is not None:
                    target_pos = np.array(ai.target["position"])
                    if np.linalg.norm(current_pos - target_pos) < 2.0:
                        # Successful hunt
                        self._remove_creature(target_id)
        
        self.population_history.append(populations)
    
    def _remove_creature(self, creature_id: int):
        """Remove creature from ecosystem"""
        self.creatures = [c for c in self.creatures if c["id"] != creature_id]
        if creature_id in self.ai_controllers:
            del self.ai_controllers[creature_id]


class PuzzleSystem:
    """Algorithmic puzzle system"""
    
    def __init__(self):
        self.puzzles: List[Dict[str, Any]] = []
        self._initialize_puzzles()
    
    def _initialize_puzzles(self):
        """Initialize puzzle types"""
        self.puzzles.extend([
            {
                "name": "Fibonacci Lock",
                "type": "sequence",
                "description": "Enter the next 3 numbers in the Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, ?, ?, ?",
                "solution": [21, 34, 55],
                "reward": {"experience": 100, "item": "Ancient Key"},
                "difficulty": 2
            },
            {
                "name": "Element Balance",
                "type": "logic",
                "description": "Balance the elements: Fire + Water + Earth = ? (A=Air, N=Nature, L=Light)",
                "solution": ["A"],  # Air balances fire+water+earth
                "reward": {"experience": 150, "item": "Elemental Orb"},
                "difficulty": 3
            },
            {
                "name": "Fractal Pattern",
                "type": "pattern",
                "description": "Complete the fractal: △ ▲ △△ ▲▲ △△△ ?",
                "solution": ["▲▲▲"],
                "reward": {"experience": 200, "spell": "Fractal Storm"},
                "difficulty": 4
            },
            {
                "name": "Prime Gate",
                "type": "mathematical",
                "description": "Enter the 10th prime number to open the gate",
                "solution": [29],
                "reward": {"experience": 80, "item": "Gate Crystal"},
                "difficulty": 2
            },
            {
                "name": "Logic Circuit",
                "type": "logic",
                "description": "Solve: (A AND B) OR (NOT C) where A=True, B=False, C=True",
                "solution": [False],  # (T AND F) OR (NOT T) = F OR F = F
                "reward": {"experience": 120, "item": "Logic Gem"},
                "difficulty": 3
            }
        ])
    
    def attempt_puzzle(self, player: Player, puzzle_name: str, 
                      answer: Any) -> Tuple[bool, str, Dict[str, Any]]:
        """Attempt to solve a puzzle"""
        puzzle = None
        for p in self.puzzles:
            if p["name"] == puzzle_name:
                puzzle = p
                break
        
        if not puzzle:
            return False, "Puzzle not found", {}
        
        # Check if solution is correct
        correct = False
        if isinstance(puzzle["solution"], list):
            if isinstance(answer, list):
                correct = answer == puzzle["solution"]
            else:
                correct = [answer] == puzzle["solution"]
        else:
            correct = answer == puzzle["solution"]
        
        if correct:
            # Grant rewards
            rewards = puzzle["reward"]
            
            # Experience
            if "experience" in rewards:
                player.gain_experience(rewards["experience"], SkillType.LOGIC)
            
            # Item reward
            if "item" in rewards:
                item = Item(
                    name=rewards["item"],
                    item_type="quest_item",
                    power=puzzle["difficulty"] * 10.0
                )
                player.add_to_inventory(item)
            
            # Spell reward
            if "spell" in rewards:
                spell_system = SpellSystem()
                spell_system.learn_spell(player, rewards["spell"])
            
            return True, f"Puzzle solved! {puzzle['name']}", rewards
        else:
            return False, "Incorrect solution", {}
    
    def get_puzzle(self, difficulty: int) -> Optional[Dict[str, Any]]:
        """Get a random puzzle of given difficulty"""
        suitable = [p for p in self.puzzles if p["difficulty"] == difficulty]
        if suitable:
            return suitable[np.random.randint(len(suitable))]
        return None


class InteractiveEnvironment:
    """System for interactive and destructible terrain"""
    
    def __init__(self, world_size: int = 256):
        self.world_size = world_size
        self.terrain_modifications: List[Dict[str, Any]] = []
        self.resource_nodes: List[Dict[str, Any]] = []
    
    def modify_terrain(self, position: Tuple[float, float, float], 
                      modification_type: str, radius: float = 5.0) -> Dict[str, Any]:
        """Modify terrain at a position"""
        modification = {
            "position": position,
            "type": modification_type,  # crater, raise, flatten, destroy
            "radius": radius,
            "timestamp": 0  # Would be actual timestamp in real game
        }
        
        self.terrain_modifications.append(modification)
        
        return {
            "success": True,
            "modification": modification,
            "affected_area": np.pi * radius ** 2
        }
    
    def create_resource_node(self, position: Tuple[float, float, float], 
                            resource_type: str, element: ElementType) -> Dict[str, Any]:
        """Create a resource gathering node"""
        node = {
            "position": position,
            "type": resource_type,
            "element": element.value,
            "quantity": np.random.randint(5, 20),
            "regeneration_rate": 0.1,
            "properties": {
                "hardness": np.random.uniform(0.3, 0.9),
                "purity": np.random.uniform(0.5, 1.0)
            }
        }
        
        self.resource_nodes.append(node)
        return node
    
    def get_nearby_resources(self, position: Tuple[float, float, float], 
                           radius: float = 10.0) -> List[Dict[str, Any]]:
        """Get resource nodes near a position"""
        pos_array = np.array(position)
        nearby = []
        
        for node in self.resource_nodes:
            node_pos = np.array(node["position"])
            if np.linalg.norm(pos_array - node_pos) <= radius:
                nearby.append(node)
        
        return nearby
    
    def harvest_resource(self, node: Dict[str, Any], amount: int = 1) -> bool:
        """Harvest from a resource node"""
        if node["quantity"] >= amount:
            node["quantity"] -= amount
            return True
        return False


class GameState:
    """Main game state manager"""
    
    def __init__(self, world_data: Dict[str, Any] = None):
        self.player = Player()
        self.world_data = world_data or {}
        self.crafting = CraftingSystem()
        self.spells = SpellSystem()
        self.combat = CombatSystem()
        self.ecosystem = EcosystemSimulator()
        self.puzzles = PuzzleSystem()
        self.environment = InteractiveEnvironment()
        self.time_elapsed = 0.0
        self.game_active = True
        
        # Initialize world creatures
        if world_data and "creatures" in world_data:
            for creature in world_data["creatures"]:
                self.ecosystem.add_creature(creature.copy())
    
    def tick(self, delta_time: float = 1.0):
        """Update game state"""
        if not self.game_active:
            return
        
        self.time_elapsed += delta_time
        
        # Regenerate player stats
        self.player.stats.regenerate(delta_time)
        
        # Simulate ecosystem
        self.ecosystem.simulate_tick(delta_time, self.player)
        
        # Regenerate resources
        for node in self.environment.resource_nodes:
            if node["quantity"] < 20:
                node["quantity"] = min(20, node["quantity"] + node["regeneration_rate"] * delta_time)
    
    def save_game(self, filename: str):
        """Save game state to file"""
        game_data = {
            "player": {
                "name": self.player.name,
                "position": self.player.position.tolist(),
                "stats": {
                    "health": self.player.stats.health,
                    "max_health": self.player.stats.max_health,
                    "mana": self.player.stats.mana,
                    "max_mana": self.player.stats.max_mana,
                    "stamina": self.player.stats.stamina,
                    "max_stamina": self.player.stats.max_stamina,
                    "strength": self.player.stats.strength,
                    "intelligence": self.player.stats.intelligence,
                    "agility": self.player.stats.agility,
                    "logic_mastery": self.player.stats.logic_mastery
                },
                "inventory": [
                    {
                        "name": item.name,
                        "type": item.item_type,
                        "element": item.element.value if item.element else None,
                        "power": item.power,
                        "quantity": item.quantity,
                        "properties": item.properties
                    }
                    for item in self.player.inventory
                ],
                "skills": {k.value: v for k, v in self.player.skills.items()},
                "known_spells": [spell.name for spell in self.player.known_spells],
                "experience": self.player.experience,
                "level": self.player.level
            },
            "world_data": self.world_data,
            "time_elapsed": self.time_elapsed,
            "discovered_recipes": self.crafting.discovered_recipes,
            "ecosystem": {
                "creatures": self.ecosystem.creatures,
                "population_history": self.ecosystem.population_history[-100:]  # Last 100 ticks
            },
            "environment": {
                "modifications": self.environment.terrain_modifications,
                "resource_nodes": self.environment.resource_nodes
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(game_data, f, indent=2)
    
    def load_game(self, filename: str):
        """Load game state from file"""
        with open(filename, 'r') as f:
            game_data = json.load(f)
        
        # Restore player
        player_data = game_data["player"]
        self.player = Player(player_data["name"], tuple(player_data["position"]))
        
        # Restore stats
        stats_data = player_data["stats"]
        for key, value in stats_data.items():
            setattr(self.player.stats, key, value)
        
        # Restore inventory
        for item_data in player_data["inventory"]:
            item = Item(
                name=item_data["name"],
                item_type=item_data["type"],
                element=ElementType[item_data["element"].upper()] if item_data["element"] else None,
                power=item_data["power"],
                properties=item_data["properties"],
                quantity=item_data["quantity"]
            )
            self.player.inventory.append(item)
        
        # Restore skills
        for skill_name, value in player_data["skills"].items():
            self.player.skills[SkillType(skill_name)] = value
        
        # Restore spells
        for spell_name in player_data["known_spells"]:
            spell = self.spells.get_spell(spell_name)
            if spell:
                self.player.known_spells.append(spell)
        
        self.player.experience = player_data["experience"]
        self.player.level = player_data["level"]
        
        # Restore world
        self.world_data = game_data["world_data"]
        self.time_elapsed = game_data["time_elapsed"]
        self.crafting.discovered_recipes = game_data["discovered_recipes"]
        
        # Restore ecosystem
        ecosystem_data = game_data["ecosystem"]
        for creature in ecosystem_data["creatures"]:
            self.ecosystem.add_creature(creature)
        
        # Restore environment
        env_data = game_data["environment"]
        self.environment.terrain_modifications = env_data["modifications"]
        self.environment.resource_nodes = env_data["resource_nodes"]
