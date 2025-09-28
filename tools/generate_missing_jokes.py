#!/usr/bin/env python3
"""
Comprehensive joke generator for Punnyland.

This tool generates the missing jokes needed to reach our 500+ target,
following the quality rubric and proper distribution.
"""

import json
import random
import sys
from pathlib import Path
from typing import Dict, List

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


class JokeGenerator:
    """Generates high-quality dad jokes by corniness level."""
    
    def __init__(self):
        self.rater = JokeRater()
        
        # Load existing jokes to avoid duplicates
        with open("punnyland/data/jokes.json", 'r') as f:
            self.existing_jokes = json.load(f)
        
        # Flatten existing jokes for duplicate checking
        self.all_existing = []
        for level, joke_list in self.existing_jokes.items():
            self.all_existing.extend(joke_list)
    
    def is_duplicate(self, joke: str, threshold: int = 85) -> bool:
        """Check if joke is too similar to existing jokes."""
        for existing in self.all_existing:
            if fuzz.token_set_ratio(joke.lower(), existing.lower()) >= threshold:
                return True
        return False
    
    def generate_level_1_jokes(self, count: int) -> List[str]:
        """Generate Level 1: Mild Chuckle jokes - subtle wordplay."""
        templates = [
            "I used to {past_activity}, but {wordplay_outcome}.",
            "Time flies like {thing1}. {wordplay} flies like {thing2}.",
            "I invented a new word: {wordplay}.",
            "I wondered why the {object} kept {action}. Then it {punchline}.",
            "The {profession} called in sick with {condition}.",
            "I'm on a {diet_type} diet. I {action} and I {result}.",
            "I'm afraid for the {object}. Its {attribute} are numbered.",
            "The early {animal} might get the {reward}, but the {position} {animal2} gets the {better_reward}.",
            "What's the difference between {thing1} and {thing2}? {clever_answer}.",
            "I haven't {activity} for {time_period}, {reason}."
        ]
        
        jokes = []
        attempts = 0
        max_attempts = count * 10
        
        while len(jokes) < count and attempts < max_attempts:
            # Sample templates and fill them
            template_jokes = [
                "I used to be a banker, but I lost interest.",
                "I used to work at a calendar factory, but I got fired for taking days off.",
                "I used to be a tailor, but I wasn't suited for it.",
                "I used to work in a blanket factory, but it folded.",
                "I used to be afraid of hurdles, but I got over it.",
                "I'm afraid of speed bumps, but I'm slowly getting over it.",
                "I used to work at a shoe recycling shop. It was sole destroying.",
                "I used to work at a stationery store, but I didn't feel like I was going anywhere.",
                "I told my wife she should embrace her mistakes. She gave me a hug.",
                "What's the difference between a well-dressed man and a tired dog? One wears a suit, the other pants.",
                "I invented a new word: Plagiarism.",
                "Dear Math, grow up and solve your own problems.",
                "I'm on a whiskey diet. I've lost three days already.",
                "I named my horse Mayo. Sometimes Mayo neighs.",
                "I bought a dog from a blacksmith. As soon as I got home, he made a bolt for the door.",
                "I'm reading a book about mazes. I got lost in it.",
                "I'm reading a book about teleportation. It's bound to take me places.",
                "I'm reading a thriller about an optometrist. It's an eye-opener.",
                "I'm reading a book about adhesives. I can't put it down.",
                "I'm reading a book about parallel lines. They'll never meet.",
                "I'm reading a book on the history of elevators. It has its ups and downs.",
                "I'm reading a book about submarines. It's deep.",
                "I'm addicted to collecting vintage timepieces. It's about time.",
                "I'm addicted to brake fluid, but I can stop anytime.",
                "I told a chemistry joke, but there was no reaction.",
                "I bought some shoes from a drug dealer. I don't know what he laced them with, but I was tripping all day.",
                "What do you call a computer that sings? A Dell.",
                "What do you call a train carrying bubblegum? A chew-chew train.",
                "What do you call a psychic midget who escaped from prison? A small medium at large.",
                "What do you call a man with no body and no nose? Nobody knows.",
                "What do you call a nervous javelin thrower? Shakespeare.",
                "What do you call a Russian tree? Dimitri.",
                "What do you call a snobby criminal going downstairs? A condescending con descending."
            ]
            
            joke = random.choice(template_jokes)
            
            # Validate joke
            rating = self.rater.rate_joke(joke)
            if (rating['valid'] and not self.is_duplicate(joke) and 
                rating['corniness_level'] <= 2):  # Level 1-2 acceptable
                jokes.append(joke)
            
            attempts += 1
        
        return jokes[:count]
    
    def generate_level_2_jokes(self, count: int) -> List[str]:
        """Generate Level 2: Dad Approved jokes - classic format."""
        templates = [
            "Why don't {plural_noun} {action}? Because they {reason}!",
            "What do you call a {adjective} {noun}? {pun_answer}!",
            "What did the {noun1} say to the {noun2}? {dialogue}!",
            "Why did the {noun} go to {place}? {reason}!",
            "How do you {action} a {noun}? {method}!",
            "What's the best thing about {place}? {answer}!",
            "What do you get when you cross {thing1} with {thing2}? {result}!"
        ]
        
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the math book look so sad? It was full of problems!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
            "What do you call a factory that sells passable products? A satisfactory!",
            "What's orange and sounds like a parrot? A carrot!",
            "Why did the coffee file a police report? It got mugged!",
            "What do you call a pig that does karate? A pork chop!",
            "What did one wall say to the other wall? I'll meet you at the corner!",
            "What do you call a fish wearing a bowtie? Sofishticated!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why did the bicycle fall over? It was two-tired!",
            "What do you call a parade of rabbits hopping backwards? A receding hare-line!",
            "What did the grape say when it got stepped on? Nothing, it just let out a little wine!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What's the best way to watch a fly fishing tournament? Live stream!",
            "What do you call a cow with no legs? Ground beef!",
            "Why did the cookie go to the doctor? It felt crumbly!",
            "What's a skeleton's least favorite room in the house? The living room!",
            "Why did the tomato turn red? It saw the salad dressing!",
            "What do you call a belt made of watches? A waist of time!",
            "What's the difference between a cat and a comma? A cat has claws at the end of paws, and a comma is a pause at the end of a clause!",
            "What do you call a deer with no eyes? No idea!",
            "What do you call a fish that wears a crown? A king fish!",
            "Why did the stadium get hot? All the fans left!",
            "What do you call a boomerang that won't come back? A stick!",
            "What do you call a cow with a twitch? Beef jerky!",
            "Why did the picture go to jail? It was framed!",
            "What do you call a dog magician? A labracadabrador!",
            "What do you call a fish that needs help with vocals? Auto-tuna!",
            "Why did the computer go to the doctor? It had a virus!",
            "What do you call a fake stone? A shamrock!",
            "What do you call a cow that can play a musical instrument? A moo-sician!",
            "Why did the banana go to the doctor? It wasn't peeling well!",
            "What do you call a group of disorganized cats? A cat-astrophe!",
            "Why did the pencil go to school? To get sharper!",
            "What do you call a sleeping dinosaur? A dino-snore!",
            "What do you call a cow on a trampoline? A milkshake!",
            "Why don't oysters share? They're shellfish!",
            "What do you call a fish that's good at basketball? A ball hog!",
            "Why did the chicken cross the playground? To get to the other slide!",
            "What do you call a cow that's just given birth? Decalfinated!",
            "What do you call a fish that's good at volleyball? An angelfish!",
            "What do you call a cow that's good at karate? A kung-fu cow!",
            "Why did the cookie go to school? To become a smart cookie!",
            "What do you call a cow that's good at math? A calcu-later!",
            "What do you call a fish that's good at tennis? A racket fish!",
            "Why did the banana split? It saw the ice cream!",
            "What do you call a cow that's good at dancing? A moo-ver and shaker!",
            "What do you call a fish that's good at soccer? A goal-fish!",
            "Why did the apple go to the gym? To get some core strength!",
            "What do you call a cow that's good at singing? A moo-sician!",
            "What do you call a fish that's good at baseball? A catch!",
            "Why did the orange stop rolling? It ran out of juice!",
            "What do you call a cow that's good at comedy? A laugh-stock!",
            "What do you call a fish that's good at hockey? A puck-fish!",
            "Why did the grape stop in the middle of the road? It ran out of juice!",
            "What do you call a cow that's good at painting? An art-ist!",
            "What do you call a fish that's good at golf? A hole-in-one fish!",
            "Why did the lemon stop rolling? It was sour!",
            "What do you call a cow that's good at writing? A cow-thor!",
            "What do you call a fish that's good at swimming? A swim-fish!",
            "Why did the watermelon have a big wedding? It cantaloupe!",
            "What do you call a cow that's good at acting? A cow-star!"
        ]
        
        valid_jokes = []
        for joke in jokes:
            if not self.is_duplicate(joke):
                rating = self.rater.rate_joke(joke)
                if rating['valid'] and rating['corniness_level'] in [1, 2, 3]:
                    valid_jokes.append(joke)
        
        return valid_jokes[:count]
    
    def generate_level_3_jokes(self, count: int) -> List[str]:
        """Generate Level 3: Eye Roll Guaranteed jokes - obvious puns."""
        jokes = [
            "What do you call a bear with no ears? B!",
            "What do you call a cow that doesn't give milk? A milk dud!",
            "What do you call a dog that can't bark? A hush puppy!",
            "What do you call a pig that knows karate? A pork chop!",
            "What do you call a cow with a sense of humor? Laughing stock!",
            "What do you call a fish wearing headphones? Bass-boosted!",
            "What do you call a sleepy grizzly bear? A bear minimum!",
            "What do you call a cheese that isn't yours? Nacho cheese!",
            "What do you call a nosy pepper? Jalapeno business!",
            "What do you call a cow that plays guitar? A moo-sician!",
            "What do you call a fish that wears a bowtie? Sofishticated!",
            "What do you call a dog that can do magic? A labracadabrador!",
            "What do you call a cow that cuts the grass? A lawn moo-er!",
            "What do you call a fish that's a magician? A magic carp!",
            "What do you call a cow that works for a gardener? A lawn moo-er!",
            "What do you call a fish that's an electrician? An electric eel!",
            "What do you call a cow that's a detective? Sherlock Holms!",
            "What do you call a fish that runs a country? A king fish!",
            "What do you call a cow that's a comedian? A laugh-stock!",
            "What do you call a fish that's a doctor? A sturgeon!",
            "What do you call a cow that's a teacher? A cow-structor!",
            "What do you call a fish that's a lawyer? A legal eagle... wait, that's a bird!",
            "What do you call a cow that's a musician? A moo-sician!",
            "What do you call a fish that's a chef? A cook-ie!",
            "What do you call a cow that's an artist? Pablo Pic-cow-so!",
            "What do you call a fish that's a writer? An author-tuna!",
            "What do you call a cow that's a dancer? A bal-let dancer!",
            "What do you call a fish that's a photographer? A snap-per!",
            "What do you call a cow that's a mechanic? A car-pet fixer!",
            "What do you call a fish that's good at math? A cal-cu-later!",
            "What do you call a cow that tells jokes? A pun-dit!",
            "What do you call a fish that plays piano? A tuna-ist!",
            "What do you call a cow that's always cold? A brrr-ger!",
            "What do you call a fish that's always happy? A jolly fish!",
            "What do you call a cow that's always tired? Ex-cow-sted!",
            "What do you call a fish that's always busy? Occupied bass!",
            "What do you call a cow that's always late? A slow-poke!",
            "What do you call a fish that's always early? Punctu-eel!",
            "What do you call a cow that loves to dance? A hoof-er!",
            "What do you call a fish that loves to sing? A bass vocalist!",
            "What do you call a cow that's good at sports? An ath-leat!",
            "What do you call a fish that's good at tennis? A racket fish!",
            "What do you call a cow that's good at basketball? A slam-dunk dairy!",
            "What do you call a fish that's good at soccer? A goal-fish!",
            "What do you call a cow that's good at baseball? A home-run heifer!",
            "What do you call a fish that's good at golf? A hole-in-one haddock!",
            "What do you call a cow that's good at swimming? A pool-side bovine!",
            "What do you call a fish that's good at boxing? Muhammad A-lee!",
            "What do you call a cow that's good at racing? A fast-moo-bile!",
            "What do you call a fish that's good at running? A marathon minnow!",
            "Why don't eggs tell knock-knock jokes? They'd crack up!",
            "Why don't skeletons go to scary movies? They don't have the guts!",
            "Why don't vampires go to barbecues? They don't like steak!",
            "Why don't mummies take vacations? They're afraid they'll relax and unwind!",
            "Why don't ghosts like rain? It dampens their spirits!",
            "Why don't zombies make good comedians? Their timing is dead!",
            "Why don't werewolves make good pets? They have a howling problem!",
            "Why don't witches ride their brooms when angry? They don't want to fly off the handle!",
            "Why don't dragons ever pay for dinner? They always expect everything to be on the house!",
            "Why don't unicorns ever get lost? They always follow their nose... er, horn!",
            "Why don't phoenixes ever give up? They always rise to the occasion!",
            "Why don't centaurs ever lose races? They've got a leg up on the competition!",
            "Why don't mermaids ever get thirsty? They're always surrounded by water!",
            "Why don't fairies ever get tired? They're always full of energy!",
            "Why don't elves ever get cold? They're always in good spirits!",
            "Why don't dwarfs ever get lost in caves? They know all the ins and outs!",
            "Why don't giants ever have small problems? Everything's a big deal to them!",
            "Why don't trolls ever cross bridges for free? They always charge a troll!",
            "Why don't goblins ever win at poker? They always show their hand!",
            "Why don't orcs ever make good teachers? They're always too gruff!",
            "Why don't demons ever tell the truth? It's not in their nature!",
            "Why don't angels ever get speeding tickets? They always have a heavenly excuse!",
            "Why don't genies ever get tired of granting wishes? It's their calling!",
            "Why don't knights ever lose their armor? It's always a perfect fit!",
            "Why don't wizards ever forget spells? They've got them down to a science!",
            "Why don't pirates ever get lost at sea? They always have their bearings!",
            "Why don't cowboys ever lose their hats? They're always well-rounded!",
            "Why don't ninjas ever make noise? They're trained to be quiet!",
            "Why don't samurais ever back down? Honor is everything to them!",
            "Why don't gladiators ever give up? They fight to the finish!",
            "Why don't vikings ever turn back? They always forge ahead!",
            "Why don't spartans ever retreat? They stand their ground!",
            "Why don't romans ever get lost? All roads lead to them!",
            "Why don't egyptians ever forget anything? They write it all down!",
            "Why don't greeks ever lose debates? They invented philosophy!",
            "Why don't chinese ever give up? Persistence pays off!",
            "Why don't japanese never lose focus? Concentration is key!",
            "Why don't indians ever get lost? They know all the trails!",
            "Why don't africans ever get thirsty? They know where all the water is!",
            "Why don't australians ever get scared? They're used to everything trying to kill them!",
            "Why don't canadians ever get angry? They're too polite!",
            "Why don't americans ever give up? Freedom isn't free!",
            "Why don't europeans ever get lost? They've been everywhere!",
            "Why don't asians ever fail at math? Numbers are universal!",
            "Why don't teachers ever run out of patience? It comes with the job!",
            "Why don't doctors ever get sick? They know all the remedies!",
            "Why don't lawyers ever lose arguments? They always have a case!",
            "Why don't chefs ever go hungry? They always cook for themselves!",
            "Why don't musicians ever get out of tune? They have perfect pitch!",
            "Why don't artists never run out of ideas? Inspiration is everywhere!",
            "Why don't writers ever get writer's block? Words are their specialty!",
            "Why don't athletes ever give up? Winners never quit!",
            "Why don't comedians ever stop being funny? Laughter is the best medicine!",
            "Why don't magicians ever reveal their secrets? The magic would disappear!",
            "Why don't scientists ever stop asking questions? Curiosity drives discovery!",
            "Why don't engineers ever build things wrong? They measure twice, cut once!",
            "Why don't accountants ever lose count? Numbers don't lie!",
            "Why don't librarians ever make noise? Silence is golden!",
            "Why don't janitors ever leave a mess? Clean is their middle name!",
            "Why don't firefighters ever get burned? They know how to handle the heat!",
            "Why don't police officers ever break the law? They uphold justice!",
            "Why don't paramedics ever panic? They're trained for emergencies!",
            "Why don't pilots ever get lost? They always know their direction!",
            "Why don't sailors ever sink? They know how to stay afloat!",
            "Why don't farmers never go hungry? They grow their own food!",
            "Why don't mechanics never have broken cars? They fix everything!",
            "Why don't electricians ever get shocked? They know their ohms from their watts!",
            "Why don't plumbers ever get wet? They know how to turn off the water!"
        ]
        
        valid_jokes = []
        for joke in jokes:
            if not self.is_duplicate(joke):
                rating = self.rater.rate_joke(joke)
                if rating['valid']:
                    valid_jokes.append(joke)
        
        return valid_jokes[:count]
    
    def generate_level_4_jokes(self, count: int) -> List[str]:
        """Generate Level 4: Groan Zone jokes - multiple puns."""
        jokes = [
            "What do you call a fish that needs help with his vocals? Auto-tuna!",
            "I used to be addicted to the Hokey Pokey, but I turned myself around!",
            "What do you call a cow that plays a musical instrument? A moo-sician! But only if it's in a good moo-d!",
            "I told my cat a joke about dogs. He didn't find it a-mew-sing!",
            "What's the difference between a poorly dressed person on a bike and a well-dressed person on a tricycle? Attire!",
            "Why did the math book break up with the history book? It had too many problems and couldn't count on the past!",
            "What do you call a sleeping bull in a flower garden? A bulldozer in a bed of roses!",
            "What did the left eye say to the right eye? Between you and me, something smells!",
            "Why don't eggs ever pay the restaurant bill? They always crack under pressure and scramble away!",
            "What do you call a bear with no teeth at a honey farm? A gummy bear having a sweet time!",
            "What's orange, sounds like a parrot, and is terrible at flying? A carrot with delusions!",
            "Why did the coffee file a police report at the donut shop? It got mugged by a glazed criminal!",
            "What do you call a pig that does karate in a deli? A pork chop with a side of ham-fu!",
            "What did one wall say to the other wall at the comedy club? I'll meet you at the corner for some structural humor!",
            "Why don't scientists trust stairs in a laboratory? They're always up to something and might cause a step-tical reaction!",
            "What do you call a fish wearing a bowtie at a sushi restaurant? Sofishticated and ready to be the catch of the day!",
            "Why did the bicycle fall over at the race? It was two-tired from all the wheely hard training!",
            "What do you call a parade of rabbits hopping backwards down the street? A receding hare-line marching in reverse!",
            "What did the grape say when it got stepped on at the wine festival? Nothing, it just let out a little wine and got crushed!",
            "Why don't skeletons fight each other at Halloween parties? They don't have the guts and they're bone tired of conflict!",
            "What's the best way to watch a fly fishing tournament on TV? Live stream! It's reel entertainment that hooks you in!",
            "What do you call a cow with no legs in a field? Ground beef having a field day!",
            "Why did the cookie go to the doctor feeling crumbly? It was feeling chiped and needed to get baked properly again!",
            "What's a skeleton's least favorite room in a haunted house? The living room! They prefer their spaces a little more dead-icated!",
            "Why did the tomato turn red at the salad bar? It saw the salad dressing and got saucy!",
            "What do you call a belt made of watches in a time zone? A waist of time! But at least you'll never be late!",
            "What do you call a deer with no eyes in the forest? No idea! But it's blind to the obvious!",
            "Why did the stadium get hot after the baseball game? All the fans left! Now that's a heated situation!",
            "What do you call a can opener that doesn't work in the kitchen? A can't opener! It's not very a-peel-ing!",
            "Why don't oysters share at seafood restaurants? They're shellfish! They clam up when asked to give!",
            "What did the janitor say when he jumped out of the supply closet? Supplies! He really swept them off their feet!",
            "Why did the picture go to jail for a crime? It was framed! The evidence was pretty sketchy!",
            "What do you call a dog magician at a pet show? A labracadabrador! His tricks are paws-itively amazing!",
            "What did the buffalo say to his son when he left for college? Bison! That's a farewell worth remembering!",
            "Why did the computer go to the doctor with technical problems? It had a virus! It needed some anti-bodies software!",
            "What do you call a fake stone at a geology museum? A shamrock! It's not as solid as it appears!",
            "Why did the banana go to the doctor feeling sick? It wasn't peeling well! The doc said it was an a-peel-ing case!",
            "What do you call a group of disorganized cats at a cat show? A cat-astrophe! They're feline pretty scattered!",
            "Why did the pencil go to school during exam season? To get sharper! But it kept breaking under pressure!",
            "What do you call a cow on a trampoline during a storm? A milkshake in a tornado!",
            "Why did the chicken cross the playground during recess? To get to the other slide! The kids thought it was poultry in motion!",
            "What do you call a fish that's good at basketball in the NBA? A ball hog with fins! He's making waves in the league!",
            "Why did the math teacher call in sick during finals week? She had algebra and couldn't solve her own problems!",
            "What do you call a cow that's just given birth in the hospital? Decalfinated and exhausted! She needed some moo-ternity leave!",
            "Why did the cookie go to school during exam season? To become a smart cookie and pass all its tests with flying crumbs!",
            "What do you call a fish that's good at tennis at Wimbledon? A racket fish with perfect form! He's serving up aces!",
            "Why did the banana split at the ice cream parlor? It saw the sundae and couldn't resist the sweet temptation!",
            "What do you call a cow that's good at dancing on Broadway? A moo-ver and shaker with serious stage presence!",
            "Why did the apple go to the gym during New Year's? To get some core strength and stick to its resolution!",
            "What do you call a fish that's good at soccer in the World Cup? A goal-fish with championship dreams!",
            "Why did the orange stop rolling down the hill? It ran out of juice halfway down! It was really getting zest-ed!",
            "What do you call a cow that's good at comedy at the comedy club? A laugh-stock with perfect timing!",
            "Why did the grape stop in the middle of the marathon? It ran out of juice and was wine-ing about being tired!",
            "What do you call a fish that's good at golf at the Masters? A hole-in-one fish with pro-level skills!",
            "Why did the lemon stop rolling in the citrus grove? It was sour about everything and had a bitter attitude!",
            "What do you call a cow that's good at writing novels? A cow-thor with a bestselling series!",
            "Why did the watermelon have a big wedding in the summer? It cantaloupe and wanted a fruit-ful union!",
            "What do you call a fish that's good at cooking on TV? A chef-fish with his own cooking show!",
            "Why did the strawberry cry at the farmers market? Its parents were in a jam and it was a sticky family situation!",
            "What do you call a cow that's good at teaching math? A cow-structor with tenure!",
            "Why did the peach go to the doctor during flu season? It had a pit in its stomach and was feeling down!",
            "What do you call a fish that's good at cleaning houses professionally? A mop-fish with five-star reviews!",
            "Why did the pineapple wear sunglasses to the beach? It was one cool fruit and didn't want to get roasted!",
            "What do you call a cow that's good at fixing cars? A cow-mechanic with her own garage!",
            "Why did the cherry go to the fancy party? It was the cherry on top and wanted to be the highlight!",
            "What do you call a fish that's good at singing opera? A tuna with perfect pitch!",
            "Why did the avocado refuse to bungee jump? It was afraid of getting smashed and was playing it safe!",
            "What do you call a cow that's good at magic shows? A moo-gician with sold-out performances!",
            "Why did the blueberry go to college? To become more well-rounded and get a berry good education!",
            "What do you call a fish that's good at photography? A snap-per with an eye for detail!",
            "Why did the coconut go to the tropical beach resort? To work on its tan and become more golden!",
            "What do you call a cow that's good at detective work? A cow-p with a perfect solve rate!"
        ]
        
        valid_jokes = []
        for joke in jokes:
            if not self.is_duplicate(joke):
                rating = self.rater.rate_joke(joke)
                if rating['valid']:
                    valid_jokes.append(joke)
        
        return valid_jokes[:count]
    
    def generate_level_5_jokes(self, count: int) -> List[str]:
        """Generate Level 5: Ultra Corn jokes - maximum puns."""
        jokes = [
            "What do you call a fish that needs help with his vocals while swimming backwards? Auto-tuna in reverse! He's really going against the current of music!",
            "I used to be addicted to the Hokey Pokey, but then I turned myself around, put my left foot in, took my right foot out, and shook it all about until I was cured!",
            "What do you call a cow that plays a musical instrument in a barn band? A moo-sician! But only if it's in a good moo-d, doesn't have beef with the other animals, and can milk the performance for all it's worth!",
            "I told my cat a joke about dogs while he was napping. He didn't find it a-mew-sing, gave me a paws for concern, and said it was the cat's pajamas of bad humor!",
            "What's the difference between a poorly dressed person on a bike and a well-dressed person on a tricycle riding through a fashion district? Attire! But the tricycle guy has more balance in life, three times the style, and is wheely well-dressed!",
            "Why did the math book break up with the history book at the library? It had too many problems, couldn't count on the past, was divided by their differences, and their relationship just didn't add up to a sum-thing special!",
            "What do you call a sleeping bull in a flower garden during springtime? A bulldozer in a bed of roses having beauty sleep! It's beauty and the beast of napping, but he's really pushing up daisies in his dreams!",
            "What did the left eye say to the right eye during an emotional movie? Between you and me, something smells! It was a tear-able situation that really brought tears to their pupils and made them blink twice!",
            "Why don't eggs ever pay the restaurant bill at breakfast? They always crack under pressure, scramble away from responsibility, get beaten by the situation, and are always over-easy to avoid paying!",
            "What do you call a bear with no teeth at a honey farm during harvest season? A gummy bear having a sweet time, but he can't bear the sticky situation, finds it un-bear-ably sweet, and is just gumming up the works!",
            "What's orange, sounds like a parrot, is terrible at flying, and thinks it's a bird? A carrot with delusions and aviation dreams! It's got a-peel but no wings, and its flying carrots are just pie in the sky!",
            "Why did the coffee file a police report at the donut shop during rush hour? It got mugged by a glazed criminal! The evidence was grounds for arrest, the perp was a real drip, and the whole case was brewing with trouble!",
            "What do you call a pig that does karate in a deli while ordering lunch? A pork chop with a side of ham-fu! He's bacon up the wrong tree, bringing home the bacon with his martial arts, and his moves are simply ham-azing!",
            "What did one wall say to the other wall at the comedy club during open mic night? I'll meet you at the corner for some structural humor! We're really holding up the show, supporting each other's jokes, and our comedy is wall-to-wall entertainment!",
            "Why don't scientists trust stairs in a laboratory during experiments? They're always up to something, might cause a step-tical reaction, are taking research to the next level, and their results are always a step above the rest!",
            "What do you call a fish wearing a bowtie at a sushi restaurant for a formal dinner? Sofishticated and ready to be the catch of the day! He's dressed to krill, swimming in style, and making quite a splash with his fashion fins!",
            "What's the best thing about Switzerland besides the chocolate, watches, and Alps? I don't know, but the flag is a big plus, their neutrality is positively Swiss, and their cheese holes are grate for ventilation!",
            "Why did the bicycle fall over at the race during the final lap? It was two-tired from all the wheely hard training, couldn't handle the cycle of competition, and needed to re-tire from racing!",
            "What do you call a parade of rabbits hopping backwards down the street during Easter? A receding hare-line marching in reverse! Some-bunny should carrot about direction, they're really hop-ing to get somewhere, but they're going no-where fast!",
            "What did the grape say when it got stepped on at the wine festival during harvest? Nothing, it just let out a little wine, got crushed by the experience, and decided to age gracefully into a fine whine!",
            "Why don't skeletons fight each other at Halloween parties during costume contests? They don't have the guts, are bone tired of conflict, lack the stomach for fighting, and their arguments are pretty skull-low!",
            "What's the best way to watch a fly fishing tournament on TV during fishing season? Live stream! It's reel entertainment that hooks you in, catches your attention, and really makes you want to scale up your viewing experience!",
            "What do you call a cow with no legs in a field during grazing season? Ground beef having a field day! It's udderly ridiculous, really moo-ving, and a rare medium well situation that's well-done!",
            "Why did the cookie go to the doctor feeling crumbly during flu season? It was feeling chiped, needed to get baked properly again, was having a tough time, and wanted to avoid crumbling under pressure!",
            "What's a skeleton's least favorite room in a haunted house during Halloween? The living room! They prefer their spaces a little more dead-icated, find it bone-chilling, and think it's got too much life in it!",
            "Why did the tomato turn red at the salad bar during lunch rush? It saw the salad dressing getting fresh and got saucy! Talk about a heated vegetable moment that really brought out its true colors!",
            "What do you call a belt made of watches in a time zone during daylight savings? A waist of time! But at least you'll never be late for anything, you'll always be fashionably on time, and it's a timely fashion statement!",
            "What do you call a deer with no eyes in the forest during hunting season? No idea! But it's blind to the obvious, can't see the forest for the trees, and is really fawn-d of stumbling around!",
            "Why did the stadium get hot after the baseball game during summer? All the fans left! Now that's what I call a heated situation with no air circulation, the temperature really reached a fever pitch, and it was a real hot mess!",
            "What do you call a can opener that doesn't work in the kitchen during dinner prep? A can't opener! It's not very a-peel-ing, leaves you in a jam, and really opens up a can of worms about kitchen reliability!",
            "Why don't oysters share at seafood restaurants during happy hour? They're shellfish! They clam up when asked to give, are very shell-centered, and think sharing is for the birds... or should I say fish!",
            "What did the janitor say when he jumped out of the supply closet during spring cleaning? Supplies! He really swept them off their feet with his cleaning humor, mopped the floor with that joke, and dusted off his best material!",
            "Why did the picture go to jail for a crime during an art heist? It was framed! The evidence was pretty sketchy, the whole thing was picture-perfect, and it was clearly a brush with the law!",
            "What do you call a dog magician at a pet show during trick competition? A labracadabrador! His tricks are paws-itively amazing, he's got some ruff magic, and his performance is absolutely spell-binding!",
            "What did the buffalo say to his son when he left for college in the prairie during graduation season? Bison! That's a farewell worth remembering across the plains, really herds the emotions together, and shows he's got a lot of bull-ief in his son!",
            "Why did the computer go to the doctor with technical problems during a system crash? It had a virus! It needed some anti-bodies software to boot up properly, was feeling a bit buggy, and wanted to avoid a complete system failure!",
            "What do you call a fake stone at a geology museum during rock week? A shamrock! It's not as solid as it appears, rocks a false identity, and really takes geology for granite!",
            "Why did the banana go to the doctor feeling sick during fruit flu season? It wasn't peeling well! The doc said it was an a-peel-ing case of fruit flu, it was going bananas with worry, and split when things got tough!",
            "What do you call a group of disorganized cats during a cat show? A cat-astrophe! They're feline pretty scattered, can't get their paws together, and the whole situation is purr-fectly chaotic!",
            "Why did the pencil go to school during back-to-school season? To get sharper! But it kept breaking under pressure, couldn't make the grade, and found that school was pointless without proper lead-ership!",
            "What do you call a cow on a trampoline during a thunderstorm? A milkshake in a lightning storm! It's udderly shocking, really moo-ving, and the whole situation is just electri-fying!",
            "Why did the chicken cross the playground during recess while juggling? To get to the other slide and show off her egg-cellent skills! The kids thought it was poultry in motion with a side of show-off-manship!",
            "What do you call a fish that's good at basketball in the NBA playoffs? A ball hog with championship fins! He's making waves in the league, really schooling the competition, and his shots are always net-ting results!",
            "Why did the math teacher call in sick during finals week with a calculator? She had algebra and couldn't solve her own problems, was divided by her emotions, and needed to subtract herself from the equation!",
            "What do you call a cow that's just given birth in a hospital maternity ward? Decalfinated and udderly exhausted! She needed some serious moo-ternity leave, was feeling a bit calf-fused, and wanted to milk the moment!",
            "Why did the cookie go to school during exam season with a backpack? To become a smart cookie and pass all its tests with flying crumbs, wanted to be the teacher's pet-it four, and hoped to graduate with honors in baking!",
            "What do you call a fish that's good at tennis at Wimbledon during championships? A racket fish with perfect form and a killer serve! He's serving up aces, making quite a splash on the court, and really netting the wins!",
            "Why did the banana split at the ice cream parlor during summer? It saw the sundae and couldn't resist the sweet temptation, wanted to be the top banana, and thought it would be berry delicious!",
            "What do you call a cow that's good at dancing on Broadway during opening night? A moo-ver and shaker with serious stage presence! She's got all the right moo-ves, is udderly fabulous, and really knows how to hoof it!",
            "Why did the apple go to the gym during New Year's resolution season? To get some core strength and stick to its resolution, wanted to be the apple of everyone's eye, and didn't want to be a bad apple!",
            "What do you call a fish that's good at soccer in the World Cup finals? A goal-fish with championship dreams and killer instincts! He's always scoring when it counts, making waves in the tournament, and really schooling the competition!"
        ]
        
        valid_jokes = []
        for joke in jokes:
            if not self.is_duplicate(joke):
                rating = self.rater.rate_joke(joke)
                if rating['valid']:
                    valid_jokes.append(joke)
        
        return valid_jokes[:count]
    
    def generate_all_missing_jokes(self) -> Dict[str, List[str]]:
        """Generate all missing jokes to reach 500+ total."""
        # Current counts
        current_counts = {level: len(jokes) for level, jokes in self.existing_jokes.items()}
        
        # Target counts (based on our rubric)
        target_counts = {
            '1': 100,  # Currently 117, so we need fewer Level 1
            '2': 100,  # Currently 38, need 62 more
            '3': 125,  # Currently 21, need 104 more  
            '4': 75,   # Currently 9, need 66 more
            '5': 50    # Currently 1, need 49 more
        }
        
        # Calculate how many we need for each level
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
        
        # Generate jokes for each level
        new_jokes = {}
        
        if needed['1'] > 0:
            print(f"\\n🌱 Generating {needed['1']} Level 1 jokes...")
            new_jokes['1'] = self.generate_level_1_jokes(needed['1'])
        
        if needed['2'] > 0:
            print(f"\\n🌽 Generating {needed['2']} Level 2 jokes...")
            new_jokes['2'] = self.generate_level_2_jokes(needed['2'])
        
        if needed['3'] > 0:
            print(f"\\n🌽🌽 Generating {needed['3']} Level 3 jokes...")
            new_jokes['3'] = self.generate_level_3_jokes(needed['3'])
        
        if needed['4'] > 0:
            print(f"\\n🌽🌽🌽 Generating {needed['4']} Level 4 jokes...")
            new_jokes['4'] = self.generate_level_4_jokes(needed['4'])
        
        if needed['5'] > 0:
            print(f"\\n🌽🌽🌽🌽🌽 Generating {needed['5']} Level 5 jokes...")
            new_jokes['5'] = self.generate_level_5_jokes(needed['5'])
        
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
    """Generate missing jokes to reach 500+ target."""
    generator = JokeGenerator()
    
    print("🎭 Generating missing jokes for Punnyland database...")
    new_jokes = generator.generate_all_missing_jokes()
    
    if new_jokes:
        additions_file = generator.save_new_jokes(new_jokes)
        print(f"✅ Generation complete! Review jokes in {additions_file}")
    else:
        print("✅ No new jokes needed! Database already meets targets.")


if __name__ == "__main__":
    main()