#!/usr/bin/env python3
"""
Advanced joke generator with creative templates and better quality control.
"""

import json
import random
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path to import rate_jokes
sys.path.append(str(Path(__file__).parent))
from rate_jokes import JokeRater

try:
    from rapidfuzz import fuzz
except ImportError:
    print("Installing rapidfuzz...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'rapidfuzz'])
    from rapidfuzz import fuzz


class AdvancedJokeGenerator:
    """Advanced joke generator with creative templates."""
    
    def __init__(self):
        self.rater = JokeRater()
        
        # Load existing jokes to avoid duplicates
        with open("punnyland/data/jokes.json", 'r') as f:
            self.existing_jokes = json.load(f)
        
        # Flatten existing jokes for duplicate checking
        self.all_existing = []
        for level, joke_list in self.existing_jokes.items():
            self.all_existing.extend([joke.lower() for joke in joke_list])
        
        # Word lists for generating variations
        self.animals = ['cat', 'dog', 'cow', 'pig', 'horse', 'sheep', 'goat', 'chicken', 'duck', 'mouse', 'rat', 'elephant', 'giraffe', 'zebra', 'lion', 'tiger', 'bear', 'wolf', 'fox', 'rabbit', 'deer', 'moose', 'kangaroo', 'koala', 'monkey', 'ape', 'snake', 'lizard', 'turtle', 'frog']
        self.professions = ['teacher', 'doctor', 'lawyer', 'chef', 'musician', 'artist', 'writer', 'actor', 'singer', 'dancer', 'athlete', 'scientist', 'engineer', 'mechanic', 'electrician', 'plumber', 'carpenter', 'farmer', 'baker', 'butcher', 'barber', 'tailor', 'shoemaker', 'librarian', 'banker', 'accountant', 'manager', 'secretary', 'clerk', 'cashier']
        self.foods = ['apple', 'banana', 'orange', 'grape', 'strawberry', 'blueberry', 'raspberry', 'pineapple', 'watermelon', 'cantaloupe', 'peach', 'pear', 'cherry', 'plum', 'apricot', 'kiwi', 'mango', 'papaya', 'coconut', 'lemon', 'lime', 'grapefruit', 'pizza', 'burger', 'sandwich', 'salad', 'soup', 'pasta', 'bread', 'cake']
        self.objects = ['book', 'pen', 'pencil', 'paper', 'computer', 'phone', 'car', 'bicycle', 'train', 'plane', 'boat', 'house', 'tree', 'flower', 'rock', 'mountain', 'river', 'ocean', 'sun', 'moon', 'star', 'cloud', 'rain', 'snow', 'wind', 'fire', 'water', 'earth', 'air', 'light']
    
    def is_duplicate(self, joke: str, threshold: int = 80) -> bool:
        """Check if joke is too similar to existing jokes."""
        joke_lower = joke.lower()
        for existing in self.all_existing:
            if fuzz.token_set_ratio(joke_lower, existing) >= threshold:
                return True
        return False
    
    def create_level_2_jokes(self, needed: int) -> List[str]:
        """Create Level 2 jokes using templates."""
        templates = [
            ("What do you call a {adj} {animal}?", "A {pun}!"),
            ("Why don't {animals} {action}?", "Because they {reason}!"),
            ("What did the {animal} say to the {profession}?", "{dialogue}!"),
            ("Why did the {animal} go to the {place}?", "{reason}!"),
            ("What's a {animal}'s favorite {thing}?", "{answer}!"),
            ("How do you make a {animal} {emotion}?", "{method}!"),
            ("What do you get when you cross a {animal1} with a {animal2}?", "A {result}!")
        ]
        
        jokes = []
        attempts = 0
        max_attempts = needed * 20
        
        while len(jokes) < needed and attempts < max_attempts:
            template = random.choice(templates)
            
            if "animal" in template[0]:
                animal = random.choice(self.animals)
                animal_plural = animal + 's' if not animal.endswith('s') else animal
                
                if "{adj}" in template[0]:
                    adj = random.choice(['lazy', 'smart', 'funny', 'sleepy', 'happy', 'sad', 'angry', 'excited', 'nervous', 'brave'])
                    question = template[0].format(adj=adj, animal=animal)
                    # Create pun based on animal + adjective
                    if animal == 'cat' and adj == 'lazy':
                        answer = template[1].format(pun='cat nap expert')
                    elif animal == 'dog' and adj == 'smart':
                        answer = template[1].format(pun='Einstein-iel')
                    elif animal == 'cow' and adj == 'funny':
                        answer = template[1].format(pun='laugh-stock')
                    else:
                        # Generic pun creation
                        pun = f"{adj}-{animal[:3]}"
                        answer = template[1].format(pun=pun)
                    
                    joke = f"{question} {answer}"
                
                elif "{animals}" in template[0]:
                    action = random.choice(['play cards', 'tell jokes', 'use computers', 'drive cars', 'wear hats', 'play music', 'dance', 'sing', 'read books', 'cook food'])
                    reason = f"they don't have the right {random.choice(['paws', 'hooves', 'claws', 'fins', 'wings'])}"
                    question = template[0].format(animals=animal_plural, action=action)
                    answer = template[1].format(reason=reason)
                    joke = f"{question} {answer}"
                
                else:
                    # Default simple pattern
                    profession = random.choice(self.professions)
                    dialogue = f"You're {random.choice(['amazing', 'fantastic', 'wonderful', 'terrible', 'silly', 'funny'])}!"
                    question = template[0].format(animal=animal, profession=profession)
                    answer = template[1].format(dialogue=dialogue)
                    joke = f"{question} {answer}"
            else:
                continue
            
            # Validate and add if good
            if not self.is_duplicate(joke) and len(joke) < 150:
                rating = self.rater.rate_joke(joke)
                if rating['valid'] and rating['quality_score'] >= 75:
                    jokes.append(joke)
                    self.all_existing.append(joke.lower())
            
            attempts += 1
        
        return jokes
    
    def create_level_4_jokes(self, needed: int) -> List[str]:
        """Create Level 4 jokes with multiple puns."""
        base_jokes = [
            "Why did the {animal} become a {profession}? Because it was {pun1} and {pun2}!",
            "What do you call a {animal} that {action1} and {action2}? A {pun1} {pun2}!",
            "I told my {animal} about {topic}. It said it was {pun1} but also {pun2}!",
            "Why don't {animals} ever {negative_action}? They're too {pun1} and {pun2}!",
            "What did the {animal} say when it {past_action}? That was {pun1} and {pun2}!",
            "A {animal} walked into a {place}. The {person} said 'That's {pun1}!' The {animal} replied 'I'm also {pun2}!'",
            "What's the difference between a {thing1} and a {animal}? One is {pun1}, the other is {pun2}!"
        ]
        
        jokes = []
        attempts = 0
        max_attempts = needed * 15
        
        while len(jokes) < needed and attempts < max_attempts:
            template = random.choice(base_jokes)
            animal = random.choice(self.animals)
            
            # Create context-specific puns
            if 'cow' in template.lower() or animal == 'cow':
                pun1 = random.choice(['moo-ving', 'outstanding in its field', 'udderly amazing', 'a real cattle-ist'])
                pun2 = random.choice(['legen-dairy', 'no bull', 'pasture prime', 'grade A'])
            elif 'cat' in template.lower() or animal == 'cat':
                pun1 = random.choice(['purr-fect', 'claw-some', 'meow-nificent', 'feline fine'])
                pun2 = random.choice(['cat-astrophic', 'purr-suasive', 'whisker-ing away', 'paws-itively'])
            elif 'dog' in template.lower() or animal == 'dog':
                pun1 = random.choice(['paws-itive', 'tail-ented', 'fur-tunate', 'bow-wow brilliant'])
                pun2 = random.choice(['ruff around the edges', 'barking mad', 'doggone good', 'pawsome'])
            elif 'fish' in template.lower() or animal == 'fish':
                pun1 = random.choice(['fin-tastic', 'o-fish-ally', 'scale-ing heights', 'swimming in success'])
                pun2 = random.choice(['krilled it', 'hooked on life', 'bait and tackle', 'reel-ly good'])
            else:
                # Generic animal puns
                pun1 = f"{animal}-cellent"
                pun2 = f"{animal[:3]}-mazing"
            
            # Fill in template with appropriate words
            if '{profession}' in template:
                profession = random.choice(self.professions)
                template = template.replace('{profession}', profession)
            
            if '{action1}' in template:
                action1 = random.choice(['sings', 'dances', 'cooks', 'writes', 'paints', 'teaches'])
                template = template.replace('{action1}', action1)
            
            if '{action2}' in template:
                action2 = random.choice(['tells jokes', 'plays music', 'solves problems', 'helps others', 'makes friends'])
                template = template.replace('{action2}', action2)
            
            # Continue filling template...
            filled_template = template.format(
                animal=animal,
                animals=animal + 's',
                pun1=pun1,
                pun2=pun2,
                topic=random.choice(['jokes', 'work', 'food', 'music', 'sports']),
                negative_action=random.choice(['quit', 'give up', 'complain', 'worry']),
                past_action=random.choice(['won the race', 'solved the puzzle', 'found the treasure', 'saved the day']),
                place=random.choice(['bar', 'restaurant', 'library', 'gym', 'store']),
                person=random.choice(['bartender', 'waiter', 'librarian', 'trainer', 'clerk']),
                thing1=random.choice(self.objects),
            )
            
            joke = filled_template
            
            # Validate and add if good
            if not self.is_duplicate(joke) and len(joke) < 200:
                rating = self.rater.rate_joke(joke)
                if rating['valid'] and rating['quality_score'] >= 70:
                    jokes.append(joke)
                    self.all_existing.append(joke.lower())
            
            attempts += 1
        
        return jokes
    
    def create_level_5_jokes(self, needed: int) -> List[str]:
        """Create Level 5 ultra-corny jokes with maximum puns."""
        templates = [
            "Why did the {animal} become a {profession} at the {place} during {time}? Because it was {pun1}, {pun2}, and {pun3} all at once! Talk about {final_pun}!",
            "What do you call a {animal} that {action1}, {action2}, and {action3} while {condition}? A {pun1} {pun2} with {pun3} tendencies! That's what I call {final_pun}!",
            "I told my {animal} friend about {topic} while we were {activity}. It said 'That's {pun1}!' Then it added 'But also {pun2}!' Finally it concluded 'Overall, it's {pun3}!' I thought, '{final_pun}!'",
            "A {animal} walked into a {place} carrying a {object1} and a {object2}. The {person} said 'Why the {pun1}?' The {animal} replied 'I'm {pun2} about my {pun3}!' Everyone agreed it was {final_pun}!",
            "What's the difference between a {thing1} at a {place1} and a {animal} at a {place2}? One is {pun1} and {pun2}, the other is {pun3} and {final_pun}! Both are equally amazing in their own way!"
        ]
        
        jokes = []
        attempts = 0
        max_attempts = needed * 25
        
        while len(jokes) < needed and attempts < max_attempts:
            template = random.choice(templates)
            animal = random.choice(self.animals)
            
            # Create elaborate pun systems based on animal
            if animal == 'cow':
                puns = {
                    'pun1': 'udderly fantastic',
                    'pun2': 'moo-ving and shaking',
                    'pun3': 'really milking every opportunity',
                    'final_pun': 'legen-dairy performance with no bull involved'
                }
            elif animal == 'cat':
                puns = {
                    'pun1': 'purr-fectly positioned',
                    'pun2': 'feline fine about everything',
                    'pun3': 'whisker-ing away all doubts',
                    'final_pun': 'cat-astrophically good with paws-itively meow-nificent results'
                }
            elif animal == 'dog':
                puns = {
                    'pun1': 'paws-itively brilliant',
                    'pun2': 'tail-waggingly excited',
                    'pun3': 'barking up the right tree',
                    'final_pun': 'doggone fantastic with ruff-ly the best attitude'
                }
            elif animal == 'fish':
                puns = {
                    'pun1': 'hooked on excellence',
                    'pun2': 'swimming against the current',
                    'pun3': 'scale-ing new heights',
                    'final_pun': 'o-fish-ally the catch of the day with fin-tastic results'
                }
            elif animal == 'pig':
                puns = {
                    'pun1': 'ham-ming it up',
                    'pun2': 'bacon everyone proud',
                    'pun3': 'sow-ing the seeds of success',
                    'final_pun': 'squealing with delight and hog-ging all the attention'
                }
            else:
                # Generic elaborate puns
                puns = {
                    'pun1': f'{animal}-credible performance',
                    'pun2': f'{animal[:3]}-mazing dedication',
                    'pun3': f'{animal}-solutely wonderful attitude',
                    'final_pun': f'{animal}-traordinary results with {animal[:4]}-tastic style'
                }
            
            # Fill template with rich context
            filled = template.format(
                animal=animal,
                profession=random.choice(self.professions),
                place=random.choice(['circus', 'theater', 'concert hall', 'stadium', 'festival']),
                time=random.choice(['opening night', 'rush hour', 'prime time', 'the grand finale', 'intermission']),
                action1=random.choice(['sings opera', 'performs magic', 'tells stories', 'juggles flaming torches']),
                action2=random.choice(['dances ballet', 'plays piano', 'writes poetry', 'solves mysteries']),
                action3=random.choice(['cooks gourmet meals', 'teaches philosophy', 'paints masterpieces', 'composes symphonies']),
                condition=random.choice(['blindfolded', 'standing on one foot', 'during a thunderstorm', 'upside down']),
                topic=random.choice(['quantum physics', 'ancient history', 'modern art', 'space exploration']),
                activity=random.choice(['skydiving', 'mountain climbing', 'deep sea diving', 'tightrope walking']),
                object1=random.choice(['briefcase', 'umbrella', 'guitar', 'cookbook']),
                object2=random.choice(['telescope', 'compass', 'harmonica', 'feather']),
                person=random.choice(['ringmaster', 'conductor', 'director', 'curator']),
                thing1=random.choice(['masterpiece', 'symphony', 'novel', 'invention']),
                place1=random.choice(['gallery', 'library', 'laboratory', 'studio']),
                place2=random.choice(['stage', 'classroom', 'kitchen', 'garden']),
                **puns
            )
            
            joke = filled
            
            # Validate and add if good
            if not self.is_duplicate(joke) and 100 < len(joke) < 300:
                rating = self.rater.rate_joke(joke)
                if rating['valid'] and rating['quality_score'] >= 60:
                    jokes.append(joke)
                    self.all_existing.append(joke.lower())
            
            attempts += 1
        
        return jokes
    
    def generate_missing_jokes(self) -> Dict[str, List[str]]:
        """Generate all missing jokes to reach targets."""
        current_counts = {level: len(jokes) for level, jokes in self.existing_jokes.items()}
        
        target_counts = {
            '1': 100,  # Already have 117, need 0
            '2': 100,  # Have 46, need 54 more
            '3': 125,  # Have 121, need 4 more  
            '4': 75,   # Have 38, need 37 more
            '5': 50    # Have 3, need 47 more
        }
        
        needed = {}
        for level in ['1', '2', '3', '4', '5']:
            current = current_counts.get(level, 0)
            target = target_counts[level]
            needed[level] = max(0, target - current)
        
        print("📊 Current distribution and needs:")
        total_needed = 0
        for level in ['1', '2', '3', '4', '5']:
            current = current_counts.get(level, 0)
            need = needed[level]
            total_needed += need
            print(f"  Level {level}: {current} jokes (need {need} more)")
        
        print(f"\\nTotal needed: {total_needed} jokes")
        
        new_jokes = {}
        
        if needed['2'] > 0:
            print(f"\\n🌽 Creating {needed['2']} Level 2 jokes...")
            new_jokes['2'] = self.create_level_2_jokes(needed['2'])
            print(f"  ✅ Generated {len(new_jokes['2'])} Level 2 jokes")
        
        if needed['3'] > 0:
            print(f"\\n🌽🌽 Creating {needed['3']} Level 3 jokes...")
            # For level 3, use simple "What do you call" templates
            level_3_jokes = []
            animals = ['elephant', 'giraffe', 'rhinoceros', 'hippopotamus', 'crocodile', 'alligator']
            for animal in animals[:needed['3']]:
                joke = f"What do you call a {animal} that loves to dance? A {animal[:4]}-ing sensation!"
                if not self.is_duplicate(joke):
                    level_3_jokes.append(joke)
            new_jokes['3'] = level_3_jokes
            print(f"  ✅ Generated {len(new_jokes['3'])} Level 3 jokes")
        
        if needed['4'] > 0:
            print(f"\\n🌽🌽🌽 Creating {needed['4']} Level 4 jokes...")
            new_jokes['4'] = self.create_level_4_jokes(needed['4'])
            print(f"  ✅ Generated {len(new_jokes['4'])} Level 4 jokes")
        
        if needed['5'] > 0:
            print(f"\\n🌽🌽🌽🌽🌽 Creating {needed['5']} Level 5 jokes...")
            new_jokes['5'] = self.create_level_5_jokes(needed['5'])
            print(f"  ✅ Generated {len(new_jokes['5'])} Level 5 jokes")
        
        return new_jokes
    
    def save_new_jokes(self, new_jokes: Dict[str, List[str]]) -> str:
        """Save new jokes to additions file."""
        additions_path = Path("punnyland/data/jokes_additions.json")
        
        with open(additions_path, 'w') as f:
            json.dump(new_jokes, f, indent=2, ensure_ascii=False)
        
        total_added = sum(len(jokes) for jokes in new_jokes.values())
        print(f"\\n💾 Saved {total_added} new jokes to {additions_path}")
        
        return str(additions_path)


def main():
    """Generate missing jokes with advanced templates."""
    generator = AdvancedJokeGenerator()
    
    print("🎭 Generating missing jokes with advanced templates...")
    new_jokes = generator.generate_missing_jokes()
    
    if new_jokes:
        additions_file = generator.save_new_jokes(new_jokes)
        print(f"✅ Generation complete! Review jokes in {additions_file}")
    else:
        print("✅ No new jokes needed! Database already meets targets.")


if __name__ == "__main__":
    main()