#!/usr/bin/env python3
"""
Joke Classification Analysis Tool

Analyzes classification accuracy issues and provides detailed examples
of misclassified jokes for manual review and algorithm improvement.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

# Add the parent directory to Python path to import the rating tool
sys.path.append(str(Path(__file__).parent))
from rate_jokes import JokeRater


class ClassificationAnalyzer:
    """Analyzes joke classification accuracy and identifies issues."""
    
    def __init__(self, jokes_file: str = "punnyland/data/jokes.json"):
        self.jokes_file = jokes_file
        self.rater = JokeRater()
        self.results = None
        
    def load_and_analyze(self):
        """Load jokes and perform comprehensive analysis."""
        print("🔍 Loading and analyzing jokes database...")
        
        with open(self.jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        # Rate all jokes and collect detailed results
        detailed_results = {}
        misclassifications = defaultdict(list)
        invalid_jokes = defaultdict(list)
        quality_issues = defaultdict(list)
        
        for actual_level, joke_list in jokes_data.items():
            level_analysis = []
            
            for joke in joke_list:
                rating = self.rater.rate_joke(joke)
                predicted_level = rating['corniness_level']
                
                # Store detailed result
                analysis_data = {
                    'joke': joke,
                    'actual_level': int(actual_level),
                    'predicted_level': predicted_level,
                    'confidence': rating['confidence'],
                    'quality_score': rating['quality_score'],
                    'valid': rating['valid'],
                    'issues': rating['issues'],
                    'length': rating['length'],
                    'pun_count': rating['pun_count'],
                    'recommendations': rating['recommendations']
                }
                level_analysis.append(analysis_data)
                
                # Collect problematic cases
                if not rating['valid']:
                    invalid_jokes[actual_level].append(analysis_data)
                
                if rating['quality_score'] < 90:
                    quality_issues[actual_level].append(analysis_data)
                
                if predicted_level != int(actual_level):
                    misclassifications[f"{actual_level}->{predicted_level}"].append(analysis_data)
            
            detailed_results[actual_level] = level_analysis
        
        self.results = {
            'detailed_results': detailed_results,
            'misclassifications': dict(misclassifications),
            'invalid_jokes': dict(invalid_jokes),
            'quality_issues': dict(quality_issues)
        }
        
        return self.results
    
    def print_summary(self):
        """Print comprehensive summary of analysis."""
        if not self.results:
            self.load_and_analyze()
        
        print("\n" + "="*80)
        print("📊 JOKE CLASSIFICATION ANALYSIS SUMMARY")
        print("="*80)
        
        # Overall statistics
        total_jokes = sum(len(jokes) for jokes in self.results['detailed_results'].values())
        total_invalid = sum(len(jokes) for jokes in self.results['invalid_jokes'].values())
        total_misclassified = sum(len(jokes) for jokes in self.results['misclassifications'].values())
        
        print(f"\n📈 Overall Statistics:")
        print(f"  Total Jokes: {total_jokes}")
        print(f"  Invalid Jokes: {total_invalid} ({total_invalid/total_jokes*100:.1f}%)")
        print(f"  Misclassified: {total_misclassified} ({total_misclassified/total_jokes*100:.1f}%)")
        
        # Level-by-level accuracy
        print(f"\n🎯 Classification Accuracy by Level:")
        for level, jokes in self.results['detailed_results'].items():
            correct = sum(1 for j in jokes if j['predicted_level'] == j['actual_level'])
            accuracy = correct / len(jokes) * 100 if jokes else 0
            avg_quality = sum(j['quality_score'] for j in jokes) / len(jokes) if jokes else 0
            invalid_count = len([j for j in jokes if not j['valid']])
            
            print(f"  Level {level}: {correct}/{len(jokes)} correct ({accuracy:.1f}% accuracy)")
            print(f"    Average Quality: {avg_quality:.1f}/100")
            print(f"    Invalid Jokes: {invalid_count}")
        
        # Most common misclassifications
        print(f"\n🔄 Most Common Misclassifications:")
        misclass_counts = {k: len(v) for k, v in self.results['misclassifications'].items()}
        for pattern, count in sorted(misclass_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {pattern}: {count} jokes")
    
    def show_examples(self, category: str, level: str = None, limit: int = 5):
        """Show specific examples of problematic jokes."""
        if not self.results:
            self.load_and_analyze()
        
        print(f"\n" + "="*80)
        print(f"📝 EXAMPLES: {category.upper()}")
        print("="*80)
        
        if category == "misclassifications":
            for pattern, jokes in self.results['misclassifications'].items():
                if level and not pattern.startswith(level):
                    continue
                    
                print(f"\n🔄 {pattern} ({len(jokes)} total):")
                for i, joke_data in enumerate(jokes[:limit]):
                    self._print_joke_details(joke_data, i+1)
                    
        elif category == "invalid":
            target_level = level or "5"  # Default to level 5 which has most invalid
            if target_level in self.results['invalid_jokes']:
                jokes = self.results['invalid_jokes'][target_level]
                print(f"\n❌ Invalid Level {target_level} Jokes ({len(jokes)} total):")
                for i, joke_data in enumerate(jokes[:limit]):
                    self._print_joke_details(joke_data, i+1)
        
        elif category == "quality_issues":
            target_level = level or "5"
            if target_level in self.results['quality_issues']:
                jokes = self.results['quality_issues'][target_level]
                print(f"\n⚠️  Low Quality Level {target_level} Jokes ({len(jokes)} total):")
                for i, joke_data in enumerate(jokes[:limit]):
                    self._print_joke_details(joke_data, i+1)
    
    def _print_joke_details(self, joke_data: Dict, index: int):
        """Print detailed information about a joke."""
        print(f"\n  {index}. 🎭 \"{joke_data['joke']}\"")
        print(f"     📊 Actual: L{joke_data['actual_level']}, Predicted: L{joke_data['predicted_level']}")
        print(f"     ⭐ Quality: {joke_data['quality_score']}/100, Confidence: {joke_data['confidence']:.3f}")
        print(f"     📏 Length: {joke_data['length']} chars, Puns: {joke_data['pun_count']}")
        
        if joke_data['issues']:
            print(f"     ❌ Issues: {', '.join(joke_data['issues'])}")
        
        if joke_data['recommendations']:
            print(f"     💡 Recommendations: {'; '.join(joke_data['recommendations'])}")
    
    def export_for_review(self, output_file: str = "classification_analysis.json"):
        """Export detailed analysis for manual review."""
        if not self.results:
            self.load_and_analyze()
        
        # Create simplified export for easier review
        export_data = {
            'summary': {
                'total_jokes': sum(len(jokes) for jokes in self.results['detailed_results'].values()),
                'invalid_count': sum(len(jokes) for jokes in self.results['invalid_jokes'].values()),
                'misclassified_count': sum(len(jokes) for jokes in self.results['misclassifications'].values())
            },
            'worst_misclassifications': {},
            'invalid_by_level': {},
            'recommended_actions': []
        }
        
        # Get worst misclassification patterns
        misclass_counts = {k: len(v) for k, v in self.results['misclassifications'].items()}
        for pattern, count in sorted(misclass_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            export_data['worst_misclassifications'][pattern] = {
                'count': count,
                'examples': [j['joke'] for j in self.results['misclassifications'][pattern][:10]]
            }
        
        # Get invalid jokes by level
        for level, jokes in self.results['invalid_jokes'].items():
            export_data['invalid_by_level'][level] = {
                'count': len(jokes),
                'examples': [{'joke': j['joke'], 'issues': j['issues']} for j in jokes[:10]]
            }
        
        # Generate recommendations
        if '3' in self.results['invalid_jokes'] and len(self.results['invalid_jokes']['3']) > 20:
            export_data['recommended_actions'].append("High priority: Review Level 3 classification criteria")
        
        if '5' in self.results['invalid_jokes'] and len(self.results['invalid_jokes']['5']) > 10:
            export_data['recommended_actions'].append("Clean up Level 5 invalid jokes")
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n💾 Detailed analysis exported to {output_file}")
        return export_data


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze joke classification accuracy")
    parser.add_argument("--examples", choices=["misclassifications", "invalid", "quality_issues"], 
                       help="Show examples of specific category")
    parser.add_argument("--level", help="Filter examples to specific level")
    parser.add_argument("--limit", type=int, default=5, help="Limit number of examples shown")
    parser.add_argument("--export", action="store_true", help="Export analysis to JSON")
    
    args = parser.parse_args()
    
    analyzer = ClassificationAnalyzer()
    
    # Always show summary
    analyzer.print_summary()
    
    # Show specific examples if requested
    if args.examples:
        analyzer.show_examples(args.examples, args.level, args.limit)
    
    # Export if requested
    if args.export:
        analyzer.export_for_review()


if __name__ == "__main__":
    main()