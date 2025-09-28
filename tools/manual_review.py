#!/usr/bin/env python3
"""
Manual Joke Review Tool

Interactive tool for reviewing and correcting joke classifications.
Focuses on misclassified jokes and helps curate proper corniness levels.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import random

# Add the parent directory to Python path to import tools
sys.path.append(str(Path(__file__).parent))
from rate_jokes import JokeRater
from analyze_classification import ClassificationAnalyzer


class ManualReviewer:
    """Interactive tool for manually reviewing and correcting joke classifications."""
    
    def __init__(self, jokes_file: str = "punnyland/data/jokes.json"):
        self.jokes_file = jokes_file
        self.rater = JokeRater()
        self.analyzer = ClassificationAnalyzer(jokes_file)
        self.corrections = {}  # Store manual corrections
        
    def show_rubric(self):
        """Display the corniness level rubric for reference."""
        print("\n" + "="*80)
        print("🌽 PUNNYLAND CORNINESS SCALE REFERENCE")
        print("="*80)
        
        rubric = {
            1: {
                'name': '🌱 Mild Chuckle',
                'desc': 'Subtle wordplay or clever twist',
                'examples': [
                    "I used to hate facial hair, but then it grew on me.",
                    "Time flies like an arrow. Fruit flies like a banana.",
                    "I invented a new word: Plagiarism."
                ]
            },
            2: {
                'name': '🌽 Dad Approved',
                'desc': 'Classic setups with gentle puns',
                'examples': [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "What do you call a fake noodle? An impasta!",
                    "Why did the scarecrow win an award? He was outstanding in his field!"
                ]
            },
            3: {
                'name': '🌽🌽 Eye Roll Guaranteed', 
                'desc': 'Obvious puns or classic dad joke forms',
                'examples': [
                    "What do you call a bear with no teeth? A gummy bear!",
                    "Why don't eggs tell jokes? They'd crack each other up!",
                    "What do you call a cow with no legs? Ground beef!"
                ]
            },
            4: {
                'name': '🌽🌽🌽 Groan Zone',
                'desc': 'Heavy-handed pun density or clunky homophones', 
                'examples': [
                    "What do you call a fish that needs help with his vocals? Auto-tuna!",
                    "I used to be addicted to the Hokey Pokey, but I turned myself around!"
                ]
            },
            5: {
                'name': '🌽🌽🌽🌽🌽 Ultra Corn',
                'desc': 'So bad they loop back to funny',
                'examples': [
                    "Multiple stacked puns with excessive wordplay",
                    "Maximum corniness that becomes endearing"
                ]
            }
        }
        
        for level, info in rubric.items():
            print(f"\nLevel {level}: {info['name']}")
            print(f"  {info['desc']}")
            for example in info['examples']:
                print(f"  • \"{example}\"")
    
    def review_misclassifications(self, focus_pattern: str = None, limit: int = 10):
        """Review misclassified jokes interactively."""
        print("🔍 Loading misclassification data...")
        analysis_results = self.analyzer.load_and_analyze()
        
        # Get misclassifications to review
        patterns_to_review = []
        if focus_pattern:
            if focus_pattern in analysis_results['misclassifications']:
                patterns_to_review.append((focus_pattern, analysis_results['misclassifications'][focus_pattern]))
        else:
            # Get the most problematic patterns
            misclass_counts = {k: len(v) for k, v in analysis_results['misclassifications'].items()}
            top_patterns = sorted(misclass_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for pattern, count in top_patterns:
                patterns_to_review.append((pattern, analysis_results['misclassifications'][pattern]))
        
        print(f"\\n📝 Reviewing {len(patterns_to_review)} misclassification patterns...")
        
        corrections_made = 0
        for pattern, jokes in patterns_to_review:
            print(f"\\n" + "="*80)
            print(f"🔄 REVIEWING PATTERN: {pattern} ({len(jokes)} jokes)")
            print("="*80)
            
            # Show a few examples for this pattern
            sample_size = min(limit, len(jokes))
            sample_jokes = random.sample(jokes, sample_size)
            
            for i, joke_data in enumerate(sample_jokes):
                print(f"\\n--- Joke {i+1}/{sample_size} ---")
                print(f"🎭 \"{joke_data['joke']}\"")
                print(f"📊 Currently: Level {joke_data['actual_level']}, Predicted: Level {joke_data['predicted_level']}")
                print(f"📏 Length: {joke_data['length']} chars, Confidence: {joke_data['confidence']:.3f}")
                
                # Get user input
                while True:
                    print(f"\\nWhat should the correct level be? (1-5, s=skip, r=rubric, q=quit): ", end="")
                    choice = input().strip().lower()
                    
                    if choice == 'q':
                        return corrections_made
                    elif choice == 's':
                        break
                    elif choice == 'r':
                        self.show_rubric()
                        continue
                    elif choice in ['1', '2', '3', '4', '5']:
                        correct_level = int(choice)
                        if correct_level != joke_data['actual_level']:
                            self.corrections[joke_data['joke']] = {
                                'from_level': joke_data['actual_level'],
                                'to_level': correct_level,
                                'pattern': pattern
                            }
                            print(f"✅ Noted: Move from Level {joke_data['actual_level']} → Level {correct_level}")
                            corrections_made += 1
                        else:
                            print("➡️ No change needed")
                        break
                    else:
                        print("Invalid choice. Please enter 1-5, s, r, or q")
        
        return corrections_made
    
    def sample_review_by_level(self, level: int, sample_size: int = 5):
        """Review a sample of jokes from a specific level."""
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        level_str = str(level)
        if level_str not in jokes_data:
            print(f"❌ Level {level} not found in database")
            return 0
        
        jokes = jokes_data[level_str]
        sample_jokes = random.sample(jokes, min(sample_size, len(jokes)))
        
        print(f"\\n" + "="*80)
        print(f"📋 REVIEWING SAMPLE FROM LEVEL {level} ({len(sample_jokes)} jokes)")
        print("="*80)
        
        corrections_made = 0
        for i, joke in enumerate(sample_jokes):
            rating = self.rater.rate_joke(joke)
            
            print(f"\\n--- Joke {i+1}/{len(sample_jokes)} ---")
            print(f"🎭 \"{joke}\"")
            print(f"📊 Current Level: {level}, Predicted: {rating['corniness_level']}")
            print(f"⭐ Quality: {rating['quality_score']}/100, Confidence: {rating['confidence']:.3f}")
            print(f"📏 Length: {len(joke)} chars")
            
            if rating['issues']:
                print(f"⚠️  Issues: {', '.join(rating['issues'])}")
            
            # Get user input
            while True:
                print(f"\\nCorrect level? (1-5, c=correct, s=skip, r=rubric, q=quit): ", end="")
                choice = input().strip().lower()
                
                if choice == 'q':
                    return corrections_made
                elif choice == 's':
                    break
                elif choice == 'c':
                    print("✅ Confirmed: Joke is correctly classified")
                    break
                elif choice == 'r':
                    self.show_rubric()
                    continue
                elif choice in ['1', '2', '3', '4', '5']:
                    correct_level = int(choice)
                    if correct_level != level:
                        self.corrections[joke] = {
                            'from_level': level,
                            'to_level': correct_level,
                            'pattern': f"manual_review_{level}"
                        }
                        print(f"✅ Noted: Move from Level {level} → Level {correct_level}")
                        corrections_made += 1
                    else:
                        print("✅ Confirmed: No change needed")
                    break
                else:
                    print("Invalid choice. Please enter 1-5, c, s, r, or q")
        
        return corrections_made
    
    def apply_corrections(self, backup: bool = True) -> Dict:
        """Apply the manual corrections to the database."""
        if not self.corrections:
            print("📝 No corrections to apply")
            return {'applied': 0}
        
        # Create backup if requested
        if backup:
            backup_file = self.jokes_file.replace('.json', '_backup_pre_reclassify.json')
            with open(self.jokes_file, 'r') as f:
                original_data = json.load(f)
            with open(backup_file, 'w') as f:
                json.dump(original_data, f, indent=2)
            print(f"💾 Backup created: {backup_file}")
        
        # Load current data
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        # Apply corrections
        applied_corrections = 0
        for joke, correction in self.corrections.items():
            from_level = str(correction['from_level'])
            to_level = str(correction['to_level'])
            
            # Remove from source level
            if from_level in jokes_data and joke in jokes_data[from_level]:
                jokes_data[from_level].remove(joke)
                
                # Add to target level
                if to_level not in jokes_data:
                    jokes_data[to_level] = []
                jokes_data[to_level].append(joke)
                
                applied_corrections += 1
                print(f"✅ Moved: \"{joke[:60]}...\" from L{from_level} → L{to_level}")
        
        # Save updated data
        with open(self.jokes_file, 'w') as f:
            json.dump(jokes_data, f, indent=2)
        
        print(f"\\n🎯 Applied {applied_corrections} corrections to database")
        
        # Clear corrections after applying
        self.corrections.clear()
        
        return {'applied': applied_corrections}
    
    def show_correction_summary(self):
        """Show summary of pending corrections."""
        if not self.corrections:
            print("📝 No pending corrections")
            return
        
        print(f"\\n📋 PENDING CORRECTIONS ({len(self.corrections)} jokes)")
        print("="*60)
        
        # Group by movement pattern
        movements = {}
        for joke, correction in self.corrections.items():
            pattern = f"{correction['from_level']}→{correction['to_level']}"
            if pattern not in movements:
                movements[pattern] = []
            movements[pattern].append(joke)
        
        for pattern, jokes in movements.items():
            print(f"\\n{pattern}: {len(jokes)} jokes")
            for joke in jokes[:3]:  # Show first 3 examples
                print(f"  • \"{joke[:60]}...\"")
            if len(jokes) > 3:
                print(f"  ... and {len(jokes)-3} more")
    
    def export_corrections(self, filename: str = "manual_corrections.json"):
        """Export corrections for review or backup."""
        with open(filename, 'w') as f:
            json.dump(self.corrections, f, indent=2)
        print(f"💾 Corrections exported to {filename}")


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manual joke classification review tool")
    parser.add_argument("--level", type=int, choices=[1,2,3,4,5], help="Review specific level")
    parser.add_argument("--pattern", help="Focus on specific misclassification pattern (e.g., '3->2')")
    parser.add_argument("--sample", type=int, default=10, help="Number of jokes to sample")
    parser.add_argument("--apply", action="store_true", help="Apply corrections after review")
    parser.add_argument("--rubric", action="store_true", help="Show corniness rubric and exit")
    
    args = parser.parse_args()
    
    reviewer = ManualReviewer()
    
    if args.rubric:
        reviewer.show_rubric()
        return
    
    print("🎭 Manual Joke Classification Review Tool")
    print("="*50)
    
    corrections_made = 0
    
    if args.level:
        corrections_made = reviewer.sample_review_by_level(args.level, args.sample)
    else:
        corrections_made = reviewer.review_misclassifications(args.pattern, args.sample)
    
    if corrections_made > 0:
        print(f"\\n📝 Made {corrections_made} correction(s)")
        reviewer.show_correction_summary()
        
        if args.apply:
            reviewer.apply_corrections()
        else:
            print("\\n💡 Use --apply flag to apply these corrections to the database")
    else:
        print("\\n✅ No corrections needed or made")


if __name__ == "__main__":
    main()