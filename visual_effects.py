"""
Visual Effects System for Fractal Fantasy World
================================================
Implements cinematic lighting, glowing magical effects, particle systems,
and visual rendering for the fantasy world.
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ParticleEffect:
    """Particle effect configuration"""
    position: Tuple[float, float, float]
    particle_count: int
    color: Tuple[int, int, int]
    lifetime: float
    velocity_range: Tuple[float, float]
    size_range: Tuple[float, float]
    glow_intensity: float
    pattern: str  # spiral, burst, stream, float


class MagicalEffects:
    """Manager for magical visual effects"""
    
    def __init__(self, magic_intensity: float = 0.7):
        self.magic_intensity = magic_intensity
        self.active_effects = []
        
    def create_glow_effect(self, position: Tuple[float, float, float],
                          color: Tuple[int, int, int],
                          intensity: float,
                          radius: float) -> Dict[str, Any]:
        """Create a glowing magical effect"""
        return {
            "type": "glow",
            "position": position,
            "color": color,
            "intensity": intensity * self.magic_intensity,
            "radius": radius,
            "falloff": "exponential",
            "pulse": {
                "enabled": True,
                "speed": np.random.uniform(0.5, 2.0),
                "amplitude": np.random.uniform(0.1, 0.3)
            },
            "bloom": True,
            "bloom_threshold": 0.8,
            "bloom_intensity": 0.5
        }
    
    def create_particle_system(self, position: Tuple[float, float, float],
                              effect_type: str = "magical_sparkles") -> ParticleEffect:
        """Create a particle system for magical effects"""
        effects = {
            "magical_sparkles": {
                "count": 100,
                "color": (255, 215, 0),
                "lifetime": 2.0,
                "velocity": (0.5, 2.0),
                "size": (0.1, 0.3),
                "pattern": "float"
            },
            "mystical_aura": {
                "count": 200,
                "color": (138, 43, 226),
                "lifetime": 3.0,
                "velocity": (0.2, 1.0),
                "size": (0.2, 0.5),
                "pattern": "spiral"
            },
            "energy_burst": {
                "count": 300,
                "color": (0, 191, 255),
                "lifetime": 1.5,
                "velocity": (2.0, 5.0),
                "size": (0.15, 0.4),
                "pattern": "burst"
            },
            "fairy_dust": {
                "count": 150,
                "color": (255, 192, 203),
                "lifetime": 2.5,
                "velocity": (0.3, 1.5),
                "size": (0.08, 0.2),
                "pattern": "float"
            },
            "arcane_stream": {
                "count": 250,
                "color": (75, 0, 130),
                "lifetime": 3.5,
                "velocity": (1.0, 3.0),
                "size": (0.12, 0.35),
                "pattern": "stream"
            }
        }
        
        effect_config = effects.get(effect_type, effects["magical_sparkles"])
        
        return ParticleEffect(
            position=position,
            particle_count=effect_config["count"],
            color=effect_config["color"],
            lifetime=effect_config["lifetime"],
            velocity_range=effect_config["velocity"],
            size_range=effect_config["size"],
            glow_intensity=np.random.uniform(0.6, 1.0) * self.magic_intensity,
            pattern=effect_config["pattern"]
        )
    
    def create_magical_aura(self, entity_position: Tuple[float, float, float],
                           magic_level: float) -> Dict[str, Any]:
        """Create a magical aura around entities"""
        return {
            "type": "aura",
            "position": entity_position,
            "inner_color": (138, 43, 226),
            "outer_color": (186, 85, 211),
            "inner_radius": 0.5,
            "outer_radius": 2.0 * magic_level,
            "intensity": 0.7 * magic_level * self.magic_intensity,
            "rotation_speed": np.random.uniform(0.1, 0.5),
            "wave_effect": True,
            "shimmer": True
        }
    
    def create_spell_effect(self, spell_type: str,
                          position: Tuple[float, float, float]) -> Dict[str, Any]:
        """Create visual effect for spell casting"""
        spell_effects = {
            "fireball": {
                "particles": "energy_burst",
                "color": (255, 69, 0),
                "trail": True,
                "trail_color": (255, 140, 0),
                "explosion_radius": 5.0,
                "light_intensity": 1.0
            },
            "ice_shard": {
                "particles": "arcane_stream",
                "color": (135, 206, 235),
                "trail": True,
                "trail_color": (176, 224, 230),
                "crystalline": True,
                "light_intensity": 0.7
            },
            "lightning": {
                "particles": "energy_burst",
                "color": (255, 255, 0),
                "arc_effect": True,
                "branches": 5,
                "light_intensity": 1.2
            },
            "healing": {
                "particles": "fairy_dust",
                "color": (50, 205, 50),
                "spiral": True,
                "light_intensity": 0.8
            }
        }
        
        effect = spell_effects.get(spell_type, spell_effects["fireball"])
        effect["position"] = position
        effect["particle_system"] = self.create_particle_system(position, effect["particles"])
        
        return effect


class LightingSystem:
    """Advanced lighting system for cinematic quality"""
    
    def __init__(self, quality: str = "cinematic"):
        self.quality = quality
        self.lights = []
        
    def add_point_light(self, position: Tuple[float, float, float],
                       color: Tuple[int, int, int],
                       intensity: float,
                       radius: float,
                       cast_shadows: bool = True) -> int:
        """Add a point light to the scene"""
        light = {
            "type": "point",
            "position": position,
            "color": color,
            "intensity": intensity,
            "radius": radius,
            "attenuation": {
                "constant": 1.0,
                "linear": 0.09,
                "quadratic": 0.032
            },
            "cast_shadows": cast_shadows,
            "shadow_resolution": 2048 if self.quality == "cinematic" else 1024
        }
        self.lights.append(light)
        return len(self.lights) - 1
    
    def add_spot_light(self, position: Tuple[float, float, float],
                      direction: Tuple[float, float, float],
                      color: Tuple[int, int, int],
                      intensity: float,
                      angle: float,
                      radius: float) -> int:
        """Add a spot light to the scene"""
        light = {
            "type": "spot",
            "position": position,
            "direction": direction,
            "color": color,
            "intensity": intensity,
            "angle": angle,
            "radius": radius,
            "soft_edge": 0.2,
            "cast_shadows": True,
            "volumetric": True
        }
        self.lights.append(light)
        return len(self.lights) - 1
    
    def add_area_light(self, position: Tuple[float, float, float],
                      size: Tuple[float, float],
                      color: Tuple[int, int, int],
                      intensity: float) -> int:
        """Add an area light for soft, realistic lighting"""
        light = {
            "type": "area",
            "position": position,
            "size": size,
            "color": color,
            "intensity": intensity,
            "samples": 16 if self.quality == "cinematic" else 4,
            "cast_shadows": True,
            "soft_shadows": True
        }
        self.lights.append(light)
        return len(self.lights) - 1
    
    def setup_environment_lighting(self) -> Dict[str, Any]:
        """Setup environment lighting (HDRI, ambient)"""
        return {
            "ambient_occlusion": {
                "enabled": True,
                "samples": 32 if self.quality == "cinematic" else 8,
                "radius": 1.0,
                "intensity": 0.5
            },
            "global_illumination": {
                "enabled": self.quality == "cinematic",
                "bounces": 3 if self.quality == "cinematic" else 1,
                "samples": 256 if self.quality == "cinematic" else 64
            },
            "sky_light": {
                "enabled": True,
                "intensity": 0.8,
                "color": (135, 206, 235)
            },
            "indirect_lighting": {
                "enabled": True,
                "multiplier": 1.2
            }
        }
    
    def create_volumetric_lighting(self) -> Dict[str, Any]:
        """Create volumetric lighting effects (god rays, fog)"""
        return {
            "volumetric_fog": {
                "enabled": True,
                "density": 0.02,
                "color": (200, 200, 220),
                "scattering": 0.5,
                "height_falloff": 0.1
            },
            "god_rays": {
                "enabled": True,
                "samples": 64 if self.quality == "cinematic" else 32,
                "density": 0.8,
                "weight": 0.4,
                "decay": 0.95,
                "exposure": 0.3
            },
            "light_shafts": {
                "enabled": True,
                "intensity": 0.6
            }
        }


class AnimationSystem:
    """System for subtle animated movements"""
    
    def __init__(self):
        self.animations = []
        
    def create_idle_animation(self, entity_type: str) -> Dict[str, Any]:
        """Create subtle idle animation for entities"""
        animations = {
            "tree": {
                "sway": {
                    "enabled": True,
                    "amplitude": 0.1,
                    "frequency": 0.3,
                    "wind_response": True
                },
                "leaf_rustle": {
                    "enabled": True,
                    "intensity": 0.5,
                    "randomness": 0.3
                }
            },
            "creature": {
                "breathing": {
                    "enabled": True,
                    "rate": 0.5,
                    "amplitude": 0.05
                },
                "idle_fidget": {
                    "enabled": True,
                    "frequency": 0.1,
                    "randomness": 0.8
                },
                "eye_blink": {
                    "enabled": True,
                    "interval": 3.0
                }
            },
            "water": {
                "flow": {
                    "enabled": True,
                    "speed": 0.5,
                    "wave_height": 0.2,
                    "foam": True
                },
                "ripples": {
                    "enabled": True,
                    "frequency": 0.8
                }
            },
            "structure": {
                "ambient_glow": {
                    "enabled": True,
                    "pulse_speed": 0.2,
                    "amplitude": 0.15
                },
                "rune_flicker": {
                    "enabled": True,
                    "randomness": 0.5
                }
            }
        }
        
        return animations.get(entity_type, {})
    
    def create_movement_animation(self, pattern: str,
                                  speed: float) -> Dict[str, Any]:
        """Create movement animation based on pattern"""
        return {
            "pattern": pattern,
            "speed": speed,
            "interpolation": "smooth",
            "easing": "ease_in_out",
            "blend_time": 0.3,
            "root_motion": True
        }
    
    def create_wind_animation(self, intensity: float) -> Dict[str, Any]:
        """Create wind animation affecting vegetation"""
        return {
            "type": "wind",
            "intensity": intensity,
            "direction": (
                np.random.uniform(-1, 1),
                0,
                np.random.uniform(-1, 1)
            ),
            "variation": {
                "frequency": 0.2,
                "amplitude": 0.3
            },
            "affects": ["trees", "grass", "leaves"],
            "noise_pattern": "perlin"
        }


class TextureSystem:
    """System for realistic texture generation"""
    
    def __init__(self):
        self.textures = {}
        
    def generate_terrain_texture(self, biome: str,
                                 height: float,
                                 moisture: float) -> Dict[str, Any]:
        """Generate terrain texture based on biome and conditions"""
        texture = {
            "base_color": self._get_biome_color(biome),
            "roughness": self._calculate_roughness(biome, height),
            "metallic": 0.0,
            "normal_map": {
                "enabled": True,
                "strength": 1.0,
                "detail_scale": 10.0
            },
            "displacement": {
                "enabled": True,
                "strength": 0.5,
                "subdivisions": 4
            },
            "detail_layers": [
                {
                    "type": "noise",
                    "scale": 5.0,
                    "strength": 0.3
                },
                {
                    "type": "detail",
                    "scale": 20.0,
                    "strength": 0.5
                }
            ]
        }
        
        # Add wetness for high moisture areas
        if moisture > 0.7:
            texture["wetness"] = {
                "amount": (moisture - 0.7) / 0.3,
                "shininess": 0.8
            }
        
        return texture
    
    def _get_biome_color(self, biome: str) -> Tuple[int, int, int]:
        """Get base color for biome"""
        colors = {
            "forest": (34, 139, 34),
            "mountains": (139, 137, 137),
            "plains": (154, 205, 50),
            "desert": (237, 201, 175),
            "swamp": (85, 107, 47),
            "tundra": (245, 245, 245),
            "magical_grove": (50, 205, 50),
            "water": (65, 105, 225)
        }
        return colors.get(biome, (128, 128, 128))
    
    def _calculate_roughness(self, biome: str, height: float) -> float:
        """Calculate surface roughness"""
        base_roughness = {
            "forest": 0.8,
            "mountains": 0.9,
            "plains": 0.6,
            "desert": 0.7,
            "swamp": 0.7,
            "tundra": 0.4,
            "magical_grove": 0.6,
            "water": 0.1
        }
        
        roughness = base_roughness.get(biome, 0.7)
        
        # Higher elevations are rougher
        roughness += height * 0.2
        
        return min(1.0, roughness)
    
    def generate_creature_texture(self, pattern: str,
                                  colors: List[Tuple[int, int, int]]) -> Dict[str, Any]:
        """Generate texture for geometric creatures"""
        return {
            "pattern_type": pattern,
            "colors": colors,
            "pattern_scale": 2.0,
            "pattern_complexity": 0.8,
            "iridescence": {
                "enabled": True,
                "strength": 0.3,
                "shift": 0.1
            },
            "subsurface_scattering": {
                "enabled": True,
                "radius": 0.5,
                "color": colors[0] if colors else (255, 255, 255)
            },
            "specular": {
                "intensity": 0.5,
                "roughness": 0.4
            }
        }


def create_post_processing_stack(quality: str = "cinematic") -> Dict[str, Any]:
    """Create post-processing effects stack"""
    return {
        "bloom": {
            "enabled": True,
            "threshold": 0.8,
            "intensity": 0.5,
            "blur_passes": 5 if quality == "cinematic" else 3
        },
        "depth_of_field": {
            "enabled": quality == "cinematic",
            "focus_distance": 10.0,
            "aperture": 2.8,
            "bokeh": True
        },
        "motion_blur": {
            "enabled": True,
            "samples": 16 if quality == "cinematic" else 8,
            "shutter_angle": 180
        },
        "color_grading": {
            "enabled": True,
            "temperature": 6500,
            "tint": 0.0,
            "contrast": 1.1,
            "saturation": 1.15,
            "vibrance": 0.2,
            "highlights": (1.0, 1.0, 1.0),
            "midtones": (1.0, 1.0, 1.0),
            "shadows": (0.95, 0.95, 1.0)
        },
        "chromatic_aberration": {
            "enabled": True,
            "intensity": 0.3
        },
        "vignette": {
            "enabled": True,
            "intensity": 0.3,
            "smoothness": 0.5
        },
        "film_grain": {
            "enabled": True,
            "intensity": 0.1,
            "size": 1.0
        },
        "ambient_occlusion": {
            "enabled": True,
            "samples": 32 if quality == "cinematic" else 16,
            "radius": 1.0,
            "intensity": 0.8
        },
        "screen_space_reflections": {
            "enabled": quality == "cinematic",
            "quality": "high" if quality == "cinematic" else "medium"
        },
        "anti_aliasing": {
            "method": "TAA" if quality == "cinematic" else "FXAA",
            "quality": "high"
        }
    }


class CinematicCamera:
    """Cinematic camera system with advanced controls"""
    
    # Class constants
    DEFAULT_FPS = 60  # Default frame rate for cinematic paths
    
    def __init__(self):
        self.position = np.array([0.0, 0.0, 10.0])
        self.target = np.array([0.0, 0.0, 0.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.fov = 60.0  # Field of view in degrees
        self.near_clip = 0.1
        self.far_clip = 1000.0
        self.camera_modes = ["free", "follow", "orbit", "cinematic_path"]
        self.current_mode = "follow"
        self.smoothing = 0.1  # Camera smoothing factor
        self.shake_intensity = 0.0
        self.fps = self.DEFAULT_FPS  # Configurable frame rate
        
    def set_mode(self, mode: str):
        """Set camera mode"""
        if mode in self.camera_modes:
            self.current_mode = mode
    
    def follow_target(self, target_position: np.ndarray, offset: np.ndarray = None,
                     delta_time: float = 1.0):
        """Smooth follow camera"""
        if offset is None:
            offset = np.array([0.0, 5.0, 10.0])
        
        desired_position = target_position + offset
        self.position += (desired_position - self.position) * self.smoothing * delta_time
        
        # Smoothly look at target
        desired_target = target_position
        self.target += (desired_target - self.target) * self.smoothing * delta_time
    
    def orbit_around(self, center: np.ndarray, radius: float, angle: float, height: float):
        """Orbit camera around a point"""
        self.position[0] = center[0] + radius * np.cos(angle)
        self.position[1] = center[1] + height
        self.position[2] = center[2] + radius * np.sin(angle)
        self.target = center
    
    def apply_shake(self, intensity: float = 0.5, duration: float = 0.5):
        """Apply camera shake effect"""
        self.shake_intensity = intensity
        # In a real implementation, this would decay over time
    
    def get_shake_offset(self) -> np.ndarray:
        """Get current shake offset"""
        if self.shake_intensity <= 0:
            return np.array([0.0, 0.0, 0.0])
        
        shake = np.array([
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1)
        ]) * self.shake_intensity
        
        return shake
    
    def create_cinematic_path(self, keyframes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create a cinematic camera path with keyframes"""
        path = []
        
        for i in range(len(keyframes) - 1):
            current = keyframes[i]
            next_frame = keyframes[i + 1]
            
            # Interpolate between keyframes
            steps = int(current.get("duration", 1.0) * self.fps)
            
            for step in range(steps):
                t = step / steps
                # Cubic ease in-out
                t = t * t * (3.0 - 2.0 * t)
                
                interpolated = {
                    "position": self._lerp(
                        np.array(current["position"]),
                        np.array(next_frame["position"]),
                        t
                    ),
                    "target": self._lerp(
                        np.array(current["target"]),
                        np.array(next_frame["target"]),
                        t
                    ),
                    "fov": current["fov"] + (next_frame["fov"] - current["fov"]) * t
                }
                path.append(interpolated)
        
        return path
    
    def _lerp(self, a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
        """Linear interpolation"""
        return a + (b - a) * t
    
    def get_view_matrix(self) -> Dict[str, Any]:
        """Get view matrix parameters"""
        # Apply shake if active
        shake_offset = self.get_shake_offset()
        adjusted_position = self.position + shake_offset
        
        # Calculate view direction
        forward = self.target - adjusted_position
        forward = forward / (np.linalg.norm(forward) + 1e-10)
        
        # Calculate right and up vectors
        right = np.cross(forward, self.up)
        right = right / (np.linalg.norm(right) + 1e-10)
        
        up = np.cross(right, forward)
        
        return {
            "position": adjusted_position.tolist(),
            "target": self.target.tolist(),
            "forward": forward.tolist(),
            "right": right.tolist(),
            "up": up.tolist(),
            "fov": self.fov,
            "near": self.near_clip,
            "far": self.far_clip
        }
    
    def get_cinematic_angles(self) -> Dict[str, Any]:
        """Get cinematic camera angles and effects"""
        return {
            "dutch_angle": 0.0,  # Tilted camera angle
            "dolly_zoom": False,  # Vertigo effect
            "rack_focus": {
                "enabled": False,
                "near_focus": 10.0,
                "far_focus": 50.0
            },
            "letterbox": {
                "enabled": True,
                "aspect_ratio": 2.35  # Cinemascope
            }
        }


def main():
    """Demo of visual effects system"""
    print("\n🎨 Visual Effects System Demo\n")
    
    # Create magical effects manager
    magic = MagicalEffects(magic_intensity=0.8)
    
    # Create some magical effects
    glow = magic.create_glow_effect(
        position=(100, 100, 50),
        color=(138, 43, 226),
        intensity=0.8,
        radius=5.0
    )
    print(f"✨ Created glow effect: {glow['type']} with intensity {glow['intensity']}")
    
    # Create particle system
    particles = magic.create_particle_system(
        position=(150, 150, 30),
        effect_type="mystical_aura"
    )
    print(f"💫 Created particle system: {particles.particle_count} particles in {particles.pattern} pattern")
    
    # Create lighting system
    lighting = LightingSystem(quality="cinematic")
    lighting.add_point_light(
        position=(128, 128, 100),
        color=(255, 250, 205),
        intensity=1.0,
        radius=50.0
    )
    print(f"💡 Lighting system initialized with {len(lighting.lights)} lights")
    
    # Create animation system
    anim = AnimationSystem()
    tree_anim = anim.create_idle_animation("tree")
    print(f"🌳 Tree animation: {list(tree_anim.keys())}")
    
    # Create texture system
    textures = TextureSystem()
    terrain_tex = textures.generate_terrain_texture("forest", 0.5, 0.7)
    print(f"🎨 Terrain texture: base color {terrain_tex['base_color']}, roughness {terrain_tex['roughness']:.2f}")
    
    # Create post-processing
    post = create_post_processing_stack("cinematic")
    print(f"📹 Post-processing: {len(post)} effects enabled")
    
    print("\n✅ Visual effects system ready!")


if __name__ == "__main__":
    main()
