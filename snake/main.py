"""
Snake Odyssey: Themed Evolution
A modern, theme-based Snake game with progressive difficulty and dynamic visuals.
"""

import pygame
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from managers.game_manager import GameManager

def main():
    """Main entry point for Snake Odyssey game."""
    try:
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create and run the game
        game = GameManager()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()