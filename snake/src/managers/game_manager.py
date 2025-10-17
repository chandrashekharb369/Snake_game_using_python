"""
Game Manager for Snake Odyssey.
Main game engine that coordinates all components.
"""

import pygame
import random
import time
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BOARD_WIDTH, BOARD_HEIGHT,
                   BOARD_X, BOARD_Y, CELL_SIZE, DIRECTIONS, BLACK, WHITE, THEMES)
from components.snake import Snake
from components.food import Food
from managers.theme_manager import ThemeManager
from managers.score_manager import ScoreManager
from managers.ui_manager import UIManager

class GameManager:
    """Main game engine managing all game systems."""
    
    def __init__(self):
        """Initialize game manager."""
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Odyssey: Themed Evolution")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.state = 'menu'  # 'menu', 'playing', 'paused', 'game_over'
        
        # Initialize managers
        self.theme_manager = ThemeManager()
        self.score_manager = ScoreManager()
        self.ui_manager = UIManager()
        
        # Game objects
        self.snake = None
        self.food = None
        self.obstacles = []
        self.particles = []
        
        # Game timing
        self.last_move_time = 0
        self.move_delay = 150  # milliseconds
        self.last_bonus_spawn = 0
        
        # Mix mode tracking
        self.last_mix_change = 0
        
    def run(self):
        """Main game loop."""
        while self.running:
            time_delta = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(time_delta)
            self.draw()
            
        pygame.quit()
        
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # UI event handling
            ui_element = self.ui_manager.handle_event(event)
            if ui_element:
                self.handle_ui_event(ui_element)
                
            # Game controls
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
                
    def handle_ui_event(self, ui_element):
        """Handle UI element interactions."""
        element_text = ui_element.text
        
        if self.ui_manager.get_current_menu() == 'main':
            if element_text == 'Start Game':
                self.start_game()
            elif element_text == 'Select Theme':
                self.ui_manager.setup_theme_menu(self.theme_manager)
            elif element_text == 'High Scores':
                self.ui_manager.setup_scores_menu(self.score_manager, self.theme_manager)
            elif element_text == 'Quit':
                self.running = False
                
        elif self.ui_manager.get_current_menu() == 'themes':
            if element_text == 'Back':
                self.ui_manager.setup_main_menu()
            elif element_text == 'Mix Mode':
                self.theme_manager.enable_mix_mode()
                self.ui_manager.setup_main_menu()
            elif element_text in ['Forest', 'Sea', 'Snow', 'Desert', 'Hill']:
                # Find theme key from display name
                for key, data in THEMES.items():
                    if data['name'] == element_text:
                        self.theme_manager.set_theme(key)
                        self.theme_manager.disable_mix_mode()
                        break
                self.ui_manager.setup_main_menu()
                
        elif self.ui_manager.get_current_menu() == 'scores':
            if element_text == 'Back':
                self.ui_manager.setup_main_menu()
                
        elif self.ui_manager.get_current_menu() == 'game_over':
            if element_text == 'Play Again':
                self.start_game()
            elif element_text == 'Main Menu':
                self.state = 'menu'
                self.ui_manager.setup_main_menu()
                
    def handle_keydown(self, key):
        """Handle keyboard input."""
        if self.state == 'playing':
            # Snake movement
            if key == pygame.K_UP or key == pygame.K_w:
                self.snake.change_direction(DIRECTIONS['UP'])
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.snake.change_direction(DIRECTIONS['DOWN'])
            elif key == pygame.K_LEFT or key == pygame.K_a:
                self.snake.change_direction(DIRECTIONS['LEFT'])
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                self.snake.change_direction(DIRECTIONS['RIGHT'])
            elif key == pygame.K_p:
                self.state = 'paused'
                
        elif self.state == 'paused':
            if key == pygame.K_p:
                self.state = 'playing'
                
        elif self.state == 'menu':
            if key == pygame.K_ESCAPE:
                self.running = False
                
    def start_game(self):
        """Initialize and start a new game."""
        self.state = 'playing'
        self.score_manager.reset_score()
        
        # Create snake
        start_x = (BOARD_WIDTH // CELL_SIZE) // 2
        start_y = (BOARD_HEIGHT // CELL_SIZE) // 2
        theme = self.theme_manager.get_current_theme()
        self.snake = Snake(start_x, start_y, theme['snake_color'])
        
        # Create food system
        self.food = Food(BOARD_WIDTH, BOARD_HEIGHT)
        self.food.spawn_regular_food(self.snake.body, self.obstacles)
        
        # Reset obstacles and particles
        self.obstacles = []
        self.particles = []
        
        # Reset timing
        self.last_move_time = pygame.time.get_ticks()
        self.last_bonus_spawn = 0
        self.last_mix_change = 0
        
        # Clear UI
        self.ui_manager.clear_menu()
        
    def update(self, time_delta):
        """Update game state."""
        if self.state == 'menu' or self.state == 'game_over':
            self.ui_manager.update(time_delta)
            self.theme_manager.update_transition()
            
        elif self.state == 'playing':
            self.update_game(time_delta)
            
        elif self.state == 'paused':
            # Only update particles and theme transitions during pause
            self.theme_manager.update_transition()
            self.theme_manager.update_particles(self.particles)
            
    def update_game(self, time_delta):
        """Update game logic during gameplay."""
        current_time = pygame.time.get_ticks()
        
        # Update theme transitions and particles
        self.theme_manager.update_transition()
        self.theme_manager.update_particles(self.particles)
        
        # Check for theme change in mix mode
        if self.theme_manager.mix_mode:
            self.theme_manager.change_theme_on_milestone(self.score_manager.get_current_score())
            
        # Update snake color based on current theme
        theme = self.theme_manager.get_current_theme()
        self.snake.color = theme['snake_color']
        
        # Calculate move delay based on score
        base_delay = 150
        speed_multiplier = self.score_manager.get_speed_multiplier()
        self.move_delay = max(80, int(base_delay / speed_multiplier))
        
        # Move snake
        if current_time - self.last_move_time > self.move_delay:
            self.snake.move()
            self.last_move_time = current_time
            
            # Check collisions
            if self.snake.check_collision(BOARD_WIDTH, BOARD_HEIGHT):
                self.game_over()
                return
                
            if self.snake.check_obstacle_collision(self.obstacles):
                self.game_over()
                return
                
            # Check food consumption
            regular_eaten, bonus_eaten = self.food.check_food_eaten(self.snake.get_head_position())
            
            if regular_eaten:
                self.snake.grow()
                self.score_manager.add_regular_food_score()
                
                # Create eating particles
                head_pos = self.snake.get_head_position()
                screen_pos = (BOARD_X + head_pos[0] * CELL_SIZE + CELL_SIZE // 2,
                             BOARD_Y + head_pos[1] * CELL_SIZE + CELL_SIZE // 2)
                particles = self.theme_manager.create_particle_effect(screen_pos, 'eat')
                self.particles.extend(particles)
                
                # Spawn new regular food
                self.food.spawn_regular_food(self.snake.body, self.obstacles)
                
                # Check for bonus food spawn
                if self.score_manager.should_spawn_bonus():
                    self.food.spawn_bonus_food(self.snake.body, self.obstacles)
                    
            if bonus_eaten:
                self.snake.grow()
                self.score_manager.add_bonus_food_score()
                
                # Create bonus particles
                head_pos = self.snake.get_head_position()
                screen_pos = (BOARD_X + head_pos[0] * CELL_SIZE + CELL_SIZE // 2,
                             BOARD_Y + head_pos[1] * CELL_SIZE + CELL_SIZE // 2)
                particles = self.theme_manager.create_particle_effect(screen_pos, 'bonus')
                self.particles.extend(particles)
                
        # Update food system
        self.food.update_bonus_food()
        
        # Update obstacles
        self.update_obstacles()
        
    def update_obstacles(self):
        """Update obstacle system."""
        target_count = self.score_manager.get_obstacle_count()
        
        if len(self.obstacles) < target_count:
            # Add new obstacle
            attempts = 0
            while attempts < 50:  # Prevent infinite loop
                x = random.randint(0, (BOARD_WIDTH // CELL_SIZE) - 1)
                y = random.randint(0, (BOARD_HEIGHT // CELL_SIZE) - 1)
                pos = (x, y)
                
                # Check if position is safe
                if (pos not in self.snake.body and 
                    pos != self.food.regular_food and 
                    pos != self.food.bonus_food and
                    pos not in self.obstacles):
                    
                    # Don't place too close to snake head
                    head = self.snake.get_head_position()
                    distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])
                    if distance > 3:
                        self.obstacles.append(pos)
                        break
                        
                attempts += 1
                
    def game_over(self):
        """Handle game over."""
        self.state = 'game_over'
        
        # Save high score
        current_theme = self.theme_manager.current_theme
        self.score_manager.save_high_score(current_theme)
        
        # Setup game over UI
        self.ui_manager.setup_game_over_menu(self.score_manager, current_theme)
        
    def draw(self):
        """Render everything to screen."""
        # Clear screen
        self.screen.fill(BLACK)
        
        if self.state == 'menu' or self.state == 'game_over':
            # Draw themed background for menus
            self.theme_manager.draw_background(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.ui_manager.draw(self.screen)
            
        elif self.state == 'playing' or self.state == 'paused':
            self.draw_game()
            
            if self.state == 'paused':
                self.ui_manager.draw_pause_overlay(self.screen)
                
        pygame.display.flip()
        
    def draw_game(self):
        """Draw game elements during gameplay."""
        # Draw themed background
        self.theme_manager.draw_background(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Draw game board border
        theme = self.theme_manager.get_current_theme()
        pygame.draw.rect(self.screen, WHITE, 
                        (BOARD_X - 2, BOARD_Y - 2, BOARD_WIDTH + 4, BOARD_HEIGHT + 4), 2)
        
        # Fill game board
        board_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        board_surface.fill(theme['background_color'])
        
        # Draw grid lines
        for x in range(0, BOARD_WIDTH, CELL_SIZE):
            pygame.draw.line(board_surface, theme['accent_color'], 
                           (x, 0), (x, BOARD_HEIGHT), 1)
        for y in range(0, BOARD_HEIGHT, CELL_SIZE):
            pygame.draw.line(board_surface, theme['accent_color'], 
                           (0, y), (BOARD_WIDTH, y), 1)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            x = obstacle[0] * CELL_SIZE
            y = obstacle[1] * CELL_SIZE
            pygame.draw.rect(board_surface, theme['obstacle_color'],
                           (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(board_surface, WHITE,
                           (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw food
        if self.food:
            self.food.draw(board_surface, 0, 0, theme)
            
        # Draw snake
        if self.snake:
            self.snake.draw(board_surface, 0, 0)
            
        # Blit board to main screen
        self.screen.blit(board_surface, (BOARD_X, BOARD_Y))
        
        # Draw particles
        self.theme_manager.draw_particles(self.screen, self.particles)
        
        # Draw HUD
        self.ui_manager.draw_game_hud(self.screen, self.score_manager, 
                                     self.theme_manager, self.food)
        
    def cleanup(self):
        """Cleanup resources."""
        pygame.quit()