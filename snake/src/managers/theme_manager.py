"""
Theme Manager for Snake Odyssey.
Handles theme switching, visual effects, and theme-based progression.
"""

import pygame
import random
import math
from config import THEMES

class ThemeManager:
    """Manages game themes and visual effects."""
    
    def __init__(self):
        """Initialize theme manager."""
        self.current_theme = 'forest'
        self.mix_mode = False
        self.theme_transition_alpha = 0
        self.transitioning = False
        self.previous_theme_surface = None
        
    def set_theme(self, theme_name):
        """Set the current theme."""
        if theme_name in THEMES:
            if self.current_theme != theme_name:
                self.start_transition()
            self.current_theme = theme_name
            
    def enable_mix_mode(self):
        """Enable automatic theme changing."""
        self.mix_mode = True
        
    def disable_mix_mode(self):
        """Disable automatic theme changing."""
        self.mix_mode = False
        
    def get_current_theme(self):
        """Get current theme configuration."""
        return THEMES[self.current_theme]
        
    def get_theme_list(self):
        """Get list of available themes."""
        return list(THEMES.keys())
        
    def change_theme_on_milestone(self, score):
        """Change theme automatically in mix mode."""
        if self.mix_mode:
            theme_names = list(THEMES.keys())
            # Change theme every 100 points
            theme_index = (score // 100) % len(theme_names)
            new_theme = theme_names[theme_index]
            if new_theme != self.current_theme:
                self.set_theme(new_theme)
                
    def start_transition(self):
        """Start theme transition effect."""
        self.transitioning = True
        self.theme_transition_alpha = 255
        
    def update_transition(self):
        """Update theme transition animation."""
        if self.transitioning:
            self.theme_transition_alpha -= 8
            if self.theme_transition_alpha <= 0:
                self.transitioning = False
                self.theme_transition_alpha = 0
                
    def draw_background(self, surface, width, height):
        """Draw themed background."""
        theme = self.get_current_theme()
        
        # Base background
        surface.fill(theme['background_color'])
        
        # Add pattern based on theme
        self._draw_theme_pattern(surface, width, height, theme)
        
        # Apply transition effect
        if self.transitioning:
            overlay = pygame.Surface((width, height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(self.theme_transition_alpha)
            surface.blit(overlay, (0, 0))
            
    def _draw_theme_pattern(self, surface, width, height, theme):
        """Draw theme-specific background patterns."""
        if self.current_theme == 'forest':
            self._draw_forest_pattern(surface, width, height, theme)
        elif self.current_theme == 'sea':
            self._draw_sea_pattern(surface, width, height, theme)
        elif self.current_theme == 'snow':
            self._draw_snow_pattern(surface, width, height, theme)
        elif self.current_theme == 'desert':
            self._draw_desert_pattern(surface, width, height, theme)
        elif self.current_theme == 'hill':
            self._draw_hill_pattern(surface, width, height, theme)
            
    def _draw_forest_pattern(self, surface, width, height, theme):
        """Draw forest-themed pattern."""
        # Draw grass-like lines
        for i in range(0, width, 40):
            for j in range(0, height, 30):
                if random.random() < 0.3:
                    pygame.draw.line(surface, theme['accent_color'],
                                   (i, j), (i + 5, j - 10), 2)
                                   
    def _draw_sea_pattern(self, surface, width, height, theme):
        """Draw sea-themed pattern."""
        # Draw wave-like curves
        time_offset = pygame.time.get_ticks() * 0.002
        for y in range(0, height, 60):
            points = []
            for x in range(0, width + 20, 20):
                wave_y = y + 10 * math.cos(x * 0.02 + time_offset)
                points.append((x, wave_y))
            if len(points) > 1:
                pygame.draw.lines(surface, theme['accent_color'], False, points, 2)
                
    def _draw_snow_pattern(self, surface, width, height, theme):
        """Draw snow-themed pattern."""
        # Draw falling snowflakes
        time_offset = pygame.time.get_ticks()
        for i in range(20):
            x = (i * 67 + time_offset * 0.1) % width
            y = (i * 43 + time_offset * 0.05) % height
            size = 2 + (i % 3)
            pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), size)
            
    def _draw_desert_pattern(self, surface, width, height, theme):
        """Draw desert-themed pattern."""
        # Draw sand dunes
        for i in range(0, width, 100):
            for j in range(0, height, 80):
                if random.random() < 0.2:
                    pygame.draw.ellipse(surface, theme['accent_color'],
                                      (i, j, 60, 20))
                                      
    def _draw_hill_pattern(self, surface, width, height, theme):
        """Draw hill-themed pattern."""
        # Draw mountain silhouettes
        for i in range(0, width, 150):
            points = [(i, height), (i + 50, height - 100), 
                     (i + 100, height - 80), (i + 150, height)]
            if len(points) > 2:
                pygame.draw.polygon(surface, theme['accent_color'], points)
                
    def get_theme_display_name(self, theme_key=None):
        """Get display name for theme."""
        if theme_key is None:
            theme_key = self.current_theme
        return THEMES.get(theme_key, {}).get('name', theme_key.title())
        
    def create_particle_effect(self, pos, effect_type='eat'):
        """Create particle effects for game events."""
        particles = []
        theme = self.get_current_theme()
        
        if effect_type == 'eat':
            # Food eating particles
            for i in range(8):
                angle = i * 45
                velocity = random.uniform(2, 5)
                particles.append({
                    'pos': list(pos),
                    'vel': [velocity * math.cos(math.radians(angle)),
                           velocity * math.sin(math.radians(angle))],
                    'color': theme['food_color'],
                    'life': 30,
                    'max_life': 30
                })
        elif effect_type == 'bonus':
            # Bonus food particles
            for i in range(12):
                angle = i * 30
                velocity = random.uniform(3, 7)
                particles.append({
                    'pos': list(pos),
                    'vel': [velocity * math.cos(math.radians(angle)),
                           velocity * math.sin(math.radians(angle))],
                    'color': (255, 215, 0),
                    'life': 45,
                    'max_life': 45
                })
                
        return particles
        
    def update_particles(self, particles):
        """Update particle system."""
        for particle in particles[:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['vel'][0] *= 0.95  # Air resistance
            particle['vel'][1] *= 0.95
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                particles.remove(particle)
                
    def draw_particles(self, surface, particles):
        """Draw particle effects."""
        for particle in particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (*particle['color'], alpha)
            
            # Create surface for alpha blending
            particle_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (3, 3), 3)
            surface.blit(particle_surf, 
                        (int(particle['pos'][0] - 3), int(particle['pos'][1] - 3)))