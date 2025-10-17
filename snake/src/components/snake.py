"""
Snake component for the Snake Odyssey game.
"""

import pygame
from config import CELL_SIZE, DIRECTIONS

class Snake:
    """Represents the snake entity in the game."""
    
    def __init__(self, start_x, start_y, color):
        """Initialize the snake."""
        self.body = [(start_x, start_y)]
        self.direction = DIRECTIONS['RIGHT']
        self.color = color
        self.grow_next = False
        
    def move(self):
        """Move the snake in the current direction."""
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False
            
    def change_direction(self, new_direction):
        """Change snake direction if valid."""
        # Prevent reverse direction
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction
            
    def grow(self):
        """Mark snake to grow on next move."""
        self.grow_next = True
        
    def check_collision(self, board_width, board_height):
        """Check if snake collides with walls or itself."""
        head = self.body[0]
        
        # Wall collision
        if (head[0] < 0 or head[0] >= board_width // CELL_SIZE or
            head[1] < 0 or head[1] >= board_height // CELL_SIZE):
            return True
            
        # Self collision
        if head in self.body[1:]:
            return True
            
        return False
        
    def check_obstacle_collision(self, obstacles):
        """Check if snake collides with obstacles."""
        head = self.body[0]
        return head in obstacles
        
    def draw(self, surface, board_x, board_y):
        """Draw the snake on the surface."""
        for i, segment in enumerate(self.body):
            x = board_x + segment[0] * CELL_SIZE
            y = board_y + segment[1] * CELL_SIZE
            
            # Draw head with different style
            if i == 0:
                # Head with eyes
                pygame.draw.rect(surface, self.color, 
                               (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, (255, 255, 255), 
                               (x, y, CELL_SIZE, CELL_SIZE), 2)
                # Eyes
                eye_size = 3
                pygame.draw.circle(surface, (255, 255, 255),
                                 (x + 5, y + 5), eye_size)
                pygame.draw.circle(surface, (255, 255, 255),
                                 (x + CELL_SIZE - 5, y + 5), eye_size)
            else:
                # Body segments
                pygame.draw.rect(surface, self.color, 
                               (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, (255, 255, 255), 
                               (x, y, CELL_SIZE, CELL_SIZE), 1)
                
    def get_head_position(self):
        """Get the position of the snake's head."""
        return self.body[0]
        
    def get_length(self):
        """Get the current length of the snake."""
        return len(self.body)