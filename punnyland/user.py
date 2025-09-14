"""
User settings and personalization system for Punnyland
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class UserProfile:
    """Manages user preferences and joke history"""

    def __init__(self):
        self.config_dir = Path.home() / ".punnyland"
        self.config_file = self.config_dir / "user_data.json"
        self.ensure_config_dir()
        self.data = self.load_user_data()

    def ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(exist_ok=True)

    def load_user_data(self) -> Dict:
        """Load user data from config file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Default user data
        return {
            "name": None,
            "corniness_level": 3,  # Default to middle level
            "total_jokes_heard": 0,
            "favorite_jokes": [],
            "joke_history": [],  # Track jokes to avoid repeats
            "daily_joke_date": None,
            "setup_completed": False,
            "dad_facts_enabled": True,
            "sound_effects": True,
            "personality_level": 3,  # How enthusiastic dad should be
            "achievements": [],
            "groan_counter": 0,
            "created_date": datetime.now().isoformat()
        }

    def save_user_data(self):
        """Save user data to config file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save user data: {e}")

    def is_setup_completed(self) -> bool:
        """Check if initial setup is completed"""
        return self.data.get("setup_completed", False)

    def complete_setup(self, name: str, corniness_level: int):
        """Complete initial user setup"""
        self.data.update({
            "name": name.strip(),
            "corniness_level": corniness_level,
            "setup_completed": True
        })
        self.save_user_data()

    def get_name(self) -> Optional[str]:
        """Get user's name"""
        return self.data.get("name")

    def get_corniness_level(self) -> int:
        """Get user's preferred corniness level"""
        return self.data.get("corniness_level", 3)

    def set_corniness_level(self, level: int):
        """Set user's corniness level (1-5)"""
        if 1 <= level <= 5:
            self.data["corniness_level"] = level
            self.save_user_data()
            return True
        return False

    def get_total_jokes_heard(self) -> int:
        """Get total number of jokes user has heard"""
        return self.data.get("total_jokes_heard", 0)

    def add_joke_to_history(self, joke: str, corniness_level: int):
        """Add a joke to user's history"""
        self.data["joke_history"].append({
            "joke": joke,
            "corniness": corniness_level,
            "timestamp": datetime.now().isoformat()
        })

        self.data["total_jokes_heard"] += 1

        # Keep only last 50 jokes to avoid huge files
        if len(self.data["joke_history"]) > 50:
            self.data["joke_history"] = self.data["joke_history"][-50:]

        self.check_achievements()
        self.save_user_data()

    def get_recent_jokes(self, count: int = 10) -> List[str]:
        """Get recently heard jokes to avoid repeats"""
        recent = self.data.get("joke_history", [])[-count:]
        return [entry["joke"] for entry in recent]

    def add_to_favorites(self, joke: str, corniness_level: int):
        """Add joke to favorites"""
        favorite_entry = {
            "joke": joke,
            "corniness": corniness_level,
            "added_date": datetime.now().isoformat()
        }

        # Check if already in favorites
        for fav in self.data["favorite_jokes"]:
            if fav["joke"] == joke:
                return False  # Already in favorites

        self.data["favorite_jokes"].append(favorite_entry)
        self.save_user_data()
        return True

    def get_favorites(self) -> List[Dict]:
        """Get user's favorite jokes"""
        return self.data.get("favorite_jokes", [])

    def remove_from_favorites(self, joke: str) -> bool:
        """Remove joke from favorites"""
        favorites = self.data.get("favorite_jokes", [])
        original_len = len(favorites)

        self.data["favorite_jokes"] = [fav for fav in favorites if fav["joke"] != joke]

        if len(self.data["favorite_jokes"]) < original_len:
            self.save_user_data()
            return True
        return False

    def increment_groan_counter(self):
        """Increment the groan counter - for dad joke satisfaction"""
        self.data["groan_counter"] = self.data.get("groan_counter", 0) + 1
        self.save_user_data()

    def get_groan_counter(self) -> int:
        """Get current groan count"""
        return self.data.get("groan_counter", 0)

    def get_achievements(self) -> List[str]:
        """Get user's achievements"""
        return self.data.get("achievements", [])

    def check_achievements(self):
        """Check and award achievements based on activity"""
        current_achievements = set(self.data.get("achievements", []))
        total_jokes = self.data.get("total_jokes_heard", 0)

        # Achievement thresholds
        achievements_to_check = [
            (1, "First Steps", "Heard your first dad joke!"),
            (5, "Getting Started", "5 jokes down, infinity to go!"),
            (15, "Pun Enthusiast", "You're really getting into the groove!"),
            (30, "Joke Collector", "Building quite the dad joke collection!"),
            (50, "Corn Connoisseur", "You know quality corn when you hear it!"),
            (100, "Pun Master", "You've mastered the art of dad jokes!"),
            (200, "Dad Joke Royalty", "Bow down to the joke royalty!"),
        ]

        for threshold, title, description in achievements_to_check:
            if total_jokes >= threshold and title not in current_achievements:
                self.data["achievements"].append(title)

    def get_daily_joke_eligible(self) -> bool:
        """Check if user is eligible for today's joke"""
        today = datetime.now().date().isoformat()
        last_daily = self.data.get("daily_joke_date")
        return last_daily != today

    def mark_daily_joke_seen(self):
        """Mark today's daily joke as seen"""
        self.data["daily_joke_date"] = datetime.now().date().isoformat()
        self.save_user_data()

    def get_personality_responses(self) -> Dict:
        """Get dad personality responses based on corniness level"""
        level = self.get_corniness_level()

        personalities = {
            1: {
                "enthusiasm": "subtle",
                "greetings": ["Hello there.", "Good to see you.", "Ready for some humor?"],
                "reactions": ["Not bad.", "Quite clever.", "I see what you did there."],
                "style": "sophisticated"
            },
            2: {
                "enthusiasm": "mild",
                "greetings": ["Hey there!", "Good to see you, friend!", "Ready for some jokes?"],
                "reactions": ["That's a good one!", "Classic!", "I like that one."],
                "style": "friendly"
            },
            3: {
                "enthusiasm": "moderate",
                "greetings": ["Hey kiddo!", "Well hello there, sport!", "Ready for some dad humor?"],
                "reactions": ["Ha! That's a good one!", "Classic dad material!", "I'm definitely using that one!"],
                "style": "traditional_dad"
            },
            4: {
                "enthusiasm": "high",
                "greetings": ["HEY THERE CHAMP!", "Well howdy, partner!", "READY TO GET PUNNY?!"],
                "reactions": ["OH BOY, THAT'S A GOOD ONE!", "WOW! Peak dad humor right there!", "I'm TOTALLY stealing that joke!"],
                "style": "enthusiastic_dad"
            },
            5: {
                "enthusiasm": "ultra",
                "greetings": ["WELL HELLO THERE, MY FAVORITE AUDIENCE!", "HOWDY THERE, SUPERSTAR!", "GET READY FOR MAXIMUM DAD ENERGY!"],
                "reactions": ["OH MY GOODNESS! THAT'S ABSOLUTELY CORN-TASTIC!", "WOWZA! That joke just made my WHOLE WEEK!", "I'M GONNA TELL EVERYONE I KNOW THAT ONE!"],
                "style": "maximum_dad_energy"
            }
        }

        return personalities.get(level, personalities[3])

    def export_favorites(self, filename: Optional[str] = None) -> str:
        """Export favorite jokes to a text file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"punnyland_favorites_{timestamp}.txt"

        try:
            with open(filename, 'w') as f:
                f.write("🎭 My Punnyland Favorite Dad Jokes 🎭\n")
                f.write("="*50 + "\n\n")

                favorites = self.get_favorites()
                if not favorites:
                    f.write("No favorite jokes yet! Start collecting some corn! 🌽\n")
                else:
                    for i, fav in enumerate(favorites, 1):
                        f.write(f"{i}. {fav['joke']}\n")
                        f.write(f"   Corniness Level: {fav['corniness']}\n")
                        f.write(f"   Added: {fav['added_date'][:10]}\n\n")

                f.write(f"\nExported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("Generated by Punnyland CLI - Where Dad Jokes Come to Life! 🎭\n")

            return filename
        except IOError as e:
            raise Exception(f"Could not export favorites: {e}")

    def get_stats(self) -> Dict:
        """Get comprehensive user statistics"""
        return {
            "name": self.get_name(),
            "total_jokes": self.get_total_jokes_heard(),
            "corniness_level": self.get_corniness_level(),
            "favorites_count": len(self.get_favorites()),
            "groan_count": self.get_groan_counter(),
            "achievements_count": len(self.get_achievements()),
            "achievements": self.get_achievements(),
            "member_since": self.data.get("created_date", "Unknown")[:10]
        }