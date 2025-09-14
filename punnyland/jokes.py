"""
Joke management and delivery system for Punnyland
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class JokeManager:
    """Manages the joke database and delivery logic"""

    def __init__(self):
        self.jokes_file = Path(__file__).parent / "data" / "jokes.json"
        self.jokes_data = self.load_jokes()
        self.dad_facts = self.load_dad_facts()

    def load_jokes(self) -> Dict[str, List[str]]:
        """Load jokes from JSON file"""
        try:
            with open(self.jokes_file, 'r') as f:
                data = json.load(f)
                # Convert string keys to integers for easier handling
                return {int(k): v for k, v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading jokes: {e}")
            return {}

    def load_dad_facts(self) -> List[str]:
        """Load fun dad facts and sayings"""
        return [
            "Did you know? The average dad tells 3.2 jokes per day!",
            "Fun fact: Dad jokes are scientifically proven to build character!",
            "Did you know? 'Dad humor' is a genetic trait passed down through generations!",
            "Fun fact: The groan is the highest form of dad joke appreciation!",
            "Did you know? Dad jokes are like fine wine - they get better with age (and worse at the same time)!",
            "Fun fact: Studies show dad jokes reduce stress by 47%*! (*Study may not exist)",
            "Did you know? The dad joke was invented in 1847 by a father named Chuck Chuckle!",
            "Fun fact: Professional comedians are secretly jealous of dad joke mastery!",
            "Did you know? Dad jokes are the only jokes that improve when told repeatedly!",
            "Fun fact: The eye roll is actually a sign of deep appreciation for quality humor!",
            "Did you know? Dad jokes are considered a form of folk art in 17 countries!",
            "Fun fact: The best dad jokes are told while wearing socks with sandals!",
            "Did you know? Dad jokes have their own periodic table of elements: Punium (Pu)!",
            "Fun fact: Ancient cave paintings show dads telling jokes around campfires!",
            "Did you know? There's a secret dad joke university somewhere in Ohio!"
        ]

    def get_joke_by_level(self, corniness_level: int, avoid_recent: List[str] = None) -> Optional[str]:
        """Get a random joke at specified corniness level"""
        if corniness_level not in self.jokes_data:
            return None

        available_jokes = self.jokes_data[corniness_level].copy()

        # Filter out recently heard jokes
        if avoid_recent:
            available_jokes = [joke for joke in available_jokes if joke not in avoid_recent]

        # If we've filtered out too many, add some back
        if len(available_jokes) < 3:
            available_jokes = self.jokes_data[corniness_level].copy()

        return random.choice(available_jokes) if available_jokes else None

    def get_random_joke(self, avoid_recent: List[str] = None) -> Tuple[str, int]:
        """Get a completely random joke from any level"""
        # Weight towards middle levels (2-4) for better balance
        level_weights = {1: 0.1, 2: 0.2, 3: 0.4, 4: 0.2, 5: 0.1}

        level = random.choices(
            list(level_weights.keys()),
            weights=list(level_weights.values())
        )[0]

        joke = self.get_joke_by_level(level, avoid_recent)
        return joke, level

    def get_daily_joke(self, corniness_level: int = 3) -> Tuple[str, int]:
        """Get joke of the day - same joke for the same day"""
        # Use date as seed for consistent daily joke
        today = datetime.now().date()
        random.seed(today.toordinal())

        joke = self.get_joke_by_level(corniness_level)

        # Reset random seed
        random.seed()

        return joke, corniness_level

    def get_dad_fact(self) -> str:
        """Get a random dad fact"""
        return random.choice(self.dad_facts)

    def search_jokes(self, search_term: str, corniness_level: Optional[int] = None) -> List[Tuple[str, int]]:
        """Search for jokes containing specific terms"""
        results = []
        search_lower = search_term.lower()

        levels_to_search = [corniness_level] if corniness_level else range(1, 6)

        for level in levels_to_search:
            if level in self.jokes_data:
                for joke in self.jokes_data[level]:
                    if search_lower in joke.lower():
                        results.append((joke, level))

        return results

    def get_jokes_count(self) -> Dict[int, int]:
        """Get count of jokes per corniness level"""
        return {level: len(jokes) for level, jokes in self.jokes_data.items()}

    def get_total_jokes_count(self) -> int:
        """Get total number of jokes in database"""
        return sum(len(jokes) for jokes in self.jokes_data.values())

    def validate_corniness_level(self, level: int) -> bool:
        """Check if corniness level is valid"""
        return 1 <= level <= 5

    def get_corniness_description(self, level: int) -> str:
        """Get description for corniness level"""
        descriptions = {
            1: "🌱 Mild Chuckle - Subtle wordplay, almost respectable",
            2: "🌽 Dad Approved - Classic dad territory",
            3: "🌽🌽 Eye Roll Guaranteed - Peak dad joke territory",
            4: "🌽🌽🌽 Groan Zone - Painfully punny",
            5: "🌽🌽🌽🌽🌽 Ultra Corn - So bad they're good again"
        }
        return descriptions.get(level, "Unknown level")

    def get_joke_stats(self) -> Dict:
        """Get comprehensive joke database statistics"""
        total_jokes = self.get_total_jokes_count()
        jokes_per_level = self.get_jokes_count()

        return {
            "total_jokes": total_jokes,
            "jokes_per_level": jokes_per_level,
            "average_per_level": total_jokes / len(jokes_per_level) if jokes_per_level else 0,
            "most_corny_level": max(jokes_per_level.keys()) if jokes_per_level else 0,
            "database_health": "Excellent" if total_jokes >= 200 else "Good" if total_jokes >= 100 else "Needs more jokes!"
        }

class JokeDelivery:
    """Handles the delivery and presentation of jokes"""

    def __init__(self, joke_manager: JokeManager):
        self.joke_manager = joke_manager

        # Dad responses for different situations
        self.setup_responses = [
            "Alright, here we go...",
            "Oh, you're gonna love this one!",
            "This one's a real knee-slapper!",
            "Buckle up for this beauty!",
            "I've been saving this one just for you!",
            "This joke has been in the family for generations!",
            "Get ready to groan!",
            "This one's so good, it hurts!"
        ]

        self.follow_up_responses = [
            "See what I did there? 😏",
            "That one gets 'em every time!",
            "I'll be here all week! Try the fish!",
            "Thank you, thank you, I'll see myself out!",
            "Your mom loves that joke!",
            "I'm not just funny, I'm dad funny!",
            "That joke has layers, like an onion!",
            "Classic dad material right there!"
        ]

        self.groan_responses = [
            "That groan means it was a good one!",
            "The louder the groan, the better the joke!",
            "Your groans fuel my comedy fire!",
            "That's the sound of appreciation!",
            "Groaning is just applause for dads!",
            "Music to my ears!",
            "That groan says it all!",
            "Victory! Another successful dad joke!"
        ]

    def get_setup_response(self) -> str:
        """Get a dad setup line before telling a joke"""
        return random.choice(self.setup_responses)

    def get_follow_up_response(self) -> str:
        """Get a dad follow-up after telling a joke"""
        return random.choice(self.follow_up_responses)

    def get_groan_response(self) -> str:
        """Get a response to acknowledge a groan"""
        return random.choice(self.groan_responses)

    def create_joke_package(self, corniness_level: int, user_name: Optional[str] = None,
                          avoid_recent: List[str] = None) -> Dict:
        """Create a complete joke package with all the trimmings"""
        joke = self.joke_manager.get_joke_by_level(corniness_level, avoid_recent)

        if not joke:
            return None

        # Personalize based on user
        name_variants = [
            f"Hey {user_name}!",
            f"Listen to this one, {user_name}!",
            f"{user_name}, you're gonna love this!",
            f"This one's for you, {user_name}!",
            f"Alright {user_name}, ready?"
        ] if user_name else [
            "Hey there!",
            "Listen to this one!",
            "You're gonna love this!",
            "Ready for this?",
            "Here's a good one!"
        ]

        return {
            "joke": joke,
            "corniness_level": corniness_level,
            "setup_line": random.choice(name_variants),
            "dad_setup": self.get_setup_response(),
            "follow_up": self.get_follow_up_response(),
            "corniness_description": self.joke_manager.get_corniness_description(corniness_level),
            "dad_fact": self.joke_manager.get_dad_fact() if random.random() < 0.3 else None  # 30% chance
        }

    def create_daily_joke_package(self, corniness_level: int, user_name: Optional[str] = None) -> Dict:
        """Create a special daily joke package"""
        joke, level = self.joke_manager.get_daily_joke(corniness_level)

        daily_intros = [
            "🌅 Good morning! Here's today's special joke!",
            "☀️ Rise and shine! Time for your daily dose of dad humor!",
            "🎭 Welcome to today's featured presentation!",
            "⭐ Today's joke of the day is brought to you by... me!",
            "🌟 Special delivery: one premium dad joke, hot off the press!"
        ]

        package = self.create_joke_package(level, user_name)
        if package:
            package.update({
                "is_daily": True,
                "daily_intro": random.choice(daily_intros),
                "special_note": "This is your special joke of the day! Come back tomorrow for another!"
            })

        return package