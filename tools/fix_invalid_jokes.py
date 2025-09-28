#!/usr/bin/env python3
"""
Tool to identify and fix invalid jokes in the Punnyland database.
"""

import json
from pathlib import Path
import sys
sys.path.append('.')
from tools.rate_jokes import JokeRater


def find_invalid_jokes():
    """Find and analyze all invalid jokes in the database."""
    rater = JokeRater()
    
    # Load jokes
    jokes_path = Path("punnyland/data/jokes.json")
    with open(jokes_path, 'r') as f:
        jokes = json.load(f)
    
    invalid_jokes = []
    
    print("🔍 Scanning database for invalid jokes...")
    
    for level, joke_list in jokes.items():
        for i, joke in enumerate(joke_list):
            rating = rater.rate_joke(joke)
            
            if not rating['valid']:
                invalid_jokes.append({
                    'level': level,
                    'index': i,
                    'joke': joke,
                    'issues': rating['issues'],
                    'recommendations': rating['recommendations'],
                    'quality_score': rating['quality_score']
                })
    
    return invalid_jokes


def fix_invalid_jokes(invalid_jokes):
    """Provide fixes for invalid jokes."""
    print(f"\n⚠️  Found {len(invalid_jokes)} invalid jokes:\n")
    
    fixes = {}
    
    for i, invalid in enumerate(invalid_jokes, 1):
        print(f"{i}. Level {invalid['level']}[{invalid['index']}]:")
        print(f"   Original: \"{invalid['joke']}\"")
        print(f"   Issues: {', '.join(invalid['issues'])}")
        
        # Suggest fixes based on issues
        original = invalid['joke']
        fixed = original
        
        # Fix common issues
        for issue in invalid['issues']:
            if "Contains explanation:" in issue:
                # Remove explanation markers
                if "because" in issue.lower():
                    fixed = fixed.split(' because')[0].strip()
                    if not fixed.endswith(('!', '?', '.')):
                        fixed += '!'
                elif "get it" in issue.lower():
                    fixed = fixed.replace("Get it?", "").replace("get it?", "").strip()
                elif "you see" in issue.lower():
                    fixed = fixed.split(' you see')[0].strip()
                elif "meaning" in issue.lower():
                    fixed = fixed.split(' meaning')[0].strip()
                elif "lol" in issue.lower():
                    fixed = fixed.replace(" lol", "").replace("lol", "").strip()
                elif "haha" in issue.lower():
                    fixed = fixed.replace(" haha", "").replace("haha", "").strip()
        
        # Clean up formatting
        fixed = fixed.strip()
        if fixed and not fixed.endswith(('.', '!', '?')):
            if '?' in original:
                fixed += '?'
            else:
                fixed += '.'
        
        if fixed != original:
            print(f"   Suggested fix: \"{fixed}\"")
            fixes[f"{invalid['level']},{invalid['index']}"] = fixed
        else:
            print(f"   Manual review needed - {invalid['recommendations'][0] if invalid['recommendations'] else 'Complex issue'}")
        
        print()
    
    return fixes


def apply_fixes(fixes):
    """Apply the suggested fixes to the database."""
    if not fixes:
        print("No automatic fixes available.")
        return
    
    # Load jokes
    jokes_path = Path("punnyland/data/jokes.json")
    with open(jokes_path, 'r') as f:
        jokes = json.load(f)
    
    applied_count = 0
    
    for key, fixed_joke in fixes.items():
        level, index = key.split(',')
        index = int(index)
        
        original = jokes[level][index]
        jokes[level][index] = fixed_joke
        
        print(f"✅ Fixed Level {level}[{index}]:")
        print(f"   Before: \"{original}\"")
        print(f"   After:  \"{fixed_joke}\"")
        applied_count += 1
    
    # Save fixed jokes
    with open(jokes_path, 'w') as f:
        json.dump(jokes, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Applied {applied_count} fixes to the database.")
    return applied_count


def main():
    """Main function to find and fix invalid jokes."""
    # Find invalid jokes
    invalid_jokes = find_invalid_jokes()
    
    if not invalid_jokes:
        print("✅ No invalid jokes found! Database is clean.")
        return
    
    # Show fixes
    fixes = fix_invalid_jokes(invalid_jokes)
    
    if fixes:
        response = input(f"Apply {len(fixes)} automatic fixes? (y/N): ").strip().lower()
        if response == 'y':
            apply_fixes(fixes)
            
            # Re-scan to verify
            print("\n🔄 Re-scanning database...")
            remaining_invalid = find_invalid_jokes()
            if remaining_invalid:
                print(f"⚠️  {len(remaining_invalid)} jokes still need manual review.")
            else:
                print("✅ All jokes are now valid!")
        else:
            print("Fixes not applied. Manual review required.")
    else:
        print("No automatic fixes available. All issues require manual review.")


if __name__ == "__main__":
    main()