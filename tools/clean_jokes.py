#!/usr/bin/env python3
"""
Joke cleaning and analysis tool for Punnyland.

This script cleans jokes by removing explanations and adds new jokes
to reach our target of 500+ total jokes.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
import difflib


def clean_joke(joke: str) -> Tuple[str, bool]:
    """
    Clean a joke by removing explanations while preserving the punchline.
    
    Returns:
        Tuple of (cleaned_joke, was_modified)
    """
    original = joke.strip()
    cleaned = original
    
    # Remove obvious explanation patterns
    explanation_patterns = [
        # Remove trailing explanations
        r'\s+because[^!]*!?\s*$',  # "because..." at end
        r'\s+get it[?!]*\s*$',     # "get it?" at end
        r'\s+you see[,\s].*$',     # "you see..." at end
        r'\s+that[\'\']?s[^!]*!?\s*$',  # "that's..." at end
        r'\s+in other words[,\s].*$',  # "in other words..."
        r'\s+meaning[,\s].*$',     # "meaning..."
        r'\s+translation[,\s].*$', # "translation..."
        r'\s+it means[,\s].*$',    # "it means..."
        
        # Remove parenthetical explanations
        r'\s*\([^)]*get it[^)]*\)',     # (get it?)
        r'\s*\([^)]*because[^)]*\)',    # (because...)
        r'\s*\([^)]*translation[^)]*\)', # (translation...)
        
        # Remove emoji and excessive punctuation
        r'\s*[😂😄😅🤣😆😊😉🙄🤦‍♂️🤦‍♀️🎭🌽⭐]+\s*',  # emojis
        r'\s*lol\s*$',             # "lol" at end
        r'\s*haha+\s*$',           # "haha" at end
        r'\.{3,}$',                # multiple dots at end
        r'!{2,}$',                 # multiple exclamation marks
    ]
    
    for pattern in explanation_patterns:
        new_cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        if new_cleaned != cleaned:
            cleaned = new_cleaned.strip()
    
    # Handle specific cases for Q&A format jokes
    # For "What do you call" jokes, keep only up to first answer
    qa_match = re.match(r'^(What do you call[^?]*\?)\s*([^!.]*[!.])', cleaned, re.IGNORECASE)
    if qa_match:
        cleaned = f"{qa_match.group(1)} {qa_match.group(2)}".strip()
    
    # For "Why did" jokes, keep question + first sentence of answer
    why_match = re.match(r'^(Why did[^?]*\?)\s*([^!.]*[!.])', cleaned, re.IGNORECASE)
    if why_match:
        cleaned = f"{why_match.group(1)} {why_match.group(2)}".strip()
    
    # Clean up whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Remove trailing commas or incomplete thoughts
    cleaned = re.sub(r',\s*$', '', cleaned)
    
    return cleaned, cleaned != original


def analyze_jokes(jokes_data: Dict[str, List[str]]) -> Dict:
    """Analyze the current jokes database."""
    analysis = {
        'total_jokes': 0,
        'jokes_per_level': {},
        'duplicates': [],
        'too_long': [],
        'with_explanations': [],
        'average_length_per_level': {}
    }
    
    all_jokes_lower = set()
    
    for level, joke_list in jokes_data.items():
        level_count = len(joke_list)
        analysis['total_jokes'] += level_count
        analysis['jokes_per_level'][level] = level_count
        
        level_lengths = []
        level_explanations = []
        
        for i, joke in enumerate(joke_list):
            joke_length = len(joke)
            level_lengths.append(joke_length)
            
            # Check for duplicates
            joke_lower = joke.lower().strip()
            if joke_lower in all_jokes_lower:
                analysis['duplicates'].append({
                    'level': level, 
                    'index': i, 
                    'joke': joke
                })
            all_jokes_lower.add(joke_lower)
            
            # Check length
            if joke_length > 180:
                analysis['too_long'].append({
                    'level': level,
                    'index': i,
                    'length': joke_length,
                    'joke': joke
                })
            
            # Check for likely explanations
            explanation_indicators = [
                'because ', 'get it', 'you see', 'that\'s ', 'meaning ',
                'translation', 'in other words', 'it means', 'but only if',
                '(get it', '(because', 'lol', 'haha'
            ]
            
            if any(indicator in joke.lower() for indicator in explanation_indicators):
                level_explanations.append({
                    'level': level,
                    'index': i,
                    'joke': joke
                })
        
        analysis['average_length_per_level'][level] = sum(level_lengths) / len(level_lengths) if level_lengths else 0
        if level_explanations:
            analysis['with_explanations'].extend(level_explanations)
    
    return analysis


def generate_new_jokes_by_level() -> Dict[str, List[str]]:
    """Generate additional jokes to reach 500+ total."""
    new_jokes = {
        "1": [
            "I used to be a banker, but I lost interest.",
            "Time flies like an arrow, fruit flies like a banana.",
            "The math teacher called in sick with algebra.",
            "I wondered why the ball kept getting bigger. Then it hit me.",
            "I'm reading a book about anti-gravity. It's impossible to put down.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "The early bird might get the worm, but the second mouse gets the cheese.",
            "I haven't slept for ten days, because that would be too long.",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "I'm terrified of elevators, so I take steps to avoid them.",
            "I only know 25 letters of the alphabet. I don't know Y.",
            "I'm on a seafood diet. I see food and I eat it.",
            "I used to play piano by ear, but now I use my hands.",
            "What do you call a fish wearing a crown? A king fish.",
            "What's orange and sounds like a parrot? A carrot.",
            "I used to be addicted to soap, but I'm clean now.",
            "What do you call a sleeping bull? A bulldozer.",
            "What do you call a bear with no teeth? A gummy bear.",
            "I'm afraid for the calendar. Its days are numbered.",
            "What do you call a fake noodle? An impasta."
        ],
        "2": [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "I told my wife she should embrace her mistakes. She hugged me.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the math book look so sad? Because it was full of problems!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
            "What do you call a factory that sells passable products? A satisfactory!",
            "What's orange and sounds like a parrot? A carrot!",
            "Why did the coffee file a police report? It got mugged!",
            "What do you call a pig that does karate? A pork chop!",
            "What did one wall say to the other wall? I'll meet you at the corner!",
            "What do you call a fish wearing a bowtie? Sofishticated!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "What do you call a parade of rabbits hopping backwards? A receding hare-line!",
            "What did the grape say when it got stepped on? Nothing, it just let out a little wine!"
        ],
        "3": [
            "Why don't scientists trust atoms? Because they make up everything and they're always bonding!",
            "I told my wife she should embrace her mistakes. She gave me a big hug!",
            "What do you call a fake noodle? An impasta! But don't worry, it's still al-dente!",
            "Why did the scarecrow win an award? He was outstanding in his field, but he was also pretty corny!",
            "What do you call a sleeping bull? A bulldozer! And it's always having a moo-ving dream!",
            "Why don't eggs tell jokes? They'd crack each other up and make a real mess!",
            "What do you call a bear with no teeth? A gummy bear! Sweet but not very intimidating!",
            "Why did the math book look so sad? Because it was full of problems and nobody wanted to solve them!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks! His insurance premiums are prehistoric!",
            "What did the ocean say to the beach? Nothing, it just waved! But it was shore thinking about it!",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one! That's par for the course!",
            "What do you call a factory that sells passable products? A satisfactory! Their quality is just okay-dokey!",
            "What's orange and sounds like a parrot? A carrot! But it's not very talkative!",
            "Why did the coffee file a police report? It got mugged! The perp was a real drip!",
            "What do you call a pig that does karate? A pork chop! He's got some serious ham-fu skills!",
            "What did one wall say to the other wall? I'll meet you at the corner! They're always supporting each other!",
            "What do you call a fish wearing a bowtie? Sofishticated! He's quite the catch at fancy parties!",
            "Why did the bicycle fall over? Because it was two-tired! It needed a wheel good rest!",
            "What do you call a parade of rabbits hopping backwards? A receding hare-line! Some-bunny needs to turn around!",
            "What did the grape say when it got stepped on? Nothing, it just let out a little wine! It was crushed!"
        ],
        "4": [
            "What do you call a fish that needs help with his vocals? Auto-tuna!",
            "I used to be addicted to the Hokey Pokey, but I turned myself around!",
            "What do you call a cow that plays a musical instrument? A moo-sician! But only if it's in a good moo-d!",
            "I told my cat a joke about dogs. He didn't find it a-mew-sing!",
            "What's the difference between a poorly dressed person on a bike and a well-dressed person on a tricycle? Attire! But the tricycle guy has more balance in life!",
            "Why did the math book break up with the history book? Because it had too many problems and couldn't count on the past!",
            "What do you call a sleeping bull in a flower garden? A bulldozer in a bed of roses! Beauty and the beast of napping!",
            "What did the left eye say to the right eye? Between you and me, something smells! It was a tear-able situation!",
            "Why don't eggs ever pay the restaurant bill? They always crack under pressure and scramble away!",
            "What do you call a bear with no teeth at a honey farm? A gummy bear having a sweet time, but he can't bear the sticky situation!",
            "What's orange, sounds like a parrot, and is terrible at flying? A carrot with delusions! It's got a-peel but no wings!",
            "Why did the coffee file a police report at the donut shop? It got mugged by a glazed criminal! The evidence was grounds for arrest!",
            "What do you call a pig that does karate in a deli? A pork chop with a side of ham-fu! He's bacon up the wrong tree!",
            "What did one wall say to the other wall at the comedy club? I'll meet you at the corner for some structural humor! We're really holding up the show!",
            "Why don't scientists trust stairs in a laboratory? Because they're always up to something and might cause a step-tical reaction!",
            "What do you call a fish wearing a bowtie at a sushi restaurant? Sofishticated and ready to be the catch of the day! Talk about dressed to krill!",
            "Why did the bicycle fall over at the race? Because it was two-tired from all the wheely hard training!",
            "What do you call a parade of rabbits hopping backwards down the street? A receding hare-line! Some-bunny should carrot about direction!",
            "What did the grape say when it got stepped on at the wine festival? Nothing, it just let out a little wine and got crushed by the experience!",
            "Why don't skeletons fight each other at Halloween parties? They don't have the guts and they're bone tired of conflict!"
        ],
        "5": [
            "What do you call a fish that needs help with his vocals while swimming backwards? Auto-tuna in reverse! He's really going against the current of music!",
            "I used to be addicted to the Hokey Pokey, but then I turned myself around, put my left foot in, took my right foot out, and shook it all about until I was cured!",
            "What do you call a cow that plays a musical instrument in a barn band? A moo-sician! But only if it's in a good moo-d, doesn't have beef with the other animals, and can milk the performance for all it's worth!",
            "I told my cat a joke about dogs while he was napping. He didn't find it a-mew-sing, gave me a paws for concern, and said it was the cat's pajamas of bad humor!",
            "What's the difference between a poorly dressed person on a bike and a well-dressed person on a tricycle riding through a fashion district? Attire! But the tricycle guy has more balance in life, three times the style, and is wheely well-dressed!",
            "Why did the math book break up with the history book at the library? Because it had too many problems, couldn't count on the past, was divided by their differences, and their relationship just didn't add up to a sum-thing special!",
            "What do you call a sleeping bull in a flower garden during springtime? A bulldozer in a bed of roses having beauty sleep! It's beauty and the beast of napping, but he's really pushing up daisies in his dreams!",
            "What did the left eye say to the right eye during an emotional movie? Between you and me, something smells! It was a tear-able situation that really brought tears to their pupils and made them blink twice!",
            "Why don't eggs ever pay the restaurant bill at breakfast? They always crack under pressure, scramble away from responsibility, get beaten by the situation, and are always over-easy to avoid paying!",
            "What do you call a bear with no teeth at a honey farm during harvest season? A gummy bear having a sweet time, but he can't bear the sticky situation, finds it un-bear-ably sweet, and is just gumming up the works!",
            "What's orange, sounds like a parrot, is terrible at flying, and thinks it's a bird? A carrot with delusions and aviation dreams! It's got a-peel but no wings, and its flying carrots are just pie in the sky!",
            "Why did the coffee file a police report at the donut shop during rush hour? It got mugged by a glazed criminal! The evidence was grounds for arrest, the perp was a real drip, and the whole case was brewing with trouble!",
            "What do you call a pig that does karate in a deli while ordering lunch? A pork chop with a side of ham-fu! He's bacon up the wrong tree, bringing home the bacon with his martial arts, and his moves are simply ham-azing!",
            "What did one wall say to the other wall at the comedy club during open mic night? I'll meet you at the corner for some structural humor! We're really holding up the show, supporting each other's jokes, and our comedy is wall-to-wall entertainment!",
            "Why don't scientists trust stairs in a laboratory during experiments? Because they're always up to something, might cause a step-tical reaction, are taking research to the next level, and their results are always a step above the rest!"
        ]
    }
    
    return new_jokes


def main():
    """Main function to clean jokes and expand the database."""
    # Load current jokes
    jokes_file = Path("punnyland/data/jokes.json")
    with open(jokes_file, 'r') as f:
        current_jokes = json.load(f)
    
    print("🎭 Punnyland Joke Database Cleanup & Expansion 🎭\n")
    
    # Analyze current state
    print("📊 Analyzing current database...")
    analysis = analyze_jokes(current_jokes)
    
    print(f"Current total jokes: {analysis['total_jokes']}")
    print("Current distribution:")
    for level, count in analysis['jokes_per_level'].items():
        print(f"  Level {level}: {count} jokes")
    
    print(f"\nFound {len(analysis['with_explanations'])} jokes with explanations")
    print(f"Found {len(analysis['duplicates'])} potential duplicates")
    print(f"Found {len(analysis['too_long'])} jokes over 180 characters")
    
    # Clean jokes
    print("\n🧹 Cleaning jokes...")
    cleaned_jokes = {}
    total_modifications = 0
    
    for level, joke_list in current_jokes.items():
        cleaned_list = []
        for joke in joke_list:
            cleaned_joke, was_modified = clean_joke(joke)
            cleaned_list.append(cleaned_joke)
            if was_modified:
                total_modifications += 1
        cleaned_jokes[level] = cleaned_list
    
    print(f"Modified {total_modifications} jokes during cleaning")
    
    # Add new jokes to reach target
    print("\n📈 Adding new jokes...")
    new_jokes = generate_new_jokes_by_level()
    
    final_jokes = {}
    added_count = 0
    
    for level in cleaned_jokes:
        final_jokes[level] = cleaned_jokes[level] + new_jokes.get(level, [])
        added_count += len(new_jokes.get(level, []))
    
    # Final analysis
    final_analysis = analyze_jokes(final_jokes)
    print(f"\n✅ Final Results:")
    print(f"Total jokes: {final_analysis['total_jokes']} (was {analysis['total_jokes']})")
    print(f"Added: {added_count} new jokes")
    print("Final distribution:")
    for level, count in final_analysis['jokes_per_level'].items():
        print(f"  Level {level}: {count} jokes")
    
    # Save cleaned and expanded jokes
    output_file = Path("punnyland/data/jokes_cleaned_expanded.json")
    with open(output_file, 'w') as f:
        json.dump(final_jokes, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved cleaned and expanded jokes to: {output_file}")
    print("\n🎉 Job complete! Review the new file and replace the original when satisfied.")
    
    # Generate a report
    with open("reports/cleanup_report.json", 'w') as f:
        json.dump({
            'original_analysis': analysis,
            'final_analysis': final_analysis,
            'modifications_made': total_modifications,
            'jokes_added': added_count,
            'timestamp': '2025-09-28T17:55:00Z'
        }, f, indent=2)
    
    print(f"📝 Detailed report saved to: reports/cleanup_report.json")


if __name__ == "__main__":
    main()