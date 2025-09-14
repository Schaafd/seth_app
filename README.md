# 🎭 Punnyland - Where Dad Jokes Come to Life! 🎭

Welcome to **Punnyland**, the most pun-derful command-line experience you'll ever have! This isn't just another joke app—it's a full-blown dad joke ecosystem with personality, style, and enough groan-worthy content to make your eyes roll into next week.

## 🌽 What's All the Fuss About?

Punnyland delivers **455+ carefully curated dad jokes** across 5 levels of corniness, each with their own sophisticated ASCII dad character to match your mood. Whether you prefer mild chuckles or want to dive deep into the groan zone, we've got you covered.

### The Corniness Scale™
- **Level 1** 🌱 *Mild Chuckle* - Subtle wordplay that's almost respectable
- **Level 2** 🌽 *Dad Approved* - Classic dad territory with solid puns  
- **Level 3** 🌽🌽 *Eye Roll Guaranteed* - Peak dad joke territory (default)
- **Level 4** 🌽🌽🌽 *Groan Zone* - Painfully punny with layered wordplay
- **Level 5** 🌽🌽🌽🌽🌽 *Ultra Corn* - So bad they're good again

## 🚀 Quick Start (No Time to Joke Around)

### Installation

```bash
# Clone this repository
git clone https://github.com/Schaafd/seth_app.git
cd seth_app

# Install dependencies with uv (our preferred tool)
uv sync

# Run your first joke!
uv run punnyland joke
```

*Don't have `uv`? No problem! You can also use traditional pip installation, but we highly recommend `uv` for the best experience.*

### First Run Experience

The first time you run Punnyland, you'll meet our dad joke master who will help you set up your preferences. Don't worry—he won't dad-shame you for your corniness choices!

## 🎮 Command Line Interface

### Core Commands

#### `punnyland joke [OPTIONS]`
Get a dad joke tailored to your taste!

```bash
# Get a joke at your preferred corniness level
punnyland joke

# Specify a particular level (1-5)
punnyland joke --level 4

# Short form works too
punnyland joke -l 2
```

#### `punnyland random`
Feeling adventurous? Roll the dad joke dice! 🎲

```bash
punnyland random
```
*Perfect for when you can't decide how corny you want to get.*

#### `punnyland daily`
Your daily dose of dad humor ⭐

```bash
punnyland daily
```
*New joke every day—because variety is the spice of life (and puns are the seasoning).*

#### `punnyland interactive`
Enter conversation mode for continuous dad joke bliss! 🎭

```bash
punnyland interactive
```
*Keep the jokes rolling until you say "quit"—it's like having a dad joke buddy who never runs out of material.*

### Personalization Commands

#### `punnyland settings`
Modify your Punnyland preferences ⚙️

```bash
punnyland settings
```

#### `punnyland stats`
View your joke consumption statistics 📊

```bash
punnyland stats
```

#### `punnyland favorites`
Manage your favorite jokes collection ⭐

```bash
punnyland favorites
```

#### `punnyland search`
Find jokes containing specific words 🔍

```bash
punnyland search "fish"
punnyland search "banana"
```

### Getting Help

```bash
# See all available commands
punnyland --help

# Get help for a specific command
punnyland joke --help
```

## 🎨 Meet Your Dad Characters

Our sophisticated ASCII art system features different dad personalities that match your joke's corniness level:

- **👨‍🏫 Wise Dad** - For those refined Level 1 moments
- **👨‍💼 Classic Dad** - The timeless joke master
- **😎 Cool Dad** - Hip and happening with his guitar
- **😤 Grumpy Dad** - For when the corn levels get serious

*Each character brings their own personality to your joke experience—because presentation is everything in the pun business.*

## 🏠 Your Personal Punnyland

Punnyland creates a cozy home directory at `~/.punnyland/` where it stores:
- Your corniness level preferences  
- Joke history and favorites
- Achievement tracking
- Daily joke status

*Don't worry, we only store the good stuff—no dad joke shaming allowed.*

## 🛠️ Technical Specifications

### Requirements
- **Python**: 3.10+ (because modern dads need modern Python)
- **Dependencies**: Click, Rich, Colorama
- **Terminal**: Any terminal that supports Unicode and colors
- **Sense of Humor**: Optional but highly recommended

### Development

This project uses:
- **uv** for dependency management
- **Click** for the CLI framework
- **Rich** for beautiful terminal output
- **Sophisticated ASCII art** for character personalities

## 🎯 Pro Tips for Maximum Enjoyment

1. **Start with Level 3** - It's the sweet spot of dad joke perfection
2. **Try Interactive Mode** - Great for family entertainment
3. **Use Daily Jokes** - Build a routine around dad humor
4. **Explore All Levels** - Each has its own charm
5. **Add Favorites** - Build your personal collection of groan-worthy gems

## 🤝 Contributing

Found a joke that's so bad it's good? Have suggestions for new features? We'd love to hear from you! Just remember—all contributions should maintain our high standards of dad joke quality.

## 📜 License

This project is licensed under the "Make People Groan" license—use it freely, but you must promise to share at least one dad joke per week with someone you care about.

## 🎊 Final Words

Remember, life's too short for bad jokes... which is exactly why we specialize in dad jokes! They're not bad—they're *so good they hurt*.

Now stop reading and start groaning! 

```bash
uv run punnyland joke
```

---

*Made with ❤️ and an unhealthy amount of puns*

> **Dad Joke Fact**: Did you know that dad jokes are like fine wine? They get better with age... and worse at the same time! 🍷