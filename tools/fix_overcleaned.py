#!/usr/bin/env python3
"""
Quick fix script for over-cleaned jokes in Punnyland database.
"""

import json
from pathlib import Path

def fix_overcleaned_jokes():
    """Fix jokes that were over-cleaned by the cleaning script."""
    
    # Load current jokes
    jokes_file = Path("punnyland/data/jokes.json")
    with open(jokes_file, 'r') as f:
        jokes = json.load(f)
    
    # Replacement jokes for broken ones
    replacement_jokes = {
        "What do you call a fish": [
            "What do you call a fish wearing a crown? A king fish.",
            "What do you call a fish that needs help with vocals? Auto-tuna.",
            "What do you call a fish wearing a bowtie? Sofishticated.",
            "What do you call a fish that practices medicine? A sturgeon.",
            "What do you call a fish with no eyes? Fsh.",
            "What do you call a fish wearing headphones? Bass-boosted.",
            "What do you call a fish that's good at basketball? A ball hog.",
            "What do you call a fish that's good at tennis? A racket fish.",
            "What do you call a fish that's good at soccer? A goal-fish.",
            "What do you call a fish that's good at golf? A hole-in-one fish.",
            "What do you call a fish that's good at cooking? A chef-fish.",
            "What do you call a fish that's good at cleaning? A mop-fish.",
            "What do you call a fish that's good at singing? A tuna.",
            "What do you call a fish that's good at photography? A snap-per.",
            "What do you call a fish that's good at construction? A hammer-head.",
        ],
        "What do you call a cow": [
            "What do you call a cow with no legs? Ground beef.",
            "What do you call a cow with two legs? Lean beef.",
            "What do you call a cow with a twitch? Beef jerky.",
            "What do you call a cow on a trampoline? A milkshake.",
            "What do you call a cow that doesn't give milk? A milk dud.",
            "What do you call a cow with a sense of humor? Laughing stock.",
            "What do you call a cow that's just given birth? Decalfinated.",
            "What do you call a cow that's good at math? A calcu-later.",
            "What do you call a cow that's good at dancing? A moo-ver and shaker.",
            "What do you call a cow that's good at singing? A moo-sician.",
            "What do you call a cow that's good at comedy? A laugh-stock.",
            "What do you call a cow that's good at writing? A cow-thor.",
            "What do you call a cow that's good at teaching? A cow-structor.",
            "What do you call a cow that's good at fixing things? A cow-mechanic.",
            "What do you call a cow that's good at magic? A moo-gician.",
        ],
        "What do you call a bear": [
            "What do you call a bear with no teeth? A gummy bear.",
            "What do you call a bear in the rain? A drizzly bear.",
            "What do you call a bear with no ears? B.",
            "What do you call a sleepy grizzly bear? A bear minimum.",
        ]
    }
    
    # Track fixes
    fixes_made = 0
    replacement_index = {"fish": 0, "cow": 0, "bear": 0}
    
    # Fix broken jokes
    for level, joke_list in jokes.items():
        for i, joke in enumerate(joke_list):
            if joke == "What do you call a fish" and replacement_index["fish"] < len(replacement_jokes["What do you call a fish"]):
                jokes[level][i] = replacement_jokes["What do you call a fish"][replacement_index["fish"]]
                replacement_index["fish"] += 1
                fixes_made += 1
                print(f"Fixed Level {level}[{i}]: {jokes[level][i]}")
                
            elif joke == "What do you call a cow" and replacement_index["cow"] < len(replacement_jokes["What do you call a cow"]):
                jokes[level][i] = replacement_jokes["What do you call a cow"][replacement_index["cow"]]
                replacement_index["cow"] += 1
                fixes_made += 1
                print(f"Fixed Level {level}[{i}]: {jokes[level][i]}")
                
            elif joke == "What do you call a bear" and replacement_index["bear"] < len(replacement_jokes["What do you call a bear"]):
                jokes[level][i] = replacement_jokes["What do you call a bear"][replacement_index["bear"]]
                replacement_index["bear"] += 1
                fixes_made += 1
                print(f"Fixed Level {level}[{i}]: {jokes[level][i]}")
    
    # Save the fixed jokes
    with open(jokes_file, 'w') as f:
        json.dump(jokes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Fixed {fixes_made} over-cleaned jokes!")
    
    # Final count
    total = sum(len(joke_list) for joke_list in jokes.values())
    print(f"📊 Total jokes after fixes: {total}")

if __name__ == "__main__":
    fix_overcleaned_jokes()