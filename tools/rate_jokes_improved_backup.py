#!/usr/bin/env python3
"""
Improved Joke Rating Tool

Enhanced classification algorithm based on actual joke patterns and manual review insights.
Focuses on joke structure, pun quality, and corniness indicators rather than just length.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ImprovedJokeRater:
    """Enhanced joke rater with better corniness classification."""
    
    def __init__(self):
        # Quality requirements (unchanged)
        self.max_length = 180
        self.min_length = 10
        
        # Content filters (unchanged)
        self.forbidden_words = [
            'damn', 'hell', 'crap', 'stupid', 'idiot', 'dumb',
            'trump', 'biden', 'democrat', 'republican', 'politics',
            'religion', 'god', 'jesus', 'muslim', 'christian', 'gay', 'lesbian'
        ]
        
        # Explanation markers (fixed - removed 'because' as it's part of many valid jokes)
        self.explanation_markers = [
            'get it', 'you see', 'meaning', 'translation',
            'in other words', 'that is', 'just kidding', 'lol', 'haha'
        ]
        
        # Improved corniness patterns based on actual joke structures
        self.level_patterns = {
            1: {  # Subtle wordplay, clever twists
                'setup_patterns': [
                    r'^I used to .+, but .+',
                    r'^Time flies like .+\. .+ flies like .+',
                    r'^I invented .+',
                    r'^The early bird .+, but .+',
                    r'^.+ used to .+, but .+'
                ],
                'pun_indicators': ['grew on', 'lost interest', 'time flies', 'invented'],
                'question_formats': [],  # Subtle jokes rarely use Q&A format
                'corniness_markers': [],  # Subtle jokes avoid obvious puns
                'length_preference': (20, 80),
                'base_score': 5  # Give Level 1 a higher base score
            },
            2: {  # Classic dad joke setups
                'setup_patterns': [
                    r'^Why don\'t .+\? .+',
                    r'^What do you call .+\? .+',
                    r'^How do you .+\? .+',
                    r'^Where do .+ go\? .+',
                    r'^Why did .+\? .+'
                ],
                'pun_indicators': ['make up everything', 'impasta', 'outstanding'],
                'question_formats': ['Why don\'t', 'What do you call', 'How do', 'Where do', 'Why did'],
                'corniness_markers': ['pun', 'play on words'],
                'length_preference': (40, 100),
                'base_score': 10
            },
            3: {  # Eye roll guaranteed - obvious puns
                'setup_patterns': [
                    r'^What do you call a .+ with no .+\?',
                    r'^What do you call .+\? .+bear!$',
                    r'^What do you call .+\? .+beef!$',
                    r'^Why don\'t .+ tell .+\?',
                    r'^What do you call .+opener.+\? .+can\'t opener'
                ],
                'pun_indicators': ['gummy bear', 'ground beef', 'can\'t opener', 'crack up'],
                'question_formats': ['What do you call'],
                'corniness_markers': ['obvious pun', '-ly', 'bear', 'beef', 'crack'],
                'length_preference': (45, 90),
                'base_score': 20
            },
            4: {  # Groan zone - heavy puns
                'setup_patterns': [
                    r'.*auto-tuna.*',
                    r'.*turned myself around.*',
                    r'.*addicted.*Hokey Pokey.*',
                    r'.*[a-z]+-[a-z]+.*'  # Hyphenated puns
                ],
                'pun_indicators': ['auto-tuna', 'turned myself around', 'hokey pokey'],
                'question_formats': [],
                'corniness_markers': ['-tuna', '-ing', 'addicted', 'turned around'],
                'length_preference': (60, 140),
                'base_score': 30
            },
            5: {  # Ultra corn - multiple stacked puns
                'setup_patterns': [
                    r'.*[a-z]+-[a-z]+.*[a-z]+-[a-z]+.*',  # Multiple hyphenated puns
                    r'.*paws.*fur.*tail.*',  # Multiple animal puns
                    r'.*moo.*udderly.*dairy.*'  # Multiple cow puns
                ],
                'pun_indicators': ['multiple puns', 'excessive wordplay', 'stacked puns'],
                'question_formats': [],
                'corniness_markers': ['multiple puns', 'excessive', 'stacked'],
                'length_preference': (80, 180),
                'base_score': 20
            }
        }
    
    def validate_content(self, joke: str) -> Tuple[bool, List[str]]:
        """Validate joke meets content standards (unchanged from original)."""
        issues = []
        
        if len(joke) > self.max_length:
            issues.append(f"Too long: {len(joke)} chars (max {self.max_length})")
        
        if len(joke) < self.min_length:
            issues.append(f"Too short: {len(joke)} chars (min {self.min_length})")
        
        if not joke.strip():
            issues.append("Empty joke")
        
        joke_lower = joke.lower()
        for word in self.forbidden_words:
            if word in joke_lower:
                issues.append(f"Contains forbidden word: {word}")
        
        for marker in self.explanation_markers:
            if marker in joke_lower:
                issues.append(f"Contains explanation: {marker}")
        
        # ASCII check with unicode allowances
        try:
            joke.encode('ascii')
        except UnicodeEncodeError:
            allowed_unicode = re.match(r'^[\x00-\x7F\u2013\u2014\u2018\u2019\u201C\u201D\u2026]*$', joke)
            if not allowed_unicode:
                issues.append("Contains non-ASCII characters")
        
        return len(issues) == 0, issues
    
    def count_actual_puns(self, joke: str) -> int:
        """More accurate pun counting focused on actual wordplay."""
        pun_count = 0
        joke_lower = joke.lower()
        
        # Hyphenated puns (strongest indicator)
        hyphenated_puns = len(re.findall(r'\b[a-z]+-[a-z]+\b', joke_lower))
        pun_count += hyphenated_puns * 2  # Weight these heavily
        
        # Sound-alike substitutions
        sound_alikes = [
            ('impasta', 'impostor'), ('gummy', 'gum'), ('ground beef', 'ground'),
            ('can\'t opener', 'can opener'), ('outstanding', 'out standing'),
            ('make up', 'makeup'), ('auto-tuna', 'auto tune')
        ]
        
        for pun_word, original in sound_alikes:
            if pun_word in joke_lower:
                pun_count += 1
        
        # Animal puns (common in corny jokes) - use word boundaries to avoid false matches
        animal_puns = ['\bmoo\b', '\bpaws\b', '\bfur\b', '\btail\b', '\bpurr\b', 'udderly', 'dairy', '\bbeef\b']
        animal_pun_count = sum(1 for pun in animal_puns if re.search(pun, joke_lower))
        if animal_pun_count > 2:  # Multiple animal puns = high corniness
            pun_count += 2
        elif animal_pun_count > 0:
            pun_count += 1
        
        # Wordplay indicators
        wordplay_phrases = [
            'grew on me', 'lost interest', 'time flies', 'crack up',
            'turned around', 'make up everything'
        ]
        
        for phrase in wordplay_phrases:
            if phrase in joke_lower:
                pun_count += 1
        
        return min(pun_count, 5)  # Cap at 5
    
    def analyze_joke_structure(self, joke: str) -> Dict:
        """Analyze the structural elements of the joke."""
        structure = {
            'has_question': '?' in joke,
            'question_count': joke.count('?'),
            'exclamation_count': joke.count('!'),
            'is_qa_format': bool(re.match(r'^(What|Why|How|Where|When).+\?.+', joke)),
            'setup_punchline': bool(re.match(r'^.+\?.+[!.]$', joke)),
            'length_category': 'short' if len(joke) < 60 else 'medium' if len(joke) < 120 else 'long'
        }
        
        return structure
    
    def rate_corniness_improved(self, joke: str) -> Tuple[int, float]:
        """
        Improved corniness rating based on actual joke patterns.
        
        Returns:
            Tuple of (level, confidence_score)
        """
        scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        joke_lower = joke.lower()
        structure = self.analyze_joke_structure(joke)
        
        # Pattern-based scoring (most important)
        for level, patterns in self.level_patterns.items():
            level_score = patterns['base_score']
            
            # Setup pattern matching (high weight)
            for pattern in patterns['setup_patterns']:
                if re.search(pattern, joke, re.IGNORECASE):
                    level_score += 15
                    break  # Only count one setup pattern match
            
            # Pun indicator matching (medium weight)
            pun_matches = sum(1 for indicator in patterns['pun_indicators'] 
                             if indicator in joke_lower)
            level_score += pun_matches * 8
            
            # Question format matching (medium weight)
            for q_format in patterns['question_formats']:
                if q_format.lower() in joke_lower:
                    level_score += 5
                    break
            
            # Corniness marker matching (low weight)
            corniness_matches = sum(1 for marker in patterns['corniness_markers']
                                  if marker in joke_lower)
            level_score += corniness_matches * 3
            
            # Length preference scoring (low weight)
            min_len, max_len = patterns['length_preference']
            if min_len <= len(joke) <= max_len:
                level_score += 3
            elif len(joke) < min_len:
                level_score -= 2
            elif len(joke) > max_len + 20:
                level_score -= 1
            
            scores[level] = level_score
        
        # Structural bonuses
        if structure['is_qa_format']:
            scores[2] += 5  # Q&A format is classic Level 2
            scores[3] += 3  # Also common in Level 3
        
        # Pun density adjustments
        actual_pun_count = self.count_actual_puns(joke)
        if actual_pun_count == 0:
            scores[1] += 8  # Likely subtle wordplay
        elif actual_pun_count == 1:
            scores[2] += 5  # Classic single pun
            scores[3] += 3
        elif actual_pun_count == 2:
            scores[3] += 6  # Obvious pun territory
            scores[4] += 3
        elif actual_pun_count >= 3:
            scores[4] += 6  # Heavy pun density
            scores[5] += 4
        
        # Specific joke pattern overrides (based on manual review)
        if 'can\'t opener' in joke_lower:
            scores[3] += 10  # Classic Level 3 joke
        
        if 'gummy bear' in joke_lower:
            scores[3] += 10  # Classic Level 3 joke
        
        if 'ground beef' in joke_lower:
            scores[3] += 10  # Classic Level 3 joke
        
        if 'auto-tuna' in joke_lower or 'hokey pokey' in joke_lower:
            scores[4] += 10  # Classic Level 4 jokes
        
        # Find the highest scoring level
        best_level = max(scores, key=scores.get)
        max_score = scores[best_level]
        
        # Calculate confidence (0-1)
        total_score = sum(scores.values())
        confidence = max_score / max(total_score, 1) if total_score > 0 else 0.1
        
        # Boost confidence for strong pattern matches
        if max_score >= 20:
            confidence = min(1.0, confidence * 1.2)
        
        return best_level, confidence
    
    def rate_joke(self, joke: str) -> Dict:
        """Comprehensive joke rating with improved algorithm."""
        # Content validation
        is_valid, issues = self.validate_content(joke)
        
        # Improved corniness rating
        level, confidence = self.rate_corniness_improved(joke)
        
        # Quality score calculation
        quality_score = 100
        quality_score -= len(issues) * 10  # Deduct for issues
        
        # Adjust for length vs level expectations
        expected_ranges = {1: 80, 2: 100, 3: 90, 4: 140, 5: 180}
        if len(joke) > expected_ranges[level]:
            quality_score -= (len(joke) - expected_ranges[level]) * 0.1
        
        quality_score = max(0, min(100, quality_score))
        
        return {
            'joke': joke,
            'valid': is_valid,
            'issues': issues,
            'corniness_level': level,
            'confidence': round(confidence, 3),
            'quality_score': round(quality_score, 1),
            'length': len(joke),
            'pun_count': self.count_actual_puns(joke),
            'structure': self.analyze_joke_structure(joke),
            'recommendations': self._generate_recommendations(joke, level, issues)
        }
    
    def _generate_recommendations(self, joke: str, level: int, issues: List[str]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        expected_lengths = {1: 80, 2: 100, 3: 90, 4: 140, 5: 180}
        if len(joke) > expected_lengths[level]:
            recommendations.append(f"Consider shortening (current: {len(joke)}, preferred: ≤{expected_lengths[level]})")
        
        if issues:
            recommendations.append("Fix content issues before using")
        
        pun_count = self.count_actual_puns(joke)
        if pun_count == 0 and level > 1:
            recommendations.append("Consider adding wordplay elements")
        
        if not any(marker in joke for marker in ['?', '!']):
            recommendations.append("Consider adding punctuation for emphasis")
        
        return recommendations
    
    def batch_rate(self, jokes: List[str]) -> List[Dict]:
        """Rate multiple jokes."""
        return [self.rate_joke(joke) for joke in jokes]


def main():
    """Main function for command-line usage."""
    import sys
    
    rater = ImprovedJokeRater()
    
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
        print(f"🎯 Actual Pun Count: {result['pun_count']}")
        
        if result['issues']:
            print(f"⚠️  Issues: {', '.join(result['issues'])}")
        
        if result['recommendations']:
            print(f"💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"  • {rec}")
    else:
        print("Usage: python improved_rater.py \"Your joke here\"")


if __name__ == "__main__":
    main()