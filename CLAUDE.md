# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Punnyland** is a whimsical CLI application for dad jokes with personality! This Python-based command-line tool delivers categorized dad jokes with a conversational interface and user personalization features.

### Key Features
- 200+ dad jokes categorized by corniness level (1-5)
- User personalization with names and preferences
- Conversational interface with ASCII art and colorful displays
- Joke favorites, history tracking, and achievements system
- Daily joke feature and interactive mode
- Joke search functionality

## Technology Stack

- **Language**: Python 3.7+
- **CLI Framework**: Click
- **UI/Display**: Rich (for colorful console output)
- **Data Storage**: JSON files for jokes and user preferences
- **Dependencies**: click, colorama, rich

## Development Commands

### Installation and Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run the application
punnyland
```

### Main Commands
```bash
punnyland joke           # Get a random joke at user's preferred level
punnyland joke --level 3 # Get joke at specific corniness level (1-5)
punnyland daily          # Get today's special joke
punnyland random         # Completely random joke from any level
punnyland favorites      # View and manage favorite jokes
punnyland settings       # Modify user preferences
punnyland stats          # View user statistics
punnyland search "term"  # Search jokes containing specific words
punnyland interactive    # Enter conversation mode
```

## Project Architecture

### Core Components

1. **`cli.py`** - Main Click-based CLI interface and command handlers
2. **`jokes.py`** - Joke management system with `JokeManager` and `JokeDelivery` classes
3. **`user.py`** - User profile management with `UserProfile` class for preferences and history
4. **`ui.py`** - Whimsical UI elements, ASCII art, and Rich-based displays
5. **`data/jokes.json`** - Joke database with 200+ jokes organized by corniness levels

### Data Flow
1. User runs command → CLI handler in `cli.py`
2. CLI creates joke package using `JokeDelivery` and `JokeManager`
3. UI displays joke with dad character using `ui.py` functions
4. User interaction tracked in `UserProfile` (history, favorites, achievements)

### Corniness Scale System
- **Level 1**: Mild Chuckle - Subtle wordplay, almost respectable
- **Level 2**: Dad Approved - Classic dad territory
- **Level 3**: Eye Roll Guaranteed - Peak dad joke territory (default)
- **Level 4**: Groan Zone - Painfully punny
- **Level 5**: Ultra Corn - So bad they're good again

### File Structure
```
punnyland/
├── __init__.py          # Package initialization
├── cli.py               # Main CLI interface and commands
├── jokes.py             # Joke management and delivery logic
├── user.py              # User profile and preferences
├── ui.py                # Whimsical UI elements and displays
└── data/
    └── jokes.json       # Joke database (200+ jokes by level)
```

### User Data Storage
- Config directory: `~/.punnyland/`
- User preferences, joke history, and favorites stored in `user_data.json`
- Automatic achievement tracking and statistics

## Development Guidelines

### Adding New Jokes
- Edit `punnyland/data/jokes.json`
- Maintain balance across corniness levels (1-5)
- Follow existing joke quality and length patterns

### UI Consistency
- Use Rich console for all output
- Follow established ASCII art and color schemes
- Maintain dad character personality across all interactions

### User Experience
- Always provide helpful error messages in dad-style humor
- Maintain conversational tone throughout the application
- Ensure commands are intuitive and well-documented

### Testing Approach
- Test CLI commands manually: `punnyland joke --level 3`
- Verify joke database integrity and variety
- Test user preference persistence across sessions
- Validate ASCII art displays correctly in different terminals

## Notes

- The application uses Rich for enhanced terminal output - ensure terminal supports colors
- User data is stored locally in home directory (cross-platform compatible)
- Joke database can be extended by adding to the JSON structure
- Achievement system automatically unlocks based on usage patterns