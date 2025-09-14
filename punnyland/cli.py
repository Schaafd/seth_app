"""
Main CLI interface for Punnyland - A whimsical dad jokes CLI
"""

import click
import random as rand_module
import time
from typing import Optional

from .user import UserProfile
from .jokes import JokeManager, JokeDelivery
from .ui import (
    console, show_welcome_banner, show_joke_with_dad, show_corniness_scale,
    show_dad_greeting, show_settings_panel, show_error, show_goodbye,
    print_with_dad_pause, typewriter_effect
)

# Global instances
user_profile = UserProfile()
joke_manager = JokeManager()
joke_delivery = JokeDelivery(joke_manager)

def check_first_time_setup():
    """Check if user needs to complete initial setup"""
    if not user_profile.is_setup_completed():
        run_initial_setup()

def run_initial_setup():
    """Run the initial user setup process"""
    show_welcome_banner()
    time.sleep(1)

    console.print("\n🎭 Welcome to Punnyland! Let's get you set up with some premium dad humor! 🎭\n")

    # Get user name
    while True:
        name = click.prompt("What should I call you, sport?", type=str).strip()
        if name:
            break
        console.print("Come on, don't be shy! What's your name?")

    console.print(f"\nNice to meet you, {name}! 👋")
    time.sleep(0.5)

    # Show corniness scale
    console.print("\nNow, let's talk about your humor preferences...")
    show_corniness_scale()

    # Get corniness preference
    while True:
        try:
            corniness = click.prompt(
                f"\nWhat's your preferred corniness level, {name}? (1-5)",
                type=int
            )
            if 1 <= corniness <= 5:
                break
            console.print("Please pick a number between 1 and 5, champ!")
        except:
            console.print("Just enter a number between 1 and 5!")

    # Complete setup
    user_profile.complete_setup(name, corniness)

    # Celebration
    console.print(f"\n🎉 Fantastic! Welcome to Punnyland, {name}! 🎉")
    time.sleep(0.5)

    console.print(f"You're all set up with corniness level {corniness}!")
    console.print("Let me tell you your first joke to get things started...\n")
    time.sleep(1)

    # Tell first joke
    tell_joke_command(None)

@click.group()
@click.version_option(version="1.0.0", prog_name="punnyland")
def main():
    """🎭 Punnyland - Where Dad Jokes Come to Life! 🎭"""
    check_first_time_setup()

@main.command()
@click.option('--level', '-l', type=int, help='Specific corniness level (1-5)')
def joke(level):
    """Get a dad joke! 😄"""
    tell_joke_command(level)

def tell_joke_command(level: Optional[int]):
    """Internal function to handle joke telling"""
    user_name = user_profile.get_name()
    user_corniness = user_profile.get_corniness_level()

    # Use specified level or user's preferred level
    corniness_level = level if level is not None else user_corniness

    if not joke_manager.validate_corniness_level(corniness_level):
        show_error(f"Corniness level must be between 1 and 5! Your default is {user_corniness}.")
        return

    # Get recent jokes to avoid repeats
    recent_jokes = user_profile.get_recent_jokes(10)

    # Create joke package
    joke_package = joke_delivery.create_joke_package(
        corniness_level, user_name, recent_jokes
    )

    if not joke_package:
        show_error("Oops! I'm all out of jokes at that level. Try a different corniness level!")
        return

    # Show dad greeting occasionally
    if rand_module.random() < 0.3:  # 30% chance
        show_dad_greeting(user_name, corniness_level)
        time.sleep(1)

    # Display the joke
    show_joke_with_dad(
        joke_package['joke'],
        joke_package['corniness_level'],
        user_name
    )

    # Add to user history
    user_profile.add_joke_to_history(
        joke_package['joke'],
        joke_package['corniness_level']
    )

    # Show dad fact occasionally
    if joke_package.get('dad_fact'):
        time.sleep(1)
        console.print(f"\n💡 {joke_package['dad_fact']}")

    # Prompt for feedback
    time.sleep(1)
    console.print("\n" + "="*50)
    console.print("Did that make you groan? (That's the goal!) 😏")

    # Ask if they want to add to favorites
    if click.confirm("\n⭐ Add this joke to your favorites?"):
        if user_profile.add_to_favorites(joke_package['joke'], joke_package['corniness_level']):
            console.print("🎉 Added to your favorites! Great choice!")
            user_profile.increment_groan_counter()
        else:
            console.print("📝 That joke is already in your favorites!")

@main.command()
def daily():
    """Get today's special joke of the day! ⭐"""
    if not user_profile.get_daily_joke_eligible():
        console.print("🌅 You've already heard today's joke! Come back tomorrow for a fresh one! 🌟")
        return

    user_name = user_profile.get_name()
    user_corniness = user_profile.get_corniness_level()

    # Create daily joke package
    joke_package = joke_delivery.create_daily_joke_package(user_corniness, user_name)

    if not joke_package:
        show_error("Sorry! There seems to be a problem with today's joke. Try a regular joke instead!")
        return

    # Show daily intro
    console.print(f"\n{joke_package['daily_intro']}\n")
    time.sleep(1)

    # Show the joke
    show_joke_with_dad(
        joke_package['joke'],
        joke_package['corniness_level'],
        user_name
    )

    # Mark as seen
    user_profile.mark_daily_joke_seen()
    user_profile.add_joke_to_history(
        joke_package['joke'],
        joke_package['corniness_level']
    )

    console.print(f"\n✨ {joke_package['special_note']} ✨")

@main.command()
def random():
    """Get a completely random joke from any corniness level! 🎲"""
    user_name = user_profile.get_name()
    recent_jokes = user_profile.get_recent_jokes(15)

    # Get random joke
    joke_text, corniness_level = joke_manager.get_random_joke(recent_jokes)

    if not joke_text:
        show_error("Oops! No jokes available right now. That's... not very funny.")
        return

    console.print("🎲 Rolling the dad joke dice... 🎲\n")
    time.sleep(1)

    show_joke_with_dad(joke_text, corniness_level, user_name)

    user_profile.add_joke_to_history(joke_text, corniness_level)

@main.command()
def settings():
    """View and modify your Punnyland settings ⚙️"""
    while True:
        stats = user_profile.get_stats()
        show_settings_panel(
            stats['name'],
            stats['corniness_level'],
            stats['total_jokes']
        )

        console.print("\nWhat would you like to do?")
        console.print("1. Change corniness level")
        console.print("2. View achievements")
        console.print("3. Export favorites")
        console.print("4. Back to main menu")

        choice = click.prompt("Enter your choice (1-4)", type=int, default=4)

        if choice == 1:
            show_corniness_scale()
            new_level = click.prompt("New corniness level (1-5)", type=int)
            if user_profile.set_corniness_level(new_level):
                console.print(f"✅ Corniness level updated to {new_level}!")
            else:
                console.print("❌ Please enter a level between 1 and 5!")

        elif choice == 2:
            achievements = user_profile.get_achievements()
            console.print("\n🏆 Your Achievements 🏆")
            if achievements:
                for i, achievement in enumerate(achievements, 1):
                    console.print(f"{i}. {achievement}")
            else:
                console.print("No achievements yet! Keep listening to jokes!")

        elif choice == 3:
            try:
                filename = user_profile.export_favorites()
                console.print(f"✅ Favorites exported to: {filename}")
            except Exception as e:
                console.print(f"❌ Export failed: {e}")

        elif choice == 4:
            break

        console.print("\nPress Enter to continue...")
        input()

@main.command()
def favorites():
    """View and manage your favorite jokes! ⭐"""
    favs = user_profile.get_favorites()

    if not favs:
        console.print("📝 No favorite jokes yet! Use 'punnyland joke' and add some to your collection! 🌟")
        return

    console.print("⭐ Your Favorite Dad Jokes ⭐\n")

    for i, fav in enumerate(favs, 1):
        console.print(f"{i}. {fav['joke']}")
        console.print(f"   Corniness: {joke_manager.get_corniness_description(fav['corniness'])}")
        console.print(f"   Added: {fav['added_date'][:10]}\n")

    if click.confirm("Would you like to remove any favorites?"):
        try:
            index = click.prompt("Which joke number to remove?", type=int) - 1
            if 0 <= index < len(favs):
                joke_to_remove = favs[index]['joke']
                if user_profile.remove_from_favorites(joke_to_remove):
                    console.print("✅ Joke removed from favorites!")
                else:
                    console.print("❌ Could not remove joke!")
            else:
                console.print("❌ Invalid joke number!")
        except:
            console.print("❌ Please enter a valid number!")

@main.command()
def stats():
    """View your Punnyland statistics 📊"""
    stats = user_profile.get_stats()
    joke_stats = joke_manager.get_joke_stats()

    console.print("📊 Your Punnyland Statistics 📊\n")
    console.print(f"👤 Name: {stats['name']}")
    console.print(f"🌽 Corniness Level: {stats['corniness_level']}")
    console.print(f"😂 Total Jokes Heard: {stats['total_jokes']}")
    console.print(f"⭐ Favorite Jokes: {stats['favorites_count']}")
    console.print(f"🤦‍♂️ Total Groans: {stats['groan_count']}")
    console.print(f"🏆 Achievements: {stats['achievements_count']}")
    console.print(f"📅 Member Since: {stats['member_since']}")

    console.print(f"\n🗃️  Database Info:")
    console.print(f"📚 Total Jokes Available: {joke_stats['total_jokes']}")
    console.print(f"🌽 Jokes Per Level: {joke_stats['jokes_per_level']}")

@main.command()
@click.argument('search_term')
@click.option('--level', '-l', type=int, help='Search only in specific corniness level')
def search(search_term, level):
    """Search for jokes containing specific words 🔍"""
    results = joke_manager.search_jokes(search_term, level)

    if not results:
        console.print(f"😕 No jokes found containing '{search_term}'.")
        console.print("Try a different search term or check a different corniness level!")
        return

    console.print(f"🔍 Found {len(results)} joke(s) containing '{search_term}':\n")

    for i, (joke, joke_level) in enumerate(results, 1):
        console.print(f"{i}. {joke}")
        console.print(f"   Level: {joke_manager.get_corniness_description(joke_level)}\n")

@main.command()
def interactive():
    """Start an interactive dad joke session! 🎭"""
    user_name = user_profile.get_name()
    show_dad_greeting(user_name)

    console.print("🎭 Welcome to Interactive Dad Mode! 🎭")
    console.print("I'll keep telling jokes until you say 'quit' or 'exit'!")
    console.print("You can also say 'level X' to change corniness level!")
    console.print("="*60 + "\n")

    current_level = user_profile.get_corniness_level()
    recent_jokes = []

    while True:
        # Tell a joke
        joke_package = joke_delivery.create_joke_package(
            current_level, user_name, recent_jokes
        )

        if joke_package:
            show_joke_with_dad(
                joke_package['joke'],
                joke_package['corniness_level'],
                user_name
            )
            recent_jokes.append(joke_package['joke'])
            user_profile.add_joke_to_history(
                joke_package['joke'],
                joke_package['corniness_level']
            )

        # Get user input
        console.print("\n" + "="*50)
        user_input = input("Press Enter for another joke, or type a command: ").strip().lower()

        if user_input in ['quit', 'exit', 'bye', 'goodbye']:
            break
        elif user_input.startswith('level '):
            try:
                new_level = int(user_input.split()[1])
                if joke_manager.validate_corniness_level(new_level):
                    current_level = new_level
                    console.print(f"🌽 Switched to corniness level {new_level}!")
                else:
                    console.print("❌ Level must be 1-5!")
            except:
                console.print("❌ Usage: 'level X' where X is 1-5!")
        elif user_input == 'help':
            console.print("Commands: 'level X' (change level), 'quit'/'exit' (leave)")

        console.print()  # Add some spacing

    show_goodbye(user_name)

if __name__ == '__main__':
    main()