#!/usr/bin/env python3
"""
Deduplication tool for Punnyland jokes database.

This tool removes duplicate jokes and fixes quality issues.
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from rapidfuzz import fuzz
import re


def normalize_joke(joke: str) -> str:
    """Normalize joke for comparison."""
    normalized = joke.lower().strip()
    
    # Remove punctuation except apostrophes
    normalized = re.sub(r"[^\w\s']", " ", normalized)
    
    # Collapse whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized


def are_duplicates(joke1: str, joke2: str, threshold: int = 85) -> bool:
    """Check if two jokes are duplicates."""
    norm1 = normalize_joke(joke1)
    norm2 = normalize_joke(joke2)
    
    # Exact match
    if norm1 == norm2:
        return True
    
    # Fuzzy match
    similarity = fuzz.token_set_ratio(norm1, norm2)
    return similarity >= threshold


def deduplicate_jokes():
    """Remove duplicate jokes from the database."""
    jokes_path = Path("punnyland/data/jokes.json")
    
    # Load jokes
    with open(jokes_path, 'r') as f:
        jokes = json.load(f)
    
    original_count = sum(len(joke_list) for joke_list in jokes.values())
    print(f"🔍 Original joke count: {original_count}")
    
    # Track seen jokes globally
    seen_jokes = set()
    duplicates_removed = 0
    
    # Deduplicate within and across levels
    for level, joke_list in jokes.items():
        print(f"  Processing Level {level}: {len(joke_list)} jokes")
        
        deduped_list = []
        level_duplicates = 0
        
        for joke in joke_list:
            joke_normalized = normalize_joke(joke)
            
            # Check if we've seen this joke before
            is_duplicate = False
            for seen_joke in seen_jokes:
                if are_duplicates(joke, seen_joke, threshold=85):
                    is_duplicate = True
                    duplicates_removed += 1
                    level_duplicates += 1
                    break
            
            if not is_duplicate:
                deduped_list.append(joke)
                seen_jokes.add(joke)
        
        jokes[level] = deduped_list
        print(f"    Removed {level_duplicates} duplicates, kept {len(deduped_list)} jokes")
    
    # Save deduplicated jokes
    with open(jokes_path, 'w') as f:
        json.dump(jokes, f, indent=2, ensure_ascii=False)
    
    final_count = sum(len(joke_list) for joke_list in jokes.values())
    print(f"✅ Deduplication complete!")
    print(f"📊 Final joke count: {final_count}")
    print(f"🗑️  Total duplicates removed: {duplicates_removed}")
    print(f"📈 Reduction: {original_count - final_count} jokes ({((original_count - final_count) / original_count * 100):.1f}%)")


if __name__ == "__main__":
    deduplicate_jokes()