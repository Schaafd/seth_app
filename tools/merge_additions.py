#!/usr/bin/env python3
"""
Merge the generated joke additions into the main jokes database.
"""

import json
from pathlib import Path


def merge_joke_additions():
    """Merge new jokes into the main database."""
    # Load existing jokes
    with open("punnyland/data/jokes.json", 'r') as f:
        existing_jokes = json.load(f)
    
    # Load additions
    additions_path = Path("punnyland/data/jokes_additions.json")
    if not additions_path.exists():
        print("No joke additions file found.")
        return
    
    with open(additions_path, 'r') as f:
        new_jokes = json.load(f)
    
    # Merge jokes
    total_added = 0
    for level, joke_list in new_jokes.items():
        if level not in existing_jokes:
            existing_jokes[level] = []
        
        before_count = len(existing_jokes[level])
        existing_jokes[level].extend(joke_list)
        after_count = len(existing_jokes[level])
        added_count = after_count - before_count
        
        print(f"Level {level}: Added {added_count} jokes ({before_count} → {after_count})")
        total_added += added_count
    
    # Save updated jokes
    with open("punnyland/data/jokes.json", 'w') as f:
        json.dump(existing_jokes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Merged {total_added} new jokes into the database!")
    
    # Show final counts
    print("\n📊 Final joke distribution:")
    grand_total = 0
    for level in ['1', '2', '3', '4', '5']:
        count = len(existing_jokes.get(level, []))
        grand_total += count
        print(f"  Level {level}: {count} jokes")
    
    print(f"\n🎯 Total jokes: {grand_total}")
    
    # Remove additions file
    additions_path.unlink()
    print(f"🗑️  Cleaned up {additions_path}")


if __name__ == "__main__":
    merge_joke_additions()