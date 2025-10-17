"""
Game Configuration Constants
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Game board settings
BOARD_WIDTH = 800
BOARD_HEIGHT = 600
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Game settings
INITIAL_SPEED = 8
SPEED_INCREMENT = 0.5
MAX_SPEED = 20
SCORE_PER_FOOD = 10
BONUS_SCORE = 20
BONUS_TIMER = 9  # seconds
DIFFICULTY_MILESTONE = 100  # points
OBSTACLE_START_SCORE = 200

# Theme definitions
THEMES = {
    'forest': {
        'name': 'Forest',
        'snake_color': (34, 139, 34),
        'food_symbol': '🍃',
        'food_color': (0, 255, 0),
        'background_color': (46, 125, 50),
        'accent_color': (27, 94, 32),
        'obstacle_color': (101, 67, 33),
        'sound_theme': 'forest'
    },
    'sea': {
        'name': 'Sea',
        'snake_color': (30, 144, 255),
        'food_symbol': '🐚',
        'food_color': (255, 192, 203),
        'background_color': (25, 118, 210),
        'accent_color': (13, 71, 161),
        'obstacle_color': (62, 39, 35),
        'sound_theme': 'sea'
    },
    'snow': {
        'name': 'Snow',
        'snake_color': (173, 216, 230),
        'food_symbol': '❄️',
        'food_color': (255, 255, 255),
        'background_color': (176, 196, 222),
        'accent_color': (100, 149, 237),
        'obstacle_color': (105, 105, 105),
        'sound_theme': 'snow'
    },
    'desert': {
        'name': 'Desert',
        'snake_color': (160, 82, 45),
        'food_symbol': '🌵',
        'food_color': (34, 139, 34),
        'background_color': (238, 203, 173),
        'accent_color': (205, 133, 63),
        'obstacle_color': (139, 69, 19),
        'sound_theme': 'desert'
    },
    'hill': {
        'name': 'Hill',
        'snake_color': (148, 0, 211),
        'food_symbol': '🪨',
        'food_color': (184, 134, 11),
        'background_color': (156, 39, 176),
        'accent_color': (74, 20, 140),
        'obstacle_color': (66, 66, 66),
        'sound_theme': 'hill'
    }
}

# Directions
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# File paths
DATA_DIR = 'data'
SCORES_FILE = 'high_scores.json'
SETTINGS_FILE = 'settings.json'