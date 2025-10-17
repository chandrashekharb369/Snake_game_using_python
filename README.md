# Snake Odyssey: Themed Evolution

A modern, feature-rich Snake game with dynamic themes, progressive difficulty, and smooth animations.

## 🎮 Features

### Core Gameplay
- Classic Snake mechanics with modern enhancements
- Smooth movement and responsive controls (Arrow Keys or WASD)
- Progressive difficulty with increasing speed
- Dynamic obstacle spawning based on score

### Theme System
- **5 Unique Themes**: Forest, Sea, Snow, Desert, Hill
- **Mix Mode**: Automatic theme switching every 100 points
- Smooth theme transitions with visual effects
- Theme-specific colors, patterns, and visual elements

### Scoring & Progression
- Regular food: +10 points
- Bonus food: +20 points (appears every 10 regular foods for 9 seconds)
- High score tracking per theme
- Difficulty levels with speed increases
- Rank system (Snake Rookie to Snake Master)

### Visual Effects
- Particle effects for food consumption
- Animated backgrounds with theme-specific patterns
- Pulsing bonus food with timer
- Snake head with eyes and detailed body segments

### User Interface
- Modern menu system with theme selection
- High score leaderboard with statistics
- Game over screen with detailed stats
- Pause/Resume functionality
- Real-time HUD with score, level, and theme info

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game
```bash
python main.py
```

## 🎯 Controls

### Menu Navigation
- Mouse clicks for menu interaction
- ESC to quit from main menu

### Gameplay
- **Arrow Keys** or **WASD**: Move snake
- **P**: Pause/Resume game

## 🏗️ Architecture

The game uses a modular architecture for easy expansion:

### Core Components
- `Snake`: Handles snake entity logic and rendering
- `Food`: Manages regular and bonus food systems

### Manager Classes
- `GameManager`: Main game engine coordinating all systems
- `ThemeManager`: Handles theme switching and visual effects
- `ScoreManager`: Manages scoring, persistence, and progression
- `UIManager`: Handles all user interface elements

### Configuration
- `config.py`: Centralized game constants and theme definitions

## 🎨 Themes

### Forest Theme 🌲
- Green snake with leaf food
- Grass patterns and nature sounds
- Earth tones and organic feel

### Sea Theme 🌊
- Blue snake with shell food
- Animated wave patterns
- Ocean blues and aquatic atmosphere

### Snow Theme ❄️
- Light blue snake with snowflake food
- Falling snow animation
- Cool whites and icy textures

### Desert Theme 🏜️
- Brown snake with cactus food
- Sand dune patterns
- Warm earth tones

### Hill Theme ⛰️
- Purple snake with rock food
- Mountain silhouettes
- Mystical purple and gold colors

## 📊 Scoring System

- **Regular Food**: 10 points + snake growth
- **Bonus Food**: 20 points + snake growth (9-second timer)
- **Speed Increase**: Every 50 points
- **Obstacles**: Start appearing at 200 points
- **Difficulty Levels**: Every 100 points

## 🏆 Achievements

The game tracks various statistics:
- Total score
- Food eaten count
- Bonus food accuracy
- Difficulty level reached
- Personal best per theme

## 🔧 Technical Features

### Performance Optimizations
- Efficient collision detection
- Optimized rendering pipeline
- Particle system with alpha blending
- Smooth 60 FPS gameplay

### Data Persistence
- High scores saved locally in JSON format
- Theme preferences remembered
- Statistics tracking across sessions

### Extensibility
- Modular design for easy feature additions
- Theme system supports unlimited themes
- Configurable game parameters
- Ready for multiplayer expansion

## 🎵 Audio (Planned)
- Theme-specific background music
- Sound effects for food consumption
- Audio feedback for game events

## 🚀 Future Enhancements

### Planned Features
- Background music system
- Power-ups (Shield, Slow Motion)
- Two-player mode
- Online leaderboards
- Achievement system
- Custom theme creator

### Technical Improvements
- C/C++ modules for performance
- Web version using JavaScript
- Mobile touch controls
- Gamepad support

## 📁 Project Structure

```
snake/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── src/
│   ├── config.py          # Game configuration
│   ├── components/        # Game entities
│   │   ├── snake.py
│   │   └── food.py
│   └── managers/          # System managers
│       ├── game_manager.py
│       ├── theme_manager.py
│       ├── score_manager.py
│       └── ui_manager.py
├── assets/                # Game assets
│   ├── themes/
│   ├── sounds/
│   └── icons/
└── data/                  # Saved data
    └── high_scores.json
```



## 📜 Note

This project is created for educational , demonstrating advanced Python game development with pygame.

---

**Snake Odyssey: Themed Evolution** - Where classic gameplay meets modern design! 🐍✨
