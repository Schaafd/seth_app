#!/usr/bin/env python3
"""
Automated Joke Reclassification Tool

Automatically reclassifies jokes based on the improved classifier's predictions.
Uses confidence thresholds to determine which jokes to move.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict, Counter

# Add the parent directory to Python path to import tools
sys.path.append(str(Path(__file__).parent))
from rate_jokes import JokeRater


class AutoReclassifier:
    """Automatically reclassifies jokes based on improved classifier predictions."""
    
    def __init__(self, jokes_file: str = "punnyland/data/jokes.json"):
        self.jokes_file = jokes_file
        self.rater = JokeRater()
        
    def analyze_reclassification_candidates(self, min_confidence: float = 0.4) -> Dict:
        """Analyze which jokes should be reclassified based on confidence thresholds."""
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        reclassification_plan = {
            'high_confidence': [],  # >= 0.6 confidence
            'medium_confidence': [],  # 0.4-0.6 confidence
            'low_confidence': [],  # < 0.4 confidence
            'already_correct': [],
            'statistics': defaultdict(int)
        }
        
        print("🔍 Analyzing reclassification candidates...")
        
        total_jokes = 0
        for actual_level, joke_list in jokes_data.items():
            for joke in joke_list:
                rating = self.rater.rate_joke(joke)
                predicted_level = rating['corniness_level']
                confidence = rating['confidence']
                total_jokes += 1
                
                candidate = {
                    'joke': joke,
                    'from_level': int(actual_level),
                    'to_level': predicted_level,
                    'confidence': confidence,
                    'quality_score': rating['quality_score'],
                    'valid': rating['valid']
                }
                
                if predicted_level == int(actual_level):
                    reclassification_plan['already_correct'].append(candidate)
                    reclassification_plan['statistics']['correct'] += 1
                else:
                    # Needs reclassification
                    pattern = f"{actual_level}->{predicted_level}"
                    reclassification_plan['statistics'][pattern] += 1
                    
                    if confidence >= 0.6:
                        reclassification_plan['high_confidence'].append(candidate)
                        reclassification_plan['statistics']['high_conf_moves'] += 1
                    elif confidence >= min_confidence:
                        reclassification_plan['medium_confidence'].append(candidate)
                        reclassification_plan['statistics']['medium_conf_moves'] += 1
                    else:
                        reclassification_plan['low_confidence'].append(candidate)
                        reclassification_plan['statistics']['low_conf_moves'] += 1
        
        reclassification_plan['statistics']['total_jokes'] = total_jokes
        reclassification_plan['statistics']['accuracy'] = (
            reclassification_plan['statistics']['correct'] / total_jokes * 100
        )
        
        return reclassification_plan
    
    def print_reclassification_summary(self, plan: Dict):
        """Print a summary of the reclassification plan."""
        stats = plan['statistics']
        
        print("\n" + "="*80)
        print("📊 AUTOMATED RECLASSIFICATION ANALYSIS")
        print("="*80)
        
        print(f"\n📈 Overall Statistics:")
        print(f"  Total Jokes: {stats['total_jokes']}")
        print(f"  Currently Correct: {stats['correct']} ({stats['accuracy']:.1f}%)")
        print(f"  Need Reclassification: {stats['total_jokes'] - stats['correct']}")
        
        print(f"\n🎯 Reclassification Confidence Breakdown:")
        print(f"  High Confidence (≥0.6): {stats['high_conf_moves']} jokes")
        print(f"  Medium Confidence (0.4-0.6): {stats['medium_conf_moves']} jokes")
        print(f"  Low Confidence (<0.4): {stats['low_conf_moves']} jokes")
        
        print(f"\n🔄 Most Common Reclassification Patterns:")
        patterns = [(k, v) for k, v in stats.items() if '->' in k]
        patterns.sort(key=lambda x: x[1], reverse=True)
        
        for pattern, count in patterns[:10]:
            print(f"  {pattern}: {count} jokes")
        
        print(f"\n💡 Recommendation Summary:")
        safe_moves = stats['high_conf_moves'] + stats['medium_conf_moves']
        print(f"  Safe to auto-move: {safe_moves} jokes (≥0.4 confidence)")
        print(f"  Questionable moves: {stats['low_conf_moves']} jokes (<0.4 confidence)")
    
    def show_examples(self, plan: Dict, category: str = "high_confidence", limit: int = 5):
        """Show examples from a specific reclassification category."""
        if category not in plan:
            print(f"❌ Category '{category}' not found")
            return
        
        candidates = plan[category]
        if not candidates:
            print(f"📝 No candidates in category '{category}'")
            return
        
        print(f"\n" + "="*80)
        print(f"📝 EXAMPLES: {category.upper().replace('_', ' ')} ({len(candidates)} total)")
        print("="*80)
        
        for i, candidate in enumerate(candidates[:limit]):
            print(f"\n{i+1}. 🎭 \"{candidate['joke'][:70]}{'...' if len(candidate['joke']) > 70 else ''}\"")
            print(f"   📊 Move: L{candidate['from_level']} → L{candidate['to_level']}")
            print(f"   📈 Confidence: {candidate['confidence']:.3f}, Quality: {candidate['quality_score']}/100")
        
        if len(candidates) > limit:
            print(f"\n... and {len(candidates) - limit} more candidates")
    
    def apply_reclassification(self, plan: Dict, min_confidence: float = 0.4, 
                             backup: bool = True, dry_run: bool = False) -> Dict:
        """Apply the reclassification plan to the database."""
        
        if backup and not dry_run:
            backup_file = self.jokes_file.replace('.json', '_backup_pre_reclassify.json')
            with open(self.jokes_file, 'r') as f:
                original_data = json.load(f)
            with open(backup_file, 'w') as f:
                json.dump(original_data, f, indent=2)
            print(f"💾 Backup created: {backup_file}")
        
        # Collect candidates to move
        candidates_to_move = []
        candidates_to_move.extend(plan['high_confidence'])
        
        # Add medium confidence candidates if they meet minimum threshold
        for candidate in plan['medium_confidence']:
            if candidate['confidence'] >= min_confidence:
                candidates_to_move.append(candidate)
        
        print(f"\n🔄 Processing {len(candidates_to_move)} reclassification moves...")
        
        if dry_run:
            print("🧪 DRY RUN MODE - No actual changes will be made")
            
            # Show what would be moved
            moves_by_pattern = defaultdict(int)
            for candidate in candidates_to_move:
                pattern = f"{candidate['from_level']}->{candidate['to_level']}"
                moves_by_pattern[pattern] += 1
            
            print(f"\n📋 Would make the following moves:")
            for pattern, count in sorted(moves_by_pattern.items()):
                print(f"  {pattern}: {count} jokes")
            
            return {
                'dry_run': True,
                'would_move': len(candidates_to_move),
                'patterns': dict(moves_by_pattern)
            }
        
        # Load current data
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        # Apply moves
        moves_applied = 0
        moves_by_pattern = defaultdict(int)
        
        for candidate in candidates_to_move:
            joke = candidate['joke']
            from_level = str(candidate['from_level'])
            to_level = str(candidate['to_level'])
            
            # Remove from source level
            if from_level in jokes_data and joke in jokes_data[from_level]:
                jokes_data[from_level].remove(joke)
                
                # Add to target level (create level if it doesn't exist)
                if to_level not in jokes_data:
                    jokes_data[to_level] = []
                jokes_data[to_level].append(joke)
                
                moves_applied += 1
                pattern = f"{from_level}->{to_level}"
                moves_by_pattern[pattern] += 1
                
                print(f"✅ Moved: \"{joke[:50]}{'...' if len(joke) > 50 else ''}\" L{from_level}→L{to_level}")
        
        # Save updated data
        with open(self.jokes_file, 'w') as f:
            json.dump(jokes_data, f, indent=2)
        
        print(f"\n🎯 Reclassification Complete!")
        print(f"   Moves Applied: {moves_applied}")
        print(f"   Patterns:")
        for pattern, count in sorted(moves_by_pattern.items()):
            print(f"     {pattern}: {count} jokes")
        
        return {
            'moves_applied': moves_applied,
            'patterns': dict(moves_by_pattern)
        }
    
    def get_post_reclassification_stats(self) -> Dict:
        """Get database statistics after reclassification."""
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        stats = {}
        total_jokes = 0
        
        for level, joke_list in jokes_data.items():
            count = len(joke_list)
            stats[level] = count
            total_jokes += count
        
        stats['total'] = total_jokes
        return stats


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated joke reclassification tool")
    parser.add_argument("--min-confidence", type=float, default=0.4,
                       help="Minimum confidence threshold for reclassification (default: 0.4)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be reclassified without making changes")
    parser.add_argument("--no-backup", action="store_true",
                       help="Skip creating backup file")
    parser.add_argument("--examples", choices=["high_confidence", "medium_confidence", "low_confidence"],
                       help="Show examples from specific confidence category")
    parser.add_argument("--file", default="punnyland/data/jokes.json",
                       help="Jokes file to reclassify")
    
    args = parser.parse_args()
    
    reclassifier = AutoReclassifier(args.file)
    
    print("🎭 Automated Joke Reclassification Tool")
    print("=" * 50)
    
    # Analyze reclassification candidates
    plan = reclassifier.analyze_reclassification_candidates(args.min_confidence)
    
    # Print summary
    reclassifier.print_reclassification_summary(plan)
    
    # Show examples if requested
    if args.examples:
        reclassifier.show_examples(plan, args.examples)
        return
    
    # Apply reclassification
    if args.dry_run:
        result = reclassifier.apply_reclassification(
            plan, args.min_confidence, backup=not args.no_backup, dry_run=True
        )
    else:
        print(f"\n🚀 Proceeding with automated reclassification...")
        print(f"   Min confidence threshold: {args.min_confidence}")
        print(f"   Backup: {'No' if args.no_backup else 'Yes'}")
        
        result = reclassifier.apply_reclassification(
            plan, args.min_confidence, backup=not args.no_backup, dry_run=False
        )
        
        # Show post-reclassification stats
        if not args.dry_run:
            print(f"\n📊 Updated Database Statistics:")
            new_stats = reclassifier.get_post_reclassification_stats()
            for level in sorted(new_stats.keys()):
                if level != 'total':
                    print(f"  Level {level}: {new_stats[level]} jokes")
            print(f"  Total: {new_stats['total']} jokes")


if __name__ == "__main__":
    main()