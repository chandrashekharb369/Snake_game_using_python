"""
Food component for the Snake Odyssey game.
"""

import pygame
import random
import time
from config import CELL_SIZE

class Food:
    """Represents food items in the game."""
    
    def __init__(self, board_width, board_height):
        """Initialize food system."""
        self.board_width = board_width
        self.board_height = board_height
        self.regular_food = None
        self.bonus_food = None
        self.bonus_timer = 0
        self.bonus_duration = 9  # seconds
        
    def spawn_regular_food(self, snake_body, obstacles):
        """Spawn regular food at random position."""
        while True:
            x = random.randint(0, (self.board_width // CELL_SIZE) - 1)
            y = random.randint(0, (self.board_height // CELL_SIZE) - 1)
            position = (x, y)
            
            if position not in snake_body and position not in obstacles:
                self.regular_food = position
                break
                
    def spawn_bonus_food(self, snake_body, obstacles):
        """Spawn bonus food for limited time."""
        while True:
            x = random.randint(0, (self.board_width // CELL_SIZE) - 1)
            y = random.randint(0, (self.board_height // CELL_SIZE) - 1)
            position = (x, y)
            
            if (position not in snake_body and position not in obstacles and 
                position != self.regular_food):
                self.bonus_food = position
                self.bonus_timer = time.time()
                break
                
    def update_bonus_food(self):
        """Update bonus food timer."""
        if self.bonus_food and time.time() - self.bonus_timer > self.bonus_duration:
            self.bonus_food = None
            self.bonus_timer = 0
            
    def check_food_eaten(self, snake_head):
        """Check if snake ate any food."""
        regular_eaten = self.regular_food == snake_head
        bonus_eaten = self.bonus_food == snake_head
        
        if regular_eaten:
            self.regular_food = None
            
        if bonus_eaten:
            self.bonus_food = None
            self.bonus_timer = 0
            
        return regular_eaten, bonus_eaten
        
    def draw(self, surface, board_x, board_y, theme):
        """Draw food items on the surface."""
        # Draw regular food
        if self.regular_food:
            x = board_x + self.regular_food[0] * CELL_SIZE
            y = board_y + self.regular_food[1] * CELL_SIZE
            
            pygame.draw.ellipse(surface, theme['food_color'],
                              (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
            pygame.draw.ellipse(surface, (255, 255, 255),
                              (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 2)
                              
        # Draw bonus food with pulsing effect
        if self.bonus_food:
            x = board_x + self.bonus_food[0] * CELL_SIZE
            y = board_y + self.bonus_food[1] * CELL_SIZE
            
            # Pulsing effect
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
            size_offset = int(pulse * 4)
            
            # Golden bonus food
            pygame.draw.ellipse(surface, (255, 215, 0),
                              (x + 2 - size_offset, y + 2 - size_offset, 
                               CELL_SIZE - 4 + size_offset * 2, 
                               CELL_SIZE - 4 + size_offset * 2))
            pygame.draw.ellipse(surface, (255, 255, 255),
                              (x + 2 - size_offset, y + 2 - size_offset, 
                               CELL_SIZE - 4 + size_offset * 2, 
                               CELL_SIZE - 4 + size_offset * 2), 2)
                               
    def get_bonus_time_remaining(self):
        """Get remaining time for bonus food."""
        if self.bonus_food:
            elapsed = time.time() - self.bonus_timer
            return max(0, self.bonus_duration - elapsed)
        return 0
        
    def has_regular_food(self):
        """Check if regular food exists."""
        return self.regular_food is not None
        
    def has_bonus_food(self):
        """Check if bonus food exists."""
        return self.bonus_food is not None