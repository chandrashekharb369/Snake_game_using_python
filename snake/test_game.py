"""
Quick test script to verify all components work correctly
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules import correctly."""
    try:
        from managers.game_manager import GameManager
        from managers.theme_manager import ThemeManager
        from managers.score_manager import ScoreManager
        from managers.ui_manager import UIManager
        from components.snake import Snake
        from components.food import Food
        from config import THEMES, SCREEN_WIDTH, SCREEN_HEIGHT
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_components():
    """Test component initialization."""
    try:
        import pygame
        pygame.init()  # Initialize pygame for font support
        
        from managers.theme_manager import ThemeManager
        from managers.score_manager import ScoreManager
        from managers.ui_manager import UIManager
        from components.snake import Snake
        from components.food import Food
        
        # Test theme manager
        theme_mgr = ThemeManager()
        themes = theme_mgr.get_theme_list()
        assert len(themes) == 5, f"Expected 5 themes, got {len(themes)}"
        
        # Test score manager
        score_mgr = ScoreManager()
        score_mgr.add_regular_food_score()
        assert score_mgr.get_current_score() == 10, "Score should be 10"
        
        # Test UI manager
        ui_mgr = UIManager()
        assert ui_mgr.current_menu == 'main', "Should start with main menu"
        
        # Test snake
        snake = Snake(10, 10, (0, 255, 0))
        assert len(snake.body) == 1, "Snake should start with 1 segment"
        
        # Test food
        food = Food(800, 600)
        assert food.regular_food is None, "Food should start unspawned"
        
        print("✅ All components initialize correctly")
        return True
    except Exception as e:
        print(f"❌ Component test error: {e}")
        return False

def test_game_logic():
    """Test basic game logic."""
    try:
        from managers.score_manager import ScoreManager
        from components.snake import Snake
        from config import DIRECTIONS
        
        # Test scoring progression
        score_mgr = ScoreManager()
        for i in range(15):
            score_mgr.add_regular_food_score()
            if score_mgr.should_spawn_bonus():
                score_mgr.add_bonus_food_score()
        
        assert score_mgr.get_current_score() > 100, "Score should increase with food"
        assert score_mgr.get_difficulty_level() >= 1, "Difficulty should increase"
        
        # Test snake movement
        snake = Snake(5, 5, (0, 255, 0))
        initial_pos = snake.get_head_position()
        snake.move()
        new_pos = snake.get_head_position()
        assert new_pos != initial_pos, "Snake should move"
        
        # Test direction change
        snake.change_direction(DIRECTIONS['UP'])
        assert snake.direction == DIRECTIONS['UP'], "Direction should change"
        
        print("✅ Game logic works correctly")
        return True
    except Exception as e:
        print(f"❌ Game logic test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🐍 Snake Odyssey: Component Test Suite")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Component Initialization", test_components),
        ("Game Logic", test_game_logic)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Snake Odyssey is ready to play!")
        print("\n🚀 Run 'python main.py' to start the game")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)