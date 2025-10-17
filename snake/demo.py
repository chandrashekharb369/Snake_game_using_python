"""
Demo script for Snake Odyssey: Themed Evolution
Showcases key features and game architecture
"""

import pygame
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from managers.theme_manager import ThemeManager
from managers.score_manager import ScoreManager
from config import THEMES

def demo_themes():
    """Demonstrate theme system capabilities."""
    print("🎨 Snake Odyssey: Theme System Demo")
    print("=" * 50)
    
    theme_manager = ThemeManager()
    
    print(f"Available themes: {len(THEMES)}")
    for theme_key, theme_data in THEMES.items():
        print(f"\n🎯 {theme_data['name']} Theme:")
        print(f"   Snake Color: {theme_data['snake_color']}")
        print(f"   Food Symbol: {theme_data['food_symbol']}")
        print(f"   Background:  {theme_data['background_color']}")
        print(f"   Sound Theme: {theme_data['sound_theme']}")
    
    print(f"\n🔄 Mix Mode: Auto-changes themes every 100 points")
    print(f"✨ Visual Effects: Particles, animations, transitions")

def demo_scoring():
    """Demonstrate scoring system."""
    print("\n\n🏆 Snake Odyssey: Scoring System Demo")
    print("=" * 50)
    
    score_manager = ScoreManager()
    
    # Simulate some scoring
    print("Simulating game progress:")
    
    for i in range(1, 16):
        score_manager.add_regular_food_score()
        if score_manager.should_spawn_bonus():
            score_manager.add_bonus_food_score()
            print(f"  🌟 Bonus food spawned and eaten! (Food #{i})")
        else:
            print(f"  🍎 Regular food eaten (Food #{i})")
            
        current_score = score_manager.get_current_score()
        level = score_manager.get_difficulty_level()
        speed = score_manager.get_speed_multiplier()
        
        if level > 0:
            print(f"     Score: {current_score} | Level: {level} | Speed: {speed:.1f}x")
            
    print(f"\nFinal Statistics:")
    stats = score_manager.get_score_statistics()
    print(f"  Final Score: {stats['score']}")
    print(f"  Food Eaten: {stats['food_eaten']}")
    print(f"  Bonus Food: {stats['bonus_eaten']}")
    print(f"  Difficulty Level: {stats['difficulty']}")
    print(f"  Rank: {score_manager.get_rank_title(stats['score'])}")
    
    if score_manager.should_add_obstacles():
        obstacle_count = score_manager.get_obstacle_count()
        print(f"  Obstacles: {obstacle_count} would be spawned")

def demo_architecture():
    """Demonstrate modular architecture."""
    print("\n\n🏗️ Snake Odyssey: Architecture Overview")
    print("=" * 50)
    
    components = {
        "GameManager": "Main game controller, coordinates all systems",
        "ThemeManager": "Handles visual themes, effects, and transitions",
        "ScoreManager": "Manages scoring, high scores, and progression",
        "UIManager": "Handles menus, HUD, and user interface",
        "Snake": "Snake entity with movement and collision logic",
        "Food": "Food system with regular and bonus mechanics"
    }
    
    print("🔧 Core Components:")
    for component, description in components.items():
        print(f"  • {component}: {description}")
    
    features = [
        "60 FPS smooth gameplay",
        "Particle effects and animations", 
        "Progressive difficulty scaling",
        "High score persistence (JSON)",
        "Configurable theme system",
        "Modular, extensible design"
    ]
    
    print(f"\n✨ Key Features:")
    for feature in features:
        print(f"  • {feature}")
    
    print(f"\n📁 Project Structure:")
    print(f"  • main.py - Entry point")
    print(f"  • src/config.py - Game configuration")
    print(f"  • src/components/ - Game entities")
    print(f"  • src/managers/ - System managers")
    print(f"  • data/ - Persistent storage")
    print(f"  • assets/ - Game assets (expandable)")

def main():
    """Run the demo."""
    print("🐍 Snake Odyssey: Themed Evolution")
    print("🎮 Modern Snake Game with Dynamic Themes")
    print("=" * 60)
    
    demo_themes()
    demo_scoring()
    demo_architecture()
    
    print("\n\n🚀 Ready to Play!")
    print("Run 'python main.py' to start the game")
    print("=" * 60)

if __name__ == "__main__":
    main()