#!/usr/bin/env python3
"""
Problematic Content Removal and Replacement Tool

Identifies and replaces jokes that contain potentially offensive racial, ethnic,
or cultural references with funnier, more inclusive alternatives.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
import random


class InclusiveJokeReplacer:
    """Identifies and replaces problematic jokes with inclusive alternatives."""
    
    def __init__(self, jokes_file: str = "punnyland/data/jokes.json"):
        self.jokes_file = jokes_file
        
        # Patterns that indicate potentially problematic content
        self.problematic_patterns = [
            # Generalizations about ethnic/national groups - these are always problematic
            r'why\s+don\'t\s+(africans?|indians?|asians?|chinese|japanese|koreans?|mexicans?|russians?|germans?|french|italians?|spanish|australians?|canadians?|americans?|europeans?)\b',
            r'\b(africans?|indians?|asians?|chinese|japanese|koreans?|mexicans?|russians?|germans?|french|italians?|spanish|australians?|canadians?|americans?|europeans?)\s+(ever|never|always|are|don\'t|can\'t|will|would)\b',
            # Color-based references in racial context
            r'\b(black|white|brown|yellow)\s+(people|person|man|woman|guy|girl)s?\b',
            # Racial/ethnic terms when used in stereotype context
            r'\b(racial|ethnicity|ethnic|nationality|immigrant|foreigner|accent|tribe|tribal)\b',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.problematic_patterns]
        
        # Replacement jokes organized by corniness level
        self.replacement_jokes = {
            1: [
                "I used to hate math puns, but then they grew on me exponentially.",
                "The math teacher called in sick with algebra. I guess she had too many problems.",
                "I'm reading a book about teleportation. It's bound to take me places!",
                "Why don't programmers like nature? It has too many bugs.",
                "I invented a new word: Procrastination. I'll define it later.",
                "Time flies like an arrow. Fruit flies like a banana.",
                "The early bird might get the worm, but the second mouse gets the cheese.",
                "I used to be indecisive, but now I'm not so sure.",
                "Parallel lines have so much in common. It's a shame they'll never meet.",
                "I told my wife she should embrace her mistakes. She gave me a hug.",
            ],
            2: [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call a fake noodle? An impasta!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a sleeping bull? A bulldozer!",
                "Why did the coffee file a police report? It got mugged!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why don't skeletons fight each other? They don't have the guts!",
                "What do you call a fish wearing a crown? A king fish!",
            ],
            3: [
                "What do you call a cow with no legs? Ground beef!",
                "Why don't oysters share? Because they're shellfish!",
                "What do you call a pig that does karate? A pork chop!",
                "Why did the banana go to the doctor? It wasn't peeling well!",
                "What do you call a factory that makes okay products? A satisfactory!",
                "Why don't cannibals eat clowns? They taste funny!",
                "What do you call a belt made of watches? A waist of time!",
                "Why did the cookie go to the doctor? Because it felt crumbly!",
                "What do you call a group of disorganized cats? A cat-astrophe!",
                "Why don't bicycles stand up by themselves? They're two tired!",
            ],
            4: [
                "What do you call a fish that needs help with his vocals? Auto-tuna!",
                "I used to be addicted to the Hokey Pokey, but I turned myself around!",
                "Why don't storm clouds ever apologize? They're too thundered to care!",
                "What do you call a cow that's good at playing instruments? A moo-sician!",
                "Why did the gardener plant light bulbs? He wanted to grow a power plant!",
                "What do you call a dinosaur that loves to sleep? A dino-snore!",
                "Why don't mountains ever get cold? They wear snow caps!",
                "What do you call a train carrying bubblegum? A chew-chew train!",
                "Why did the computer go to the doctor? It had a virus!",
                "What do you call a group of musical whales? An orca-stra!",
            ],
            5: [
                "What do you call a cow that performs magic tricks and teaches calculus? A moo-gician with udderly incredible mathematical skills!",
                "Why did the cat become a motivational speaker? Because it was purr-fectly positioned to inspire with its paws-itive attitude!",
                "What do you call a fish that conducts orchestras while solving crossword puzzles? A bass-master with fin-tastic intellectual abilities!",
                "Why did the dog become a quantum physicist? Because it mastered the art of being in multiple states of happiness simultaneously!",
                "What do you call a chicken that writes poetry and solves mysteries? A clue-cking detective with egg-ceptional literary talents!",
                "Why did the elephant become a memory expert? Because it never forgot to remember everything it needed to not forget!",
                "What do you call a turtle that teaches philosophy and plays jazz? A shell-shocked intellectual with slow-but-steady musical genius!",
                "Why did the penguin become a refrigeration engineer? Because it was ice-olated in its field of expertise!",
                "What do you call a bear that manages a successful startup? An entrepreneur with bear-y good business instincts!",
                "Why did the owl become a time management consultant? Because it was a hoot at working night shifts efficiently!",
            ]
        }
    
    def identify_problematic_jokes(self) -> Dict[str, List[Dict]]:
        """Identify jokes that contain potentially problematic content."""
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        problematic_jokes = {
            'by_level': {},
            'all_problematic': [],
            'total_count': 0
        }
        
        print("🔍 Scanning database for potentially problematic content...")
        
        for level, joke_list in jokes_data.items():
            level_problematic = []
            
            for joke in joke_list:
                # Check if joke matches any problematic patterns
                is_problematic = False
                matched_patterns = []
                
                for i, pattern in enumerate(self.compiled_patterns):
                    if pattern.search(joke):
                        is_problematic = True
                        matched_patterns.append(self.problematic_patterns[i])
                
                if is_problematic:
                    problem_info = {
                        'joke': joke,
                        'level': int(level),
                        'matched_patterns': matched_patterns
                    }
                    level_problematic.append(problem_info)
                    problematic_jokes['all_problematic'].append(problem_info)
            
            if level_problematic:
                problematic_jokes['by_level'][level] = level_problematic
        
        problematic_jokes['total_count'] = len(problematic_jokes['all_problematic'])
        
        return problematic_jokes
    
    def generate_replacement(self, level: int, avoid_jokes: Set[str]) -> str:
        """Generate a replacement joke for the given level."""
        available_jokes = [joke for joke in self.replacement_jokes[level] if joke not in avoid_jokes]
        
        if not available_jokes:
            # Fallback if we've used all replacements for this level
            fallback_jokes = [
                "Why don't scientists trust stairs? Because they're always up to something!",
                "What do you call a fake stone? A shamrock!",
                "Why did the math book look so sad? Because it had too many problems!",
                "What do you call a sleeping bull at the library? A bulldozer in the quiet section!",
                "Why don't clouds ever get speeding tickets? They're always changing lanes!"
            ]
            return random.choice(fallback_jokes)
        
        return random.choice(available_jokes)
    
    def replace_problematic_jokes(self, dry_run: bool = False) -> Dict:
        """Replace problematic jokes with inclusive alternatives."""
        
        # First identify problematic content
        problematic_data = self.identify_problematic_jokes()
        
        if problematic_data['total_count'] == 0:
            print("✅ No problematic content found in the database!")
            return {'replaced': 0, 'message': 'No problematic content found'}
        
        print(f"⚠️  Found {problematic_data['total_count']} potentially problematic jokes")
        
        # Show what will be replaced
        for level, problems in problematic_data['by_level'].items():
            print(f"\n📝 Level {level} ({len(problems)} jokes):")
            for i, problem in enumerate(problems[:3]):  # Show first 3
                print(f"  {i+1}. \"{problem['joke'][:60]}{'...' if len(problem['joke']) > 60 else ''}\"")
                print(f"     Patterns: {', '.join(problem['matched_patterns'])}")
            if len(problems) > 3:
                print(f"  ... and {len(problems) - 3} more")
        
        if dry_run:
            print(f"\n🧪 DRY RUN - Would replace {problematic_data['total_count']} jokes")
            return {
                'dry_run': True,
                'would_replace': problematic_data['total_count'],
                'by_level': {level: len(problems) for level, problems in problematic_data['by_level'].items()}
            }
        
        # Create backup
        backup_file = self.jokes_file.replace('.json', '_backup_pre_inclusive_cleanup.json')
        with open(self.jokes_file, 'r') as f:
            original_data = json.load(f)
        with open(backup_file, 'w') as f:
            json.dump(original_data, f, indent=2)
        print(f"💾 Backup created: {backup_file}")
        
        # Apply replacements
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        used_replacements = set()
        replacements_made = 0
        
        for level, problems in problematic_data['by_level'].items():
            print(f"\n🔄 Processing Level {level}...")
            
            for problem in problems:
                old_joke = problem['joke']
                new_joke = self.generate_replacement(int(level), used_replacements)
                used_replacements.add(new_joke)
                
                # Replace in the data
                if old_joke in jokes_data[level]:
                    jokes_data[level].remove(old_joke)
                    jokes_data[level].append(new_joke)
                    replacements_made += 1
                    
                    print(f"✅ Replaced: \"{old_joke[:50]}{'...' if len(old_joke) > 50 else ''}\"")
                    print(f"   With: \"{new_joke[:50]}{'...' if len(new_joke) > 50 else ''}\"")
        
        # Save updated data
        with open(self.jokes_file, 'w') as f:
            json.dump(jokes_data, f, indent=2)
        
        print(f"\n🎯 Inclusive Cleanup Complete!")
        print(f"   Jokes Replaced: {replacements_made}")
        print(f"   Database Updated: {self.jokes_file}")
        
        return {
            'replaced': replacements_made,
            'backup_file': backup_file,
            'by_level': {level: len(problems) for level, problems in problematic_data['by_level'].items()}
        }
    
    def validate_inclusivity(self) -> Dict:
        """Validate that the database is now free of problematic content."""
        problematic_data = self.identify_problematic_jokes()
        
        if problematic_data['total_count'] == 0:
            print("✅ Database validation passed: No problematic content found!")
            return {'valid': True, 'issues': 0}
        else:
            print(f"❌ Database validation failed: {problematic_data['total_count']} issues remain")
            return {'valid': False, 'issues': problematic_data['total_count'], 'details': problematic_data}


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Remove problematic content and replace with inclusive jokes")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be replaced without making changes")
    parser.add_argument("--validate", action="store_true", help="Only validate current database for problematic content")
    parser.add_argument("--file", default="punnyland/data/jokes.json", help="Jokes file to process")
    
    args = parser.parse_args()
    
    replacer = InclusiveJokeReplacer(args.file)
    
    print("🎭 Punnyland Inclusive Content Tool")
    print("=" * 50)
    
    if args.validate:
        replacer.validate_inclusivity()
    else:
        result = replacer.replace_problematic_jokes(dry_run=args.dry_run)
        
        if not args.dry_run and result['replaced'] > 0:
            print(f"\n🔍 Running post-replacement validation...")
            replacer.validate_inclusivity()


if __name__ == "__main__":
    main()