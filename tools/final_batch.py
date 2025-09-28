#!/usr/bin/env python3
"""
Generate a final batch of simple, clean jokes to reach 500+ total.
"""

import json
from pathlib import Path


def create_final_batch():
    """Create simple, clean jokes to reach 500+ target."""
    
    # We need about 103 more jokes to reach 500
    # Focus on levels that are lower than target
    
    level_1_jokes = [
        "I used to be a banker, but I lost interest.",
        "I used to work at a calendar factory, but I got fired for taking days off.",
        "I used to be a tailor, but I wasn't suited for it.",
        "I used to work in a blanket factory, but it folded.",
        "I used to be afraid of hurdles, but I got over it.",
        "I'm afraid of speed bumps, but I'm slowly getting over it.",
        "I used to work at a shoe recycling shop. It was sole destroying.",
        "I used to work at a stationery store, but I didn't feel like I was going anywhere.",
        "I told my wife she should embrace her mistakes. She gave me a hug.",
        "I invented a new word: Plagiarism.",
        "Dear Math, grow up and solve your own problems.",
        "I'm on a whiskey diet. I've lost three days already.",
        "I named my horse Mayo. Sometimes Mayo neighs.",
        "I bought a dog from a blacksmith. As soon as I got home, he made a bolt for the door.",
        "I'm reading a book about mazes. I got lost in it."
    ]
    
    level_2_jokes = [
        "What do you call a magic dog? A labracadabrador!",
        "What do you call a sleeping dinosaur? A dino-snore!",
        "What do you call a fish wearing a crown? A king fish!",
        "What do you call a cow with two legs? Lean beef!",
        "What do you call a pig with three eyes? A piiig!",
        "What do you call a bear with no ears? B!",
        "What do you call a deer with no eyes? No idea!",
        "What do you call a deer with no eyes and no legs? Still no idea!",
        "What do you call a fish with no eyes? Fsh!",
        "What do you call a cow during an earthquake? A milkshake!",
        "What do you call a fake noodle? An impasta!",
        "What do you call a nosy pepper? Jalapeno business!",
        "What do you call a cheese that isn't yours? Nacho cheese!",
        "What do you call a cow that plays guitar? A moo-sician!",
        "What do you call a pig that does karate? A pork chop!",
        "What do you call a sheep with no legs? A cloud!",
        "What do you call a dog magician? A labracadabrador!",
        "What do you call a cat that loves water? A swimming cat!",
        "What do you call a horse that can't lose a race? Sherbet!",
        "What do you call a turtle that flies planes? A pilot turtle!",
        "What do you call a duck that gets all A's? A wise quacker!",
        "What do you call a cow that doesn't give milk? A milk dud!",
        "What do you call a fish that needs help with vocals? Auto-tuna!",
        "What do you call a dinosaur that crashes cars? Tyrannosaurus Wrecks!",
        "What do you call a sleeping bull? A bulldozer!",
        "What do you call a bear with no teeth? A gummy bear!",
        "What do you call a cow with no legs? Ground beef!",
        "What do you call a pig that tells jokes? A ham!",
        "What do you call a chicken crossing the road? Poultry in motion!",
        "What do you call a fish wearing a bowtie? Sofishticated!"
    ]
    
    level_3_jokes = [
        "Why don't elephants use computers? They're afraid of the mouse!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "Why don't oysters share? Because they're shellfish!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why don't pencils have erasers in Europe? Because they don't make mistakes!",
        "Why don't mountains ever get cold? They have snow caps!",
        "Why don't calendars ever get upset? Their days are numbered!",
        "Why don't shoes ever get tired? They're sole survivors!",
        "Why don't storms ever apologize? They're too thunder-struck!",
        "Why don't rivers ever get lost? They always know which way to flow!",
        "Why don't deserts ever get thirsty? They're used to being dry!",
        "Why don't clouds ever get tired? They're always floating around!",
        "Why don't bees ever get stressed? They're always buzzing with excitement!",
        "Why don't trees ever get lonely? They have their roots!",
        "Why don't flowers ever get angry? They're always blooming with joy!",
        "Why don't rocks ever get worried? They're solid as a rock!",
        "Why don't stars ever get lost? They always follow the North Star!",
        "Why don't oceans ever get thirsty? They're full of water!",
        "Why don't volcanoes ever get cold? They have lava!"
    ]
    
    level_4_jokes = [
        "I went to buy some camouflage pants but couldn't find any!",
        "I haven't slept for ten days, because that would be too long!",
        "I told my cat a joke about dogs. He didn't find it a-mew-sing!",
        "My wife told me to stop singing 'Wonderwall.' I said maybe!",
        "I used to hate facial hair, but then it grew on me!",
        "I'm terrified of elevators, so I'm going to start taking steps to avoid them!",
        "The early bird might get the worm, but the second mouse gets the cheese!",
        "I wondered why the baseball kept getting bigger. Then it hit me!",
        "A bicycle can't stand on its own because it's two-tired!",
        "I used to be a banker, but then I lost interest in the business!",
        "The math teacher called in sick with algebra! She had problems!",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "The graveyard is so crowded, people are dying to get in!",
        "I used to be addicted to soap, but I'm clean now!",
        "The shovel was a ground-breaking invention!",
        "I lost my job at the bank when a woman asked me to check her balance!",
        "Time flies like an arrow. Fruit flies like a banana!",
        "The best time to add insult to injury is when you're signing somebody's cast!",
        "I broke my finger last week. On the other hand, I'm okay!",
        "A plateau is the highest form of flattery!"
    ]
    
    level_5_jokes = [
        "I told my wife she was drawing her eyebrows too high. She looked surprised!",
        "My therapist says I have a preoccupation with vengeance. We'll see about that!",
        "I haven't spoken to my wife in years. I didn't want to interrupt her!",
        "My wife accused me of being immature. I was so shocked I nearly choked on my fruit loops!",
        "The other day I bought a thesaurus, but when I got home and opened it, all the pages were blank. I have no words to describe how angry I am!",
        "I tried to sue the airline for losing my luggage. I lost my case!",
        "My friend's bakery burned down. Now his business is toast!",
        "I used to be a banker, but I lost interest. Then I became a historian, but there was no future in it. Now I'm a mathematician, but I'm just going through a phase!",
        "The rotation of earth really makes my day!",
        "I was wondering why the ball kept getting bigger and bigger. Then it hit me - it was a bowling ball and I was standing in the lane!"
    ]
    
    return {
        '1': level_1_jokes,
        '2': level_2_jokes,
        '3': level_3_jokes,
        '4': level_4_jokes,
        '5': level_5_jokes
    }


def main():
    """Generate and save the final batch of jokes."""
    print("🎭 Creating final batch of jokes to reach 500+ target...")
    
    new_jokes = create_final_batch()
    
    # Save to additions file
    additions_path = Path("punnyland/data/jokes_additions.json")
    
    with open(additions_path, 'w') as f:
        json.dump(new_jokes, f, indent=2, ensure_ascii=False)
    
    total_added = sum(len(jokes) for jokes in new_jokes.values())
    print(f"💾 Saved {total_added} new jokes to {additions_path}")
    
    print("\\n📊 Final batch distribution:")
    for level, jokes in new_jokes.items():
        print(f"  Level {level}: {len(jokes)} jokes")
    
    print("✅ Final batch creation complete!")


if __name__ == "__main__":
    main()