#!/usr/bin/env python3
"""
Automated joke rating and validation tool based on Punnyland quality rubric.

This tool helps classify jokes by corniness level and validates quality standards.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from rapidfuzz import fuzz


class JokeRater:
    """Rates jokes based on Punnyland quality rubric and corniness scale."""
    
    def __init__(self):
        # Quality requirements
        self.max_length = 180
        self.preferred_lengths = {
            1: 100,  # Mild chuckle
            2: 120,  # Dad approved  
            3: 140,  # Eye roll guaranteed
            4: 160,  # Groan zone
            5: 180   # Ultra corn
        }
        
        # Content filters
        self.forbidden_words = [
            # Profanity indicators (basic list)
            'damn', 'hell', 'crap', 'stupid', 'idiot', 'dumb',
            # Political terms
            'trump', 'biden', 'democrat', 'republican', 'politics',
            # Sensitive topics  
            'religion', 'god', 'jesus', 'muslim', 'christian', 'gay', 'lesbian'
        ]
        
        # Explanation markers
        self.explanation_markers = [
            'get it', 'because', 'you see', 'meaning', 'translation',
            'in other words', 'that is', 'just kidding', 'lol', 'haha'
        ]
        
        # Corniness indicators by level
        self.corniness_patterns = {
            1: {  # Mild chuckle - subtle
                'keywords': ['used to', 'then it', 'new word', 'invented'],
                'patterns': [r'I used to .+ but .+', r'.+ then .+'],
                'complexity': 'simple',
                'pun_density': 'low'
            },
            2: {  # Dad approved - classic format
                'keywords': ['why did', 'what do you call', 'how do you'],
                'patterns': [r'Why did .+\?', r'What do you call .+\?', r'How do you .+\?'],
                'complexity': 'standard',
                'pun_density': 'medium'
            },
            3: {  # Eye roll guaranteed - obvious puns
                'keywords': ['bear', 'cow', 'fish', 'call a', 'with no'],
                'patterns': [r'What do you call a .+ with no .+\?', r'Why don\'t .+ tell .+\?'],
                'complexity': 'obvious',
                'pun_density': 'medium'
            },
            4: {  # Groan zone - multiple puns
                'keywords': ['auto-tuna', 'moo-sician', 'addicted', 'turned myself around'],
                'patterns': [r'.+-\w+', r'.+ but .+ and .+'],
                'complexity': 'layered',
                'pun_density': 'high'
            },
            5: {  # Ultra corn - maximum puns
                'keywords': ['a-mew-sing', 'paws for concern', 'moo-d', 'beef with'],
                'patterns': [r'.+-\w+.+-\w+', r'.+!\s*.+!\s*.+!'],
                'complexity': 'excessive',
                'pun_density': 'maximum'
            }
        }
    
    def validate_content(self, joke: str) -> Tuple[bool, List[str]]:
        """Validate joke meets content standards."""
        issues = []
        
        # Length check
        if len(joke) > self.max_length:
            issues.append(f"Too long: {len(joke)} chars (max {self.max_length})")
        
        if len(joke) < 10:
            issues.append(f"Too short: {len(joke)} chars (min 10)")
        
        # Empty check
        if not joke.strip():
            issues.append("Empty joke")
        
        # Forbidden content
        joke_lower = joke.lower()
        for word in self.forbidden_words:
            if word in joke_lower:
                issues.append(f"Contains forbidden word: {word}")
        
        # Explanation markers
        for marker in self.explanation_markers:
            if marker in joke_lower:
                issues.append(f"Contains explanation: {marker}")
        
        # ASCII check
        try:
            joke.encode('ascii')
        except UnicodeEncodeError:
            # Allow some common unicode
            allowed_unicode = re.match(r'^[\x00-\x7F\u2013\u2014\u2018\u2019\u201C\u201D\u2026]*$', joke)
            if not allowed_unicode:
                issues.append("Contains non-ASCII characters")
        
        return len(issues) == 0, issues
    
    def count_puns(self, joke: str) -> int:
        """Count number of puns/wordplay elements in joke."""
        pun_indicators = [
            r'\w+-\w+',           # Hyphenated puns like "auto-tuna"
            r'\b\w*-\w*ing\b',    # -ing puns
            r'\b\w+\s+\w+\b',     # Sound-alike words
        ]
        
        pun_count = 0
        for pattern in pun_indicators:
            pun_count += len(re.findall(pattern, joke))
        
        # Also count obvious pun words
        pun_words = ['moo', 'paws', 'tail', 'purr', 'fur', 'bear', 'bee', 'sea', 'see']
        joke_lower = joke.lower()
        for word in pun_words:
            if word in joke_lower:
                pun_count += 1
        
        return min(pun_count, 5)  # Cap at 5
    
    def rate_corniness(self, joke: str) -> Tuple[int, float]:
        """
        Rate joke corniness level 1-5.
        
        Returns:
            Tuple of (level, confidence_score)
        """
        scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        joke_lower = joke.lower()
        
        # Check patterns and keywords for each level
        for level, indicators in self.corniness_patterns.items():
            # Keyword matching
            keyword_matches = sum(1 for kw in indicators['keywords'] if kw in joke_lower)
            scores[level] += keyword_matches * 2
            
            # Pattern matching
            pattern_matches = sum(1 for pattern in indicators['patterns'] 
                                if re.search(pattern, joke, re.IGNORECASE))
            scores[level] += pattern_matches * 3
        
        # Length-based scoring
        joke_len = len(joke)
        if joke_len <= 60:
            scores[1] += 1  # Short jokes tend to be subtle
        elif joke_len <= 100:
            scores[2] += 1  # Medium jokes are classic
        elif joke_len <= 140:
            scores[3] += 1  # Standard dad joke length
        elif joke_len <= 170:
            scores[4] += 1  # Longer jokes have more puns
        else:
            scores[5] += 2  # Very long jokes are ultra corn
        
        # Pun density scoring
        pun_count = self.count_puns(joke)
        if pun_count == 0:
            scores[1] += 2
        elif pun_count == 1:
            scores[2] += 2
        elif pun_count == 2:
            scores[3] += 2
        elif pun_count >= 3:
            scores[4] += 1
            scores[5] += 1
        
        # Question format scoring
        if joke.count('?') >= 1:
            scores[2] += 1
            scores[3] += 1
        
        if joke.count('?') >= 2 or joke.count('!') >= 2:
            scores[4] += 1
            scores[5] += 1
        
        # Find the highest scoring level
        best_level = max(scores, key=scores.get)
        max_score = scores[best_level]
        
        # Calculate confidence (0-1)
        total_score = sum(scores.values())
        confidence = max_score / max(total_score, 1)
        
        return best_level, confidence
    
    def rate_joke(self, joke: str) -> Dict:
        """Comprehensive joke rating."""
        # Content validation
        is_valid, issues = self.validate_content(joke)
        
        # Corniness rating
        level, confidence = self.rate_corniness(joke)
        
        # Quality score (0-100)
        quality_score = 100
        quality_score -= len(issues) * 10  # Deduct for issues
        quality_score -= max(0, len(joke) - self.preferred_lengths[level]) * 0.1  # Length penalty
        quality_score = max(0, min(100, quality_score))
        
        return {
            'joke': joke,
            'valid': is_valid,
            'issues': issues,
            'corniness_level': level,
            'confidence': round(confidence, 3),
            'quality_score': round(quality_score, 1),
            'length': len(joke),
            'pun_count': self.count_puns(joke),
            'recommendations': self._generate_recommendations(joke, level, issues)
        }
    
    def _generate_recommendations(self, joke: str, level: int, issues: List[str]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if len(joke) > self.preferred_lengths[level]:
            recommendations.append(f"Consider shortening (current: {len(joke)}, preferred: ≤{self.preferred_lengths[level]})")
        
        if issues:
            recommendations.append("Fix content issues before using")
        
        if self.count_puns(joke) == 0:
            recommendations.append("Consider adding wordplay or pun elements")
        
        if not any(marker in joke.lower() for marker in ['?', '!']):
            recommendations.append("Consider adding punctuation for emphasis")
        
        return recommendations
    
    def batch_rate(self, jokes: List[str]) -> List[Dict]:
        """Rate multiple jokes."""
        return [self.rate_joke(joke) for joke in jokes]
    
    def rate_database(self, jokes_file: str = "punnyland/data/jokes.json") -> Dict:
        """Rate entire jokes database."""
        with open(jokes_file, 'r') as f:
            jokes_data = json.load(f)
        
        results = {}
        total_stats = {
            'total_jokes': 0,
            'valid_jokes': 0,
            'average_quality': 0,
            'level_accuracy': 0
        }
        
        for level, joke_list in jokes_data.items():
            level_results = []
            correct_classifications = 0
            
            for joke in joke_list:
                rating = self.rate_joke(joke)
                level_results.append(rating)
                
                if rating['valid']:
                    total_stats['valid_jokes'] += 1
                
                if rating['corniness_level'] == int(level):
                    correct_classifications += 1
                    
                total_stats['average_quality'] += rating['quality_score']
                total_stats['total_jokes'] += 1
            
            results[level] = {
                'jokes': level_results,
                'count': len(joke_list),
                'accuracy': correct_classifications / len(joke_list) if joke_list else 0,
                'avg_quality': sum(r['quality_score'] for r in level_results) / len(level_results) if level_results else 0
            }
        
        # Calculate overall stats
        if total_stats['total_jokes'] > 0:
            total_stats['average_quality'] /= total_stats['total_jokes']
            total_stats['level_accuracy'] = sum(results[level]['accuracy'] * results[level]['count'] 
                                               for level in results) / total_stats['total_jokes']
        
        return {
            'by_level': results,
            'overall': total_stats
        }


def main():
    """Main function for command-line usage."""
    import sys
    
    rater = JokeRater()
    
    if len(sys.argv) > 1:
        # Rate single joke from command line
        joke = ' '.join(sys.argv[1:])
        result = rater.rate_joke(joke)
        
        print(f"🎭 Joke: \"{result['joke']}\"")
        print(f"✅ Valid: {result['valid']}")
        print(f"🌽 Corniness Level: {result['corniness_level']}")
        print(f"📊 Confidence: {result['confidence']}")
        print(f"⭐ Quality Score: {result['quality_score']}/100")
        print(f"📏 Length: {result['length']} chars")
        print(f"🎯 Pun Count: {result['pun_count']}")
        
        if result['issues']:
            print(f"⚠️  Issues: {', '.join(result['issues'])}")
        
        if result['recommendations']:
            print(f"💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"  • {rec}")
    else:
        # Rate entire database
        print("🔍 Rating entire jokes database...")
        results = rater.rate_database()
        
        print(f"\n📊 Overall Results:")
        print(f"Total Jokes: {results['overall']['total_jokes']}")
        print(f"Valid Jokes: {results['overall']['valid_jokes']}")
        print(f"Average Quality: {results['overall']['average_quality']:.1f}/100")
        print(f"Level Classification Accuracy: {results['overall']['level_accuracy']:.1%}")
        
        print(f"\n📈 By Level:")
        for level, data in results['by_level'].items():
            print(f"  Level {level}: {data['count']} jokes, "
                  f"{data['accuracy']:.1%} accurate, "
                  f"{data['avg_quality']:.1f} quality")


if __name__ == "__main__":
    main()