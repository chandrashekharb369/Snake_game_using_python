"""
Score Manager for Snake Odyssey.
Handles scoring, high scores, and persistence.
"""

import json
import os
from datetime import datetime
from config import DATA_DIR, SCORES_FILE

class ScoreManager:
    """Manages game scoring and high score persistence."""
    
    def __init__(self):
        """Initialize score manager."""
        self.current_score = 0
        self.food_eaten = 0
        self.bonus_food_eaten = 0
        self.high_scores = self.load_high_scores()
        
    def reset_score(self):
        """Reset current game score."""
        self.current_score = 0
        self.food_eaten = 0
        self.bonus_food_eaten = 0
        
    def add_regular_food_score(self, points=10):
        """Add points for regular food."""
        self.current_score += points
        self.food_eaten += 1
        
    def add_bonus_food_score(self, points=20):
        """Add points for bonus food."""
        self.current_score += points
        self.bonus_food_eaten += 1
        
    def get_current_score(self):
        """Get current game score."""
        return self.current_score
        
    def get_food_count(self):
        """Get total food eaten."""
        return self.food_eaten
        
    def get_bonus_count(self):
        """Get bonus food eaten."""
        return self.bonus_food_eaten
        
    def should_spawn_bonus(self):
        """Check if bonus food should spawn."""
        return self.food_eaten > 0 and self.food_eaten % 10 == 0
        
    def get_difficulty_level(self):
        """Get current difficulty level based on score."""
        return self.current_score // 100
        
    def get_speed_multiplier(self):
        """Get speed multiplier based on score."""
        return 1.0 + (self.current_score // 50) * 0.1
        
    def should_add_obstacles(self):
        """Check if obstacles should be added."""
        return self.current_score >= 200
        
    def get_obstacle_count(self):
        """Get number of obstacles to spawn."""
        if not self.should_add_obstacles():
            return 0
        return min(10, (self.current_score - 200) // 100 + 1)
        
    def save_high_score(self, theme, player_name="Player"):
        """Save high score for theme."""
        if theme not in self.high_scores:
            self.high_scores[theme] = []
            
        score_entry = {
            'score': self.current_score,
            'player': player_name,
            'date': datetime.now().isoformat(),
            'food_eaten': self.food_eaten,
            'bonus_eaten': self.bonus_food_eaten
        }
        
        self.high_scores[theme].append(score_entry)
        
        # Sort and keep top 10
        self.high_scores[theme].sort(key=lambda x: x['score'], reverse=True)
        self.high_scores[theme] = self.high_scores[theme][:10]
        
        self.save_high_scores()
        
    def is_high_score(self, theme):
        """Check if current score is a high score."""
        if theme not in self.high_scores or len(self.high_scores[theme]) < 10:
            return True
            
        lowest_high_score = self.high_scores[theme][-1]['score']
        return self.current_score > lowest_high_score
        
    def get_high_scores(self, theme=None):
        """Get high scores for theme or all themes."""
        if theme:
            return self.high_scores.get(theme, [])
        return self.high_scores
        
    def get_best_score(self, theme):
        """Get best score for theme."""
        scores = self.get_high_scores(theme)
        return scores[0]['score'] if scores else 0
        
    def load_high_scores(self):
        """Load high scores from file."""
        try:
            # Ensure data directory exists
            os.makedirs(DATA_DIR, exist_ok=True)
            
            scores_path = os.path.join(DATA_DIR, SCORES_FILE)
            if os.path.exists(scores_path):
                with open(scores_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading high scores: {e}")
            
        return {}
        
    def save_high_scores(self):
        """Save high scores to file."""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            scores_path = os.path.join(DATA_DIR, SCORES_FILE)
            
            with open(scores_path, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")
            
    def get_score_statistics(self):
        """Get scoring statistics for current game."""
        stats = {
            'score': self.current_score,
            'food_eaten': self.food_eaten,
            'bonus_eaten': self.bonus_food_eaten,
            'accuracy': 0,
            'difficulty': self.get_difficulty_level()
        }
        
        total_food_spawned = self.food_eaten + self.bonus_food_eaten
        if total_food_spawned > 0:
            stats['accuracy'] = (self.bonus_food_eaten / 
                               max(1, self.food_eaten // 10)) * 100
            
        return stats
        
    def format_score(self, score):
        """Format score with proper spacing."""
        return f"{score:,}"
        
    def get_rank_title(self, score):
        """Get rank title based on score."""
        if score >= 1000:
            return "Snake Master"
        elif score >= 500:
            return "Snake Expert"
        elif score >= 250:
            return "Snake Warrior"
        elif score >= 100:
            return "Snake Hunter"
        else:
            return "Snake Rookie"