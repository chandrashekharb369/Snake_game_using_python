"""
UI Manager for Snake Odyssey.
Handles menus, HUD, and user interface elements.
"""

import pygame
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, 
                   GRAY, DARK_GRAY, THEMES)

class Button:
    """Simple button class."""
    def __init__(self, x, y, width, height, text, font, color=GRAY, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
        self.is_hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class UIManager:
    """Manages all UI elements and menus."""
    
    def __init__(self):
        """Initialize UI manager."""
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.current_menu = 'main'
        self.buttons = []
        self.selected_theme_filter = 'All'
        self.score_manager = None
        self.theme_manager = None
        self.game_over_score = 0
        self.game_over_stats = {}
        self.game_over_theme = None
        self.is_high_score = False
        self.setup_main_menu()
        
    def setup_main_menu(self):
        """Setup main menu UI elements."""
        self.current_menu = 'main'
        self.buttons = []
        
        # Create buttons
        self.buttons.append(Button(SCREEN_WIDTH//2 - 100, 250, 200, 50, 'Start Game', self.font_medium))
        self.buttons.append(Button(SCREEN_WIDTH//2 - 100, 320, 200, 50, 'Select Theme', self.font_medium))
        self.buttons.append(Button(SCREEN_WIDTH//2 - 100, 390, 200, 50, 'High Scores', self.font_medium))
        self.buttons.append(Button(SCREEN_WIDTH//2 - 100, 460, 200, 50, 'Quit', self.font_medium))
        
    def setup_theme_menu(self, theme_manager):
        """Setup theme selection menu."""
        self.current_menu = 'themes'
        self.buttons = []
        
        # Theme buttons
        themes = theme_manager.get_theme_list()
        for i, theme in enumerate(themes):
            y_pos = 200 + i * 60
            self.buttons.append(Button(SCREEN_WIDTH//2 - 100, y_pos, 200, 50, 
                                     THEMES[theme]['name'], self.font_medium))
            
        # Mix Mode button
        mix_y = 200 + len(themes) * 60
        self.buttons.append(Button(SCREEN_WIDTH//2 - 100, mix_y, 200, 50, 
                                 'Mix Mode', self.font_medium))
        
        # Back button
        self.buttons.append(Button(SCREEN_WIDTH//2 - 100, mix_y + 80, 200, 50, 
                                 'Back', self.font_medium))
        
    def setup_scores_menu(self, score_manager, theme_manager):
        """Setup high scores menu."""
        self.current_menu = 'scores'
        self.buttons = []
        self.score_manager = score_manager
        self.theme_manager = theme_manager
        
        # Back button
        self.buttons.append(Button(SCREEN_WIDTH//2 - 100, 690, 200, 50, 
                                 'Back', self.font_medium))
        
    def setup_game_over_menu(self, score_manager, theme):
        """Setup game over menu."""
        self.current_menu = 'game_over'
        self.buttons = []
        self.game_over_score = score_manager.get_current_score()
        self.game_over_stats = score_manager.get_score_statistics()
        self.game_over_theme = theme
        self.is_high_score = score_manager.is_high_score(theme)
        
        # Buttons
        self.buttons.append(Button(SCREEN_WIDTH//2 - 150, 450, 120, 50, 
                                 'Play Again', self.font_medium))
        self.buttons.append(Button(SCREEN_WIDTH//2 + 30, 450, 120, 50, 
                                 'Main Menu', self.font_medium))
        
    def clear_menu(self):
        """Clear current menu elements."""
        self.buttons = []
        
    def draw_game_hud(self, surface, score_manager, theme_manager, food_manager):
        """Draw game HUD during gameplay."""
        # Score
        score_text = self.font_medium.render(
            f"Score: {score_manager.format_score(score_manager.get_current_score())}", 
            True, WHITE)
        surface.blit(score_text, (20, 20))
        
        # Food count
        food_text = self.font_small.render(
            f"Food: {score_manager.get_food_count()}", True, WHITE)
        surface.blit(food_text, (20, 60))
        
        # Current theme
        theme_name = theme_manager.get_theme_display_name()
        theme_text = self.font_small.render(f"Theme: {theme_name}", True, WHITE)
        surface.blit(theme_text, (20, 90))
        
        # Difficulty level
        level = score_manager.get_difficulty_level()
        level_text = self.font_small.render(f"Level: {level}", True, WHITE)
        surface.blit(level_text, (20, 120))
        
        # Bonus timer
        if food_manager.has_bonus_food():
            time_left = food_manager.get_bonus_time_remaining()
            timer_text = self.font_small.render(
                f"Bonus: {time_left:.1f}s", True, (255, 215, 0))
            surface.blit(timer_text, (SCREEN_WIDTH - 150, 20))
            
        # Speed indicator
        speed_mult = score_manager.get_speed_multiplier()
        speed_text = self.font_small.render(f"Speed: {speed_mult:.1f}x", True, WHITE)
        surface.blit(speed_text, (SCREEN_WIDTH - 150, 50))
        
    def draw_pause_overlay(self, surface):
        """Draw pause overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        surface.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(pause_text, text_rect)
        
        instruction_text = self.font_medium.render("Press P to Resume", True, WHITE)
        inst_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        surface.blit(instruction_text, inst_rect)
        
    def handle_event(self, event):
        """Handle UI events."""
        for button in self.buttons:
            if button.handle_event(event):
                return button
        return None
        
    def update(self, time_delta):
        """Update UI manager."""
        pass
        
    def draw(self, surface):
        """Draw UI elements."""
        if self.current_menu == 'main':
            self.draw_main_menu(surface)
        elif self.current_menu == 'themes':
            self.draw_theme_menu(surface)
        elif self.current_menu == 'scores':
            self.draw_scores_menu(surface)
        elif self.current_menu == 'game_over':
            self.draw_game_over_menu(surface)
            
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
    def draw_main_menu(self, surface):
        """Draw main menu."""
        # Title
        title_text = self.font_large.render('Snake Odyssey: Themed Evolution', True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        surface.blit(title_text, title_rect)
        
    def draw_theme_menu(self, surface):
        """Draw theme selection menu."""
        # Title
        title_text = self.font_large.render('Select Theme', True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        surface.blit(title_text, title_rect)
        
    def draw_scores_menu(self, surface):
        """Draw high scores menu."""
        # Title
        title_text = self.font_large.render('High Scores', True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        surface.blit(title_text, title_rect)
        
        # Display scores only if score_manager is available
        if self.score_manager:
            y_offset = 150
            for theme_key, theme_data in THEMES.items():
                scores = self.score_manager.get_high_scores(theme_key)
                if scores:
                    theme_title = self.font_medium.render(f"{theme_data['name']} Theme", True, WHITE)
                    surface.blit(theme_title, (50, y_offset))
                    y_offset += 30
                    
                    for i, score in enumerate(scores[:5], 1):
                        score_text = self.font_small.render(
                            f"{i}. {score['player']} - {self.score_manager.format_score(score['score'])}", 
                            True, WHITE)
                        surface.blit(score_text, (70, y_offset))
                        y_offset += 25
                    y_offset += 20
        else:
            # Show message if no scores available
            no_scores_text = self.font_medium.render('No high scores yet!', True, WHITE)
            no_scores_rect = no_scores_text.get_rect(center=(SCREEN_WIDTH//2, 300))
            surface.blit(no_scores_text, no_scores_rect)
                
    def draw_game_over_menu(self, surface):
        """Draw game over menu."""
        # Title
        title_text = self.font_large.render('Game Over!', True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        surface.blit(title_text, title_rect)
        
        # Only display details if we have the data
        if self.score_manager and hasattr(self, 'game_over_score'):
            # Score
            score_text = self.font_medium.render(
                f'Final Score: {self.score_manager.format_score(self.game_over_score)}', True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 270))
            surface.blit(score_text, score_rect)
            
            # Statistics
            if hasattr(self, 'game_over_stats'):
                stats_text = (f"Food: {self.game_over_stats.get('food_eaten', 0)} | "
                             f"Bonus: {self.game_over_stats.get('bonus_eaten', 0)} | "
                             f"Level: {self.game_over_stats.get('difficulty', 0)}")
                stats_surface = self.font_small.render(stats_text, True, WHITE)
                stats_rect = stats_surface.get_rect(center=(SCREEN_WIDTH//2, 310))
                surface.blit(stats_surface, stats_rect)
            
            # Rank
            rank = self.score_manager.get_rank_title(self.game_over_score)
            rank_text = self.font_medium.render(f'Rank: {rank}', True, WHITE)
            rank_rect = rank_text.get_rect(center=(SCREEN_WIDTH//2, 350))
            surface.blit(rank_text, rank_rect)
            
            # High score notification
            if hasattr(self, 'is_high_score') and self.is_high_score:
                hs_text = self.font_medium.render('New High Score!', True, (255, 215, 0))
                hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH//2, 390))
                surface.blit(hs_text, hs_rect)

        
    def get_current_menu(self):
        """Get current menu state."""
        return self.current_menu