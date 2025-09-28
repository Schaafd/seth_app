#!/usr/bin/env python3
"""
Comprehensive jokes database audit tool for Punnyland.

This tool validates the jokes database against the schema, detects duplicates,
checks for quality issues, and generates detailed reports.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime
import difflib

try:
    import jsonschema
    from rapidfuzz import fuzz
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema", "rapidfuzz"])
    import jsonschema
    from rapidfuzz import fuzz


class JokesAuditor:
    """Comprehensive auditor for the Punnyland jokes database."""
    
    def __init__(self):
        self.schema_path = Path("schemas/jokes.schema.json")
        self.jokes_path = Path("punnyland/data/jokes.json")
        self.reports_path = Path("reports")
        self.reports_path.mkdir(exist_ok=True)
        
        # Quality thresholds
        self.duplicate_threshold = 85  # Fuzzy match threshold
        self.max_length = 180
        self.min_length = 10
        
        # Load schema and jokes
        self.schema = self._load_schema()
        self.jokes = self._load_jokes()
    
    def _load_schema(self) -> dict:
        """Load the JSON schema."""
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        
        with open(self.schema_path, 'r') as f:
            return json.load(f)
    
    def _load_jokes(self) -> dict:
        """Load the jokes database."""
        if not self.jokes_path.exists():
            raise FileNotFoundError(f"Jokes file not found: {self.jokes_path}")
        
        with open(self.jokes_path, 'r') as f:
            return json.load(f)
    
    def validate_schema(self) -> Dict:
        """Validate jokes database against JSON schema."""
        result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }
        
        try:
            jsonschema.validate(self.jokes, self.schema)
            result['valid'] = True
        except jsonschema.ValidationError as e:
            result['errors'].append({
                'message': str(e.message),
                'path': list(e.absolute_path),
                'invalid_value': str(e.instance)[:100] if e.instance else None
            })
        except jsonschema.SchemaError as e:
            result['errors'].append({
                'message': f"Schema error: {e.message}",
                'path': [],
                'invalid_value': None
            })
        
        return result
    
    def detect_duplicates(self) -> Dict:
        """Detect duplicate jokes using fuzzy matching."""
        all_jokes = []
        duplicates = []
        
        # Collect all jokes with metadata
        for level, joke_list in self.jokes.items():
            for idx, joke in enumerate(joke_list):
                all_jokes.append({
                    'level': level,
                    'index': idx,
                    'joke': joke,
                    'normalized': self._normalize_joke(joke)
                })
        
        # Find duplicates
        for i, joke1 in enumerate(all_jokes):
            for j, joke2 in enumerate(all_jokes[i+1:], i+1):
                similarity = fuzz.token_set_ratio(
                    joke1['normalized'], 
                    joke2['normalized']
                )
                
                if similarity >= self.duplicate_threshold:
                    duplicates.append({
                        'similarity': similarity,
                        'joke1': {
                            'level': joke1['level'],
                            'index': joke1['index'],
                            'text': joke1['joke']
                        },
                        'joke2': {
                            'level': joke2['level'],
                            'index': joke2['index'],
                            'text': joke2['joke']
                        }
                    })
        
        return {
            'total_comparisons': len(all_jokes) * (len(all_jokes) - 1) // 2,
            'duplicates_found': len(duplicates),
            'duplicates': duplicates
        }
    
    def _normalize_joke(self, joke: str) -> str:
        """Normalize joke for comparison."""
        # Convert to lowercase
        normalized = joke.lower()
        
        # Remove punctuation except apostrophes
        normalized = re.sub(r"[^\w\s']", " ", normalized)
        
        # Collapse whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def analyze_quality(self) -> Dict:
        """Analyze joke quality metrics."""
        quality_issues = {
            'too_short': [],
            'too_long': [],
            'contains_explanations': [],
            'empty_strings': [],
            'suspicious_characters': []
        }
        
        # Quality patterns to check
        explanation_patterns = [
            r'\b(because|get it|you see|that\'?s why|meaning|translation|in other words)\b',
            r'\(.*?(get it|because|translation).*?\)',
            r'\blol\b|\bhaha+\b',
            r'!{2,}|\.{3,}'
        ]
        
        for level, joke_list in self.jokes.items():
            for idx, joke in enumerate(joke_list):
                joke_info = {'level': level, 'index': idx, 'joke': joke}
                
                # Length checks
                if len(joke) < self.min_length:
                    quality_issues['too_short'].append(joke_info)
                
                if len(joke) > self.max_length:
                    joke_info['length'] = len(joke)
                    quality_issues['too_long'].append(joke_info)
                
                # Empty string check
                if not joke.strip():
                    quality_issues['empty_strings'].append(joke_info)
                
                # Explanation checks
                for pattern in explanation_patterns:
                    if re.search(pattern, joke, re.IGNORECASE):
                        joke_info['pattern'] = pattern
                        quality_issues['contains_explanations'].append(joke_info)
                        break
                
                # Character encoding check
                try:
                    joke.encode('ascii')
                except UnicodeEncodeError:
                    # Check if it's just allowed unicode characters
                    allowed_unicode = re.match(r'^[\x00-\x7F\u2013\u2014\u2018\u2019\u201C\u201D\u2026]*$', joke)
                    if not allowed_unicode:
                        quality_issues['suspicious_characters'].append(joke_info)
        
        return quality_issues
    
    def analyze_distribution(self) -> Dict:
        """Analyze joke distribution across levels."""
        distribution = {}
        total_jokes = sum(len(joke_list) for joke_list in self.jokes.values())
        
        for level, joke_list in self.jokes.items():
            count = len(joke_list)
            percentage = (count / total_jokes) * 100 if total_jokes > 0 else 0
            
            distribution[level] = {
                'count': count,
                'percentage': percentage,
                'avg_length': sum(len(joke) for joke in joke_list) / count if count > 0 else 0,
                'min_length': min(len(joke) for joke in joke_list) if count > 0 else 0,
                'max_length': max(len(joke) for joke in joke_list) if count > 0 else 0
            }
        
        return {
            'total_jokes': total_jokes,
            'by_level': distribution,
            'balance_score': self._calculate_balance_score(distribution)
        }
    
    def _calculate_balance_score(self, distribution: Dict) -> float:
        """Calculate how balanced the distribution is (0-100)."""
        if not distribution:
            return 0.0
        
        percentages = [data['percentage'] for data in distribution.values()]
        ideal_percentage = 100.0 / len(percentages)
        
        # Calculate deviation from ideal
        deviations = [abs(p - ideal_percentage) for p in percentages]
        avg_deviation = sum(deviations) / len(deviations)
        
        # Convert to score (lower deviation = higher score)
        balance_score = max(0, 100 - (avg_deviation * 2))
        return round(balance_score, 2)
    
    def run_full_audit(self) -> Dict:
        """Run comprehensive audit and return results."""
        print("🔍 Running comprehensive Punnyland jokes audit...")
        
        # Schema validation
        print("  📋 Validating against JSON schema...")
        schema_results = self.validate_schema()
        
        # Duplicate detection  
        print("  🔄 Detecting duplicates...")
        duplicate_results = self.detect_duplicates()
        
        # Quality analysis
        print("  ✨ Analyzing quality metrics...")
        quality_results = self.analyze_quality()
        
        # Distribution analysis
        print("  📊 Analyzing distribution...")
        distribution_results = self.analyze_distribution()
        
        # Compile full report
        report = {
            'audit_timestamp': datetime.now().isoformat(),
            'database_file': str(self.jokes_path),
            'schema_file': str(self.schema_path),
            'schema_validation': schema_results,
            'duplicate_analysis': duplicate_results,
            'quality_analysis': quality_results,
            'distribution_analysis': distribution_results,
            'summary': self._generate_summary(
                schema_results, duplicate_results, 
                quality_results, distribution_results
            )
        }
        
        return report
    
    def _generate_summary(self, schema_results, duplicate_results, 
                         quality_results, distribution_results) -> Dict:
        """Generate executive summary of audit results."""
        total_issues = (
            len(schema_results['errors']) +
            duplicate_results['duplicates_found'] +
            sum(len(issues) for issues in quality_results.values())
        )
        
        quality_score = max(0, 100 - min(100, total_issues * 2))
        
        return {
            'overall_status': 'PASS' if total_issues == 0 else 'ISSUES_FOUND',
            'quality_score': quality_score,
            'total_jokes': distribution_results['total_jokes'],
            'schema_valid': schema_results['valid'],
            'duplicates_found': duplicate_results['duplicates_found'],
            'quality_issues': sum(len(issues) for issues in quality_results.values()),
            'distribution_balance': distribution_results['balance_score'],
            'recommendations': self._generate_recommendations(
                schema_results, duplicate_results, quality_results
            )
        }
    
    def _generate_recommendations(self, schema_results, duplicate_results, quality_results) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if not schema_results['valid']:
            recommendations.append("Fix schema validation errors before proceeding")
        
        if duplicate_results['duplicates_found'] > 0:
            recommendations.append(f"Remove or review {duplicate_results['duplicates_found']} potential duplicate jokes")
        
        if quality_results['too_long']:
            recommendations.append(f"Shorten {len(quality_results['too_long'])} jokes that exceed 180 characters")
        
        if quality_results['contains_explanations']:
            recommendations.append(f"Remove explanations from {len(quality_results['contains_explanations'])} jokes")
        
        if quality_results['empty_strings']:
            recommendations.append(f"Replace {len(quality_results['empty_strings'])} empty joke entries")
        
        if not recommendations:
            recommendations.append("Database quality looks excellent! No major issues found.")
        
        return recommendations
    
    def save_report(self, report: Dict, filename: str = None) -> str:
        """Save audit report to file."""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"audit_report_{timestamp}.json"
        
        report_path = self.reports_path / filename
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return str(report_path)


def main():
    """Main function to run the audit."""
    try:
        auditor = JokesAuditor()
        report = auditor.run_full_audit()
        
        # Save report
        report_file = auditor.save_report(report, "audit_initial.json")
        
        # Print summary
        summary = report['summary']
        print(f"\n{'='*60}")
        print("🎭 PUNNYLAND JOKES DATABASE AUDIT RESULTS 🎭")
        print(f"{'='*60}")
        print(f"📊 Total Jokes: {summary['total_jokes']}")
        print(f"✅ Schema Valid: {summary['schema_valid']}")
        print(f"🔄 Duplicates Found: {summary['duplicates_found']}")
        print(f"⚠️  Quality Issues: {summary['quality_issues']}")
        print(f"📈 Quality Score: {summary['quality_score']}/100")
        print(f"⚖️  Distribution Balance: {summary['distribution_balance']}/100")
        print(f"🎯 Overall Status: {summary['overall_status']}")
        
        print(f"\n📝 Recommendations:")
        for i, rec in enumerate(summary['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print(f"\n💾 Full report saved to: {report_file}")
        
        return 0 if summary['overall_status'] == 'PASS' else 1
        
    except Exception as e:
        print(f"❌ Audit failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())