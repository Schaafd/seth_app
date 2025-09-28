#!/usr/bin/env python3
"""
Invalid Joke Cleanup Tool

Identifies and fixes invalid jokes in the database, with special focus on
overly long Level 5 jokes that exceed character limits.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add the parent directory to Python path to import the rating tool
sys.path.append(str(Path(__file__).parent))
from rate_jokes import JokeRater


class JokeCleanup:
    """Cleans up invalid jokes in the database."""
    
    def __init__(self, jokes_file: str = "punnyland/data/jokes.json"):
        self.jokes_file = jokes_file
        self.rater = JokeRater()
        
    def identify_invalid_jokes(self) -> Dict:
        """Identify all invalid jokes and their issues."""
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        invalid_jokes = {}
        for level, joke_list in jokes_data.items():
            level_invalid = []
            for joke in joke_list:
                rating = self.rater.rate_joke(joke)
                if not rating['valid']:
                    level_invalid.append({
                        'joke': joke,
                        'issues': rating['issues'],
                        'length': len(joke),
                        'rating': rating
                    })
            if level_invalid:
                invalid_jokes[level] = level_invalid
        
        return invalid_jokes
    
    def fix_long_jokes(self, joke: str) -> Tuple[str, bool]:
        """Attempt to fix overly long jokes by intelligent trimming."""
        if len(joke) <= 180:
            return joke, False
        
        # Strategy 1: Remove explanatory endings
        explanations = [
            r'!\s*Talk about.*?!$',
            r'!\s*That\'s what I call.*?!$',
            r'!\s*Now that\'s.*?!$',
            r'!\s*I thought.*?!$',
            r'!\s*Everyone agreed.*?!$',
            r'!\s*It was.*?success.*?!$',
        ]
        
        fixed_joke = joke
        for pattern in explanations:
            fixed_joke = re.sub(pattern, '!', fixed_joke, flags=re.IGNORECASE)
        
        if len(fixed_joke) <= 180:
            return fixed_joke.strip(), True
        
        # Strategy 2: Simplify the core joke to essential elements
        # Find the main setup and punchline, remove elaborative details
        
        # Look for pattern: Setup + punchline with excessive detail
        match = re.match(r'^(.*?\?)\s*(.*?)([!.]).*', fixed_joke)
        if match:
            setup, answer, punct = match.groups()
            simplified = f"{setup.strip()} {answer.strip()}{punct}"
            if len(simplified) <= 180:
                return simplified, True
        
        # Strategy 3: Find the core punchline and keep just that
        sentences = re.split(r'[!.]\s+', fixed_joke)
        if len(sentences) > 1:
            # Try to keep just the first sentence that contains a pun
            for sentence in sentences:
                if len(sentence) <= 180:
                    # Check if it contains pun elements
                    pun_indicators = ['moo', 'paws', 'fur', 'tail', 'purr', '-', 'udderly', 'paw-']
                    if any(indicator in sentence.lower() for indicator in pun_indicators):
                        if not sentence.endswith(('.', '!', '?')):
                            sentence += '!'
                        return sentence.strip(), True
        
        # Strategy 4: Truncate at 180 chars at word boundary
        if len(joke) > 180:
            truncated = joke[:177] + '...'
            # Find the last complete word
            last_space = truncated.rfind(' ')
            if last_space > 100:  # Make sure we don't truncate too much
                truncated = joke[:last_space] + '!'
                return truncated, True
        
        return joke, False  # Could not fix
    
    def cleanup_level_5(self) -> Dict:
        """Specifically clean up Level 5 jokes."""
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        if '5' not in jokes_data:
            return {'message': 'No Level 5 jokes found'}
        
        original_jokes = jokes_data['5']
        cleaned_jokes = []
        removed_jokes = []
        fixed_count = 0
        
        print(f"🔧 Processing {len(original_jokes)} Level 5 jokes...")
        
        for joke in original_jokes:
            rating = self.rater.rate_joke(joke)
            
            if rating['valid']:
                # Keep valid jokes as-is
                cleaned_jokes.append(joke)
            else:
                # Try to fix invalid jokes
                if 'Too long' in ' '.join(rating['issues']):
                    fixed_joke, was_fixed = self.fix_long_jokes(joke)
                    
                    # Re-rate the fixed joke
                    fixed_rating = self.rater.rate_joke(fixed_joke)
                    
                    if fixed_rating['valid'] and was_fixed:
                        cleaned_jokes.append(fixed_joke)
                        fixed_count += 1
                        print(f"✅ Fixed: {joke[:60]}... → {fixed_joke[:60]}...")
                    elif len(fixed_joke) <= 180:
                        # Even if not fully valid, keep if length is fixed
                        cleaned_jokes.append(fixed_joke)
                        fixed_count += 1
                        print(f"⚠️  Partially fixed: {joke[:60]}...")
                    else:
                        # Cannot fix, remove
                        removed_jokes.append({
                            'joke': joke,
                            'issues': rating['issues'],
                            'length': len(joke)
                        })
                        print(f"❌ Removed: {joke[:60]}... (too long, unfixable)")
                else:
                    # Other issues - try to keep if not too problematic
                    if len(joke) <= 180 and len(rating['issues']) <= 2:
                        cleaned_jokes.append(joke)
                        print(f"⚠️  Kept with issues: {joke[:60]}...")
                    else:
                        removed_jokes.append({
                            'joke': joke,
                            'issues': rating['issues'],
                            'length': len(joke)
                        })
                        print(f"❌ Removed: {joke[:60]}... (multiple issues)")
        
        return {
            'original_count': len(original_jokes),
            'cleaned_count': len(cleaned_jokes),
            'removed_count': len(removed_jokes),
            'fixed_count': fixed_count,
            'cleaned_jokes': cleaned_jokes,
            'removed_jokes': removed_jokes
        }
    
    def apply_cleanup(self, backup: bool = True) -> Dict:
        """Apply cleanup to the database."""
        # Create backup if requested
        if backup:
            backup_file = self.jokes_file.replace('.json', '_backup_pre_cleanup.json')
            with open(self.jokes_file, 'r') as f:
                original_data = json.load(f)
            with open(backup_file, 'w') as f:
                json.dump(original_data, f, indent=2)
            print(f"💾 Backup created: {backup_file}")
        
        # Perform Level 5 cleanup
        cleanup_results = self.cleanup_level_5()
        
        if 'cleaned_jokes' in cleanup_results:
            # Update the database
            with open(self.jokes_file, 'r') as f:
                jokes_data = json.load(f)
            
            jokes_data['5'] = cleanup_results['cleaned_jokes']
            
            with open(self.jokes_file, 'w') as f:
                json.dump(jokes_data, f, indent=2)
            
            print(f"\n✅ Database updated!")
            print(f"   Level 5 jokes: {cleanup_results['original_count']} → {cleanup_results['cleaned_count']}")
            print(f"   Fixed jokes: {cleanup_results['fixed_count']}")
            print(f"   Removed jokes: {cleanup_results['removed_count']}")
        
        return cleanup_results
    
    def preview_cleanup(self) -> Dict:
        """Preview what cleanup would do without making changes."""
        print("🔍 Previewing cleanup (no changes will be made)...")
        return self.cleanup_level_5()


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean up invalid jokes in database")
    parser.add_argument("--preview", action="store_true", help="Preview changes without applying")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup file")
    parser.add_argument("--file", default="punnyland/data/jokes.json", help="Jokes file to clean")
    
    args = parser.parse_args()
    
    cleaner = JokeCleanup(args.file)
    
    if args.preview:
        results = cleaner.preview_cleanup()
    else:
        results = cleaner.apply_cleanup(backup=not args.no_backup)
    
    print("\n📊 Cleanup Summary:")
    if 'original_count' in results:
        print(f"   Original Level 5 jokes: {results['original_count']}")
        print(f"   Would clean to: {results['cleaned_count']}")
        print(f"   Would fix: {results['fixed_count']}")
        print(f"   Would remove: {results['removed_count']}")


if __name__ == "__main__":
    main()