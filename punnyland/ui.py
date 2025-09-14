"""
Whimsical UI elements for Punnyland CLI
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
import random
from typing import Optional

console = Console()

# ASCII Art for Dad Character
DAD_ASCII = r"""
    ╭─────╮
   ╰─╭─╭─╰╮
     ╰─╯   │ 👓
     ╭───╮ │
    ╱     ╲│
   ╱  \_/  ╲
  ╱         ╲
 ╱    ___    ╲
╱             ╲
│  Dad Joke   │
│   Master    │
╰─────────────╯
"""

MINI_DAD = r"""
  👨‍👔
 ╱─╲│╱─╲
╱   👓   ╲
│  \_/   │
╰───────╯
"""

# Corniness level visual indicators
CORN_LEVELS = {
    1: "🌱 Mild Chuckle",
    2: "🌽 Dad Approved",
    3: "🌽🌽 Eye Roll Guaranteed",
    4: "🌽🌽🌽 Groan Zone",
    5: "🌽🌽🌽🌽🌽 ULTRA CORN"
}

# Dad phrases for different occasions
DAD_GREETINGS = [
    "Well hello there, kiddo!",
    "Hey sport! Ready for some quality dad humor?",
    "Howdy partner! Time to get punny!",
    "Well well well, look who's here for some jokes!",
    "Ahoy there! Welcome to the pun zone!",
    "Hey there, champ! Let's make some memories!",
    "Well if it isn't my favorite audience!",
    "Greetings, earthling! Prepare for dad-level comedy!"
]

DAD_ENCOURAGEMENTS = [
    "That one really tickled my funny bone! 🦴",
    "Oof! That joke hit different! 💥",
    "Now that's what I call peak dad humor! 👨‍👔",
    "Classic! *chef's kiss* 👨‍🍳💋",
    "That joke was corn-y good! 🌽",
    "I'm stealing that one for the dad vault! 🏦",
    "Pure comedy gold right there! ⭐",
    "That's going in my greatest hits! 🎵"
]

DAD_RESPONSES = [
    "I told that joke to your mother... she rolled her eyes! 👀",
    "That reminds me of when I was your age...",
    "You know what they say... *dad wisdom incoming*",
    "I've got a million of these! Well, maybe 200+... 🤔",
    "That joke has been in the family for generations!",
    "Your old man's still got it! 😎",
    "I should write a book... 'Dad Jokes Volume 1'!"
]

def show_welcome_banner():
    """Display the main welcome banner"""
    title = Text("🎭 WELCOME TO PUNNYLAND 🎭", style="bold magenta")
    subtitle = Text("Where Dad Jokes Come to Life!", style="italic cyan")

    welcome_text = Align.center(Text.assemble(
        title, "\n",
        subtitle, "\n\n",
        Text(DAD_ASCII, style="yellow"),
        "\n",
        Text("Ready to groan with delight? Let's get punny! 🤪", style="bold green")
    ))

    console.print(Panel(
        welcome_text,
        box=box.DOUBLE,
        border_style="bright_yellow",
        padding=(1, 2)
    ))

def show_joke_with_dad(joke_text: str, corniness: int, user_name: Optional[str] = None):
    """Display a joke with the dad character"""
    name_part = f" {user_name}" if user_name else ""
    corn_level = CORN_LEVELS.get(corniness, "🌽 Unknown Level")

    # Dad saying the joke
    dad_speech = Text.assemble(
        Text(f"Hey{name_part}! Here's a good one:\n\n", style="bold blue"),
        Text(f'"{joke_text}"\n\n', style="white on blue", justify="center"),
        Text(f"Corniness Level: {corn_level}", style="yellow")
    )

    # Combine dad ASCII with speech
    content = Align.center(Text.assemble(
        Text(MINI_DAD, style="yellow"), "\n",
        dad_speech, "\n",
        Text(random.choice(DAD_ENCOURAGEMENTS), style="italic green")
    ))

    console.print(Panel(
        content,
        title="🎤 Dad's Corner 🎤",
        box=box.ROUNDED,
        border_style="cyan",
        padding=(1, 2)
    ))

def show_corniness_scale():
    """Display the corniness scale explanation"""
    scale_text = Text()

    for level, description in CORN_LEVELS.items():
        color = ["green", "yellow", "orange3", "red", "bright_red"][level-1]
        scale_text.append(f"{level}. {description}\n", style=f"bold {color}")

    console.print(Panel(
        Align.center(Text.assemble(
            Text("🌽 CORNINESS SCALE 🌽\n\n", style="bold yellow"),
            scale_text,
            Text("\nChoose your corn level wisely! 🤔", style="italic cyan")
        )),
        title="📊 How Corny Do You Want It? 📊",
        box=box.HEAVY,
        border_style="yellow"
    ))

def show_dad_greeting(user_name: Optional[str] = None):
    """Show a personalized dad greeting"""
    name_part = f" {user_name}" if user_name else ""
    greeting = random.choice(DAD_GREETINGS).replace("kiddo", user_name or "kiddo")

    content = Align.center(Text.assemble(
        Text(MINI_DAD, style="yellow"), "\n",
        Text(f"{greeting}{name_part}", style="bold blue"), "\n",
        Text(random.choice(DAD_RESPONSES), style="italic green")
    ))

    console.print(Panel(
        content,
        box=box.ROUNDED,
        border_style="bright_blue"
    ))

def show_settings_panel(user_name: str, corniness: int, total_jokes_heard: int):
    """Display user settings in a nice panel"""
    settings_text = Text.assemble(
        Text(f"👤 Name: ", style="bold cyan"),
        Text(f"{user_name}\n", style="white"),
        Text(f"🌽 Corniness Level: ", style="bold cyan"),
        Text(f"{corniness} - {CORN_LEVELS[corniness]}\n", style="yellow"),
        Text(f"😂 Total Jokes Heard: ", style="bold cyan"),
        Text(f"{total_jokes_heard}\n", style="white"),
        Text(f"🏆 Status: ", style="bold cyan"),
        Text(_get_status_title(total_jokes_heard), style="gold1")
    )

    console.print(Panel(
        Align.center(settings_text),
        title="⚙️  Your Punnyland Profile ⚙️",
        box=box.DOUBLE,
        border_style="bright_cyan"
    ))

def show_error(message: str):
    """Display error message in dad style"""
    console.print(Panel(
        Align.center(Text.assemble(
            Text("🤦‍♂️ Oops! Dad made a mistake...\n\n", style="bold red"),
            Text(message, style="white"),
            Text("\n\nTry again, sport!", style="italic yellow")
        )),
        title="🚫 Dad Error 🚫",
        box=box.HEAVY,
        border_style="red"
    ))

def show_goodbye(user_name: Optional[str] = None):
    """Show a dad-style goodbye"""
    name_part = f" {user_name}" if user_name else ""

    goodbyes = [
        f"See you later, alligator{name_part}! 🐊",
        f"Catch you on the flip side{name_part}! 🔄",
        f"Don't be a stranger{name_part}! Come back for more groans! 😄",
        f"Remember{name_part}: I'm not just your dad joke dealer, I'm also your friend! 👨‍👔",
        f"Until next time{name_part}... stay punny! 🎭"
    ]

    console.print(Panel(
        Align.center(Text.assemble(
            Text(DAD_ASCII, style="yellow"), "\n",
            Text(random.choice(goodbyes), style="bold blue"), "\n",
            Text("Thanks for letting me share my jokes with you! 🤗", style="italic green")
        )),
        title="👋 Thanks for Visiting Punnyland! 👋",
        box=box.DOUBLE,
        border_style="bright_yellow"
    ))

def _get_status_title(joke_count: int) -> str:
    """Get status title based on jokes heard"""
    if joke_count < 5:
        return "🌱 Pun Rookie"
    elif joke_count < 15:
        return "🌽 Corn Enthusiast"
    elif joke_count < 30:
        return "😂 Joke Collector"
    elif joke_count < 50:
        return "🎭 Pun Master"
    elif joke_count < 100:
        return "👑 Dad Joke Royalty"
    else:
        return "🏆 Ultimate Corn Legend"

# Animation helpers
def print_with_dad_pause(text: str, style: str = "white"):
    """Print text with a dad-like pause for dramatic effect"""
    console.print(text, style=style)
    import time
    time.sleep(0.8)  # Dad pause for effect

def typewriter_effect(text: str, delay: float = 0.03):
    """Create a typewriter effect for special messages"""
    import time
    for char in text:
        console.print(char, end="", style="bold green")
        time.sleep(delay)
    console.print()  # New line at the end