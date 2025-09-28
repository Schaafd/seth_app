#!/usr/bin/env python3
"""
Simple manual joke generator to fill remaining gaps.
"""

import json
from pathlib import Path


def create_remaining_jokes():
    """Create the remaining jokes needed to meet targets."""
    
    # Level 2 jokes (need 54 more)
    level_2_jokes = [
        "What do you call a snobby gardener? A snap-dragon!",
        "Why don't mountains ever get cold? They have snow caps!",
        "What do you call a rabbit that's good at karate? A kung-fu bunny!",
        "Why did the musician break up with his metronome? It couldn't keep time!",
        "What do you call a vegetable that's always complaining? A whine-apple!",
        "Why don't clouds ever get tired? They're always floating around!",
        "What do you call a snake that bakes? A pie-thon!",
        "Why did the tree go to the dentist? It needed a root canal!",
        "What do you call a flower that runs on electricity? A power plant!",
        "Why don't rivers ever get lost? They always know which way to flow!",
        "What do you call a dinosaur that loves to sleep? A dino-snore!",
        "Why did the sun go to school? To get brighter!",
        "What do you call a bird that's afraid to fly? A chicken!",
        "Why don't deserts ever get thirsty? They're used to being dry!",
        "What do you call a fish that wears a crown? Your royal high-ness!",
        "Why did the clock go to therapy? It had too much time on its hands!",
        "What do you call a dog that works at a bank? A golden retriever!",
        "Why don't bees ever get stressed? They're always buzzing with excitement!",
        "What do you call a cat that works out? A gym-cat!",
        "Why did the book go to the doctor? Its spine was hurting!",
        "What do you call a cow that plays violin? A moo-sician!",
        "Why don't pencils ever get lonely? They come in packs!",
        "What do you call a sheep covered in chocolate? A candy baa!",
        "Why did the computer catch a cold? It had a virus!",
        "What do you call a pig that knows martial arts? A pork chop!",
        "Why don't shoes ever get tired? They're sole survivors!",
        "What do you call a bear that's stuck in the rain? A drizzly bear!",
        "Why did the bicycle fall asleep? It was two-tired!",
        "What do you call a turtle that flies planes? A pilot-tortoise!",
        "Why don't eggs play sports? They might crack under pressure!",
        "What do you call a horse that lives next door? A neigh-bor!",
        "Why did the cookie cry? Because its mom was a wafer so long!",
        "What do you call a dinosaur that crashes cars? Tyrannosaurus Wrecks!",
        "Why don't storms ever apologize? They're too thunder-struck!",
        "What do you call a sleeping bull? A bulldozer!",
        "Why did the math book look worried? It was full of problems!",
        "What do you call a fish that needs help singing? Auto-tuna!",
        "Why don't calendars ever get upset? Their days are numbered!",
        "What do you call a dog magician? A labracadabrador!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a fake noodle? An impasta!",
        "Why don't skeletons fight? They don't have the guts!",
        "What do you call a sleeping deer? Nap-kin!",
        "Why did the teddy bear say no to dessert? She was stuffed!",
        "What do you call a fish wearing a bowtie? Sofishticated!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a pig that does karate? A pork chop!",
        "Why did the tomato turn red? It saw the salad dressing!",
        "What do you call a cow with no legs? Ground beef!",
        "Why don't oysters donate to charity? They're shellfish!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the golfer bring extra pants? In case he got a hole in one!",
        "What do you call a factory that makes good products? A satisfactory!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a dinosaur that loves to sleep? A dino-snore!"
    ]
    
    # Level 3 jokes (need 4 more)
    level_3_jokes = [
        "What do you call an elephant that doesn't matter? An irr-elephant!",
        "What do you call a rhinoceros that loves to party? A party-ceratops!",
        "What do you call a hippopotamus that tells time? A hippo-clock-amus!",
        "What do you call a crocodile in a vest? An investigator!"
    ]
    
    # Level 4 jokes (need 37 more)
    level_4_jokes = [
        "Why did the cat become a lawyer? Because it was purr-suasive and had great claw-se for argument!",
        "What do you call a dog that works at a coffee shop? A barista with a ruff attitude but paws-itive reviews!",
        "Why did the cow start a band? It was udderly musical and really knew how to milk the audience!",
        "What do you call a pig that tells jokes at a comedy club? A ham-comedian with bacon-breaking humor!",
        "Why did the fish become a therapist? It was great at helping others scale their problems and find their porpoise!",
        "What do you call a chicken that solves mysteries? A clue-ck with egg-cellent detective skills!",
        "Why did the horse become a motivational speaker? It was always stable and knew how to stirrup emotions!",
        "What do you call a sheep that practices yoga? A baa-lanced individual with wool-derful flexibility!",
        "Why did the rabbit open a bakery? It was great at making carrot cake and had a bunny for business!",
        "What do you call a turtle that loves to race? A slow-and-steady competitor with shell-shocking determination!",
        "Why did the elephant become a memory coach? It never forgets and has trunk-loads of experience!",
        "What do you call a giraffe that works at a library? A high-reaching librarian with neck-ceptional service!",
        "Why did the lion start a hair salon? It was the mane attraction with a roar-ing business!",
        "What do you call a bear that loves to dance? A bear-y good dancer with grizzly moves!",
        "Why did the monkey become a computer programmer? It was great at debugging and going bananas over code!",
        "What do you call a snake that works in construction? A hiss-tory maker with coil-osal building skills!",
        "Why did the frog become a singer? It had a ribbiting voice and could really croak out a tune!",
        "What do you call a duck that loves photography? A quack-shot artist with a bill for capturing moments!",
        "Why did the owl become a teacher? It was a wise choice with hoot-standing educational skills!",
        "What do you call a penguin that loves to cook? A chill chef with ice-ceptional culinary skills!",
        "Why did the kangaroo start a delivery service? It could really hop to it and had pouch-itive reviews!",
        "What do you call a koala that works at a spa? A eucalyptus specialist with bear-y relaxing treatments!",
        "Why did the zebra become an artist? It was great at drawing lines and had stripe-ing creativity!",
        "What do you call a camel that works in logistics? A hump-day hero with desert-ed dedication!",
        "Why did the fox become a news reporter? It was sly-ly good at getting the scoop!",
        "What do you call a wolf that loves to howl at concerts? A pack-leader with howl-ing good taste!",
        "Why did the deer become a track coach? It was fast and had a hart for helping others!",
        "What do you call a moose that loves gardening? A antler-ed expert with a passion for growing!",
        "Why did the squirrel become a financial advisor? It was nuts about saving and had acorn-y sense of humor!",
        "What do you call a raccoon that loves to clean? A mask-ed hero with paw-some organizational skills!",
        "Why did the skunk become a perfume maker? It had a nose for scents and a scent-sational business!",
        "What do you call a porcupine that loves to hug? A point-ed friend with sharp wit but soft heart!",
        "Why did the beaver become a carpenter? It had dam good skills and could really chew through projects!",
        "What do you call a bat that loves baseball? A wing-ed wonder with bat-ting average skills!",
        "Why did the hamster become a personal trainer? It loved running on wheels and had wheel-y good energy!",
        "What do you call a guinea pig that loves music? A squeaky-clean performer with pig-ture perfect pitch!",
        "Why did the chinchilla become a fashion designer? It had fur-bulous taste and dust-bath fresh ideas!"
    ]
    
    # Level 5 jokes (need 47 more)
    level_5_jokes = [
        "Why did the cat become a stand-up comedian at the fancy theater during opening night? Because it was purr-fectly positioned, feline fine about everything, and whisker-ing away all doubts! Talk about cat-astrophically good with paws-itively meow-nificent results that left the audience in stitches!",
        "What do you call a cow that performs magic tricks, teaches calculus, and runs marathons while juggling? A moo-gician with udderly incredible skills, legen-dairy dedication, and a no-bull attitude! That's what I call moo-ving and shaking with pasture-perfect performance!",
        "I told my dog about quantum physics while we were skydiving during a thunderstorm. It said 'That's paws-itively mind-blowing!' Then it added 'But also tail-waggingly confusing!' Finally it concluded 'Overall, it's ruff but fascinating!' I thought, 'Doggone brilliant with bow-wow intellectual curiosity!'",
        "A pig walked into a five-star restaurant carrying a briefcase and a harmonica during the dinner rush. The maître d' said 'Why the formal presentation?' The pig replied 'I'm ham-ming it up for my new business venture!' Everyone agreed it was squealing success with bacon-breaking innovation!",
        "What's the difference between a symphony at Carnegie Hall and a fish at a sushi restaurant? One is a masterpiece of musical excellence with perfect harmony, the other is fin-tastically fresh with scale-ing flavors! Both are equally hook-ing in their own spectacular ways!",
        "Why did the elephant become a memory therapist at the wellness center during peak season? Because it was trunk-fully equipped, never forgets anything important, and had pachy-dermal wisdom! Talk about mammoth success with ear-resistibly effective treatments that clients remember forever!",
        "What do you call a chicken that writes novels, solves crosswords, and performs Shakespeare while tap dancing? A literary genius with egg-ceptional talent, feather-brained creativity, and comb-pletely amazing performances! That's what I call poultry in motion with egg-straordinary artistic expression!",
        "I told my rabbit friend about rocket science while we were bungee jumping off the Empire State Building. It said 'That's hop-efully accurate!' Then it added 'But also ear-resistibly complex!' Finally it concluded 'Overall, it's bunny-derful knowledge!' I thought, 'Some-bunny's really carrot-ing about education!'",
        "A horse walked into a Broadway theater carrying a violin and a top hat during intermission of a major production. The director said 'Why the musical entrance?' The horse replied 'I'm just trying to stirrup some interest in my one-horse show!' Everyone agreed it was mane-ly spectacular entertainment!",
        "What's the difference between a painting in the Louvre and a sheep in a meadow? One is a priceless work of art that inspires millions, the other is wool-derfully peaceful with baa-utiful simplicity! Both are equally flock-ing amazing in their unique artistic expressions!",
        "Why did the monkey become a computer scientist at Silicon Valley during the tech boom? Because it was bananas about innovation, had ape-solutely brilliant coding skills, and could swing through problems with ease! Talk about going bananas with primo-rdial programming genius!",
        "What do you call a turtle that teaches philosophy, practices law, and performs surgery while doing yoga? A shell-shocked intellectual with slow-and-steady wisdom, turtle-ly amazing skills, and snap-ping good judgment! That's what I call shell-ebrated excellence with reptile dysfunction... wait, that came out wrong!",
        "I told my duck friend about advanced mathematics while we were white-water rafting through the Grand Canyon. It said 'That's quack-tastic knowledge!' Then it added 'But also bill-iantly complicated!' Finally it concluded 'Overall, it's duck-ing incredible!' I thought, 'Water you thinking? This duck is absolutely fowl-some!'",
        "A bear walked into a gourmet honey shop carrying a cookbook and a chef's hat during the busy harvest season. The shopkeeper said 'Why the culinary preparation?' The bear replied 'I'm just trying to bear down on my cooking skills!' Everyone agreed it was bear-y impressive with claw-some potential!",
        "What's the difference between a rocket at NASA and a kangaroo in Australia? One reaches for the stars with scientific precision and cosmic ambition, the other hops around with pouch-itive energy! Both are equally jump-ing with out-of-this-world potential for amazing achievements!",
        "Why did the fox become a detective at Scotland Yard during the Victorian era? Because it was sly-ly observant, had tail-telling investigative skills, and could den-y nothing to justice! Talk about fur-ensic excellence with fox-y problem-solving abilities that left criminals out-fox-ed!",
        "What do you call a penguin that conducts orchestras, teaches ice skating, and runs an Antarctic tour company while wearing a tuxedo? A formally dressed entrepreneur with ice-cold business acumen, slip-pery smooth operations, and waddle-ing success! That's what I call black-and-white excellence with flipper-fect execution!",
        "I told my owl friend about aerodynamics while we were hang-gliding over the Swiss Alps at midnight. It said 'That's owl-standing information!' Then it added 'But also hoot-rifically complex!' Finally it concluded 'Overall, it's a wise subject!' I thought, 'Who's the smart one now? This owl is absolutely talon-ted!'",
        "A giraffe walked into an art gallery carrying a paintbrush and a ladder during the opening night exhibition. The curator said 'Why the elevated preparation?' The giraffe replied 'I'm just trying to reach new heights in my artistic expression!' Everyone agreed it was neck-st level creativity with tall-ented vision!",
        "What's the difference between a diamond in Tiffany's and a zebra in the Serengeti? One sparkles with precious brilliance and timeless elegance, the other dazzles with stripe-ing natural beauty! Both are equally rare treasures that stripe up conversations wherever they appear!",
        "Why did the lion become a motivational speaker at corporate retreats during leadership conferences? Because it had mane-ly charismatic presence, roar-ing confidence, and pride-ful speaking abilities! Talk about king-ly performance with claw-some inspiration that left audiences roaring with approval!",
        "What do you call a dolphin that practices medicine, performs in circuses, and teaches marine biology while doing backflips? A fin-credibly talented professional with whale-ing good bedside manner, splash-ing entertainment value, and deep-sea knowledge! That's what I call porpoise-ful living with fin-tastic career diversity!",
        "I told my squirrel friend about stock market investments while we were zip-lining through the Amazon rainforest. It said 'That's nuts-olutely fascinating!' Then it added 'But also acorn-y subject!' Finally it concluded 'Overall, it's tree-mendous knowledge!' I thought, 'This squirrel is nuts about finance and bushy-tailed with investment wisdom!'",
        "A peacock walked into a fashion show carrying a mirror and a feather boa during Paris Fashion Week. The designer said 'Why the elaborate accessories?' The peacock replied 'I'm just trying to feather my nest in the fashion industry!' Everyone agreed it was preen-ty spectacular with tail-ored excellence!",
        "What's the difference between a telescope at Mount Palomar and a hawk soaring over the Rocky Mountains? One peers into the cosmos with scientific precision and stellar focus, the other soars with hawk-ward grace! Both are equally talon-ted at reaching incredible heights and keeping their eyes on amazing targets!",
        "Why did the whale become an opera singer at the Metropolitan Opera during the season finale? Because it had whale-ing good vocal range, deep-sea resonance, and could make waves with every performance! Talk about mammoth talent with fin-esse that left audiences spouting with enthusiasm!",
        "What do you call a chameleon that works as a therapist, performs magic shows, and teaches art classes while changing colors? A multi-faceted professional with blend-ing therapeutic skills, color-ful personality, and scale-ing artistic abilities! That's what I call adapt-able excellence with hue-morous talent!",
        "I told my flamingo friend about ballet techniques while we were performing synchronized swimming in the Everglades. It said 'That's pink-redibly graceful!' Then it added 'But also leg-endarily difficult!' Finally it concluded 'Overall, it's fla-mingo-nificent!' I thought, 'This bird is absolutely stand-out with one-legged perfection!'",
        "A rhinoceros walked into a china shop carrying bubble wrap and safety gloves during the holiday rush. The owner said 'Why the protective measures?' The rhinoceros replied 'I'm just trying to horn in on the delicate business without causing a crash!' Everyone agreed it was point-ed wisdom with thick-skinned consideration!",
        "What's the difference between a Stradivarius violin at a concert hall and a cricket in a meadow? One creates heavenly music with masterful craftsmanship and perfect pitch, the other chirps with natural rhythm! Both are equally string-ing together beautiful sounds that resonate with their audiences!",
        "Why did the octopus become a multitasking consultant at Fortune 500 companies during busy mergers? Because it had eight arms for juggling projects, ink-credible problem-solving skills, and could tentacle any challenge! Talk about well-armed success with sucker-punch efficiency!",
        "What do you call a butterfly that teaches transformation seminars, performs aerial acrobatics, and runs a flower delivery service while migrating thousands of miles? A metamorphosis expert with flutter-ing business acumen, wing-ed delivery precision, and monarch-ical dedication! That's what I call butter-fly success with cater-pillar-to-CEO transformation!",
        "I told my porcupine friend about acupuncture techniques while we were practicing martial arts in a bamboo forest. It said 'That's point-edly relevant!' Then it added 'But also needle-ssly complicated!' Finally it concluded 'Overall, it's sharp thinking!' I thought, 'This porcupine really knows how to get to the point with quill-ity education!'",
        "A hamster walked into a fitness center carrying a protein shake and a tiny stopwatch during the marathon training session. The trainer said 'Why the athletic preparation?' The hamster replied 'I'm just trying to wheel my way to victory!' Everyone agreed it was wheel-y impressive with cheek-pouch determination!",
        "What's the difference between a masterpiece at the Smithsonian and a beaver building a dam? One is preserved art that inspires generations with cultural significance, the other creates engineering marvels! Both are equally dam impressive with their own forms of architectural excellence and wood-erful craftsmanship!",
        "Why did the parrot become a foreign language instructor at the United Nations during international conferences? Because it had poly-glot abilities, colorful teaching methods, and could wing it in any situation! Talk about bird-brained brilliance with feather-ed linguistic skills that left students squawking with delight!",
        "What do you call a sloth that runs a productivity consulting firm, teaches time management, and practices speed reading while hanging upside down? An ironic success story with slow-and-steady wisdom, hang-ing in there persistence, and claw-some time optimization! That's what I call sloth-ful efficiency with tree-mendous patience!",
        "I told my hummingbird friend about energy conservation while we were power-lifting at a high-altitude gym. It said 'That's buzz-worthy information!' Then it added 'But also wing-ingly exhausting!' Finally it concluded 'Overall, it's tweet perfection!' I thought, 'This hummingbird is absolutely hover-achiever with nectar-sweet knowledge!'",
        "A moose walked into a antique shop carrying reading glasses and a magnifying glass during the estate sale weekend. The appraiser said 'Why the visual aids?' The moose replied 'I'm just trying to antler-lyze the value of these collectibles!' Everyone agreed it was rack-ing up expertise with moose-eum quality knowledge!",
        "What's the difference between a symphony conductor at Carnegie Hall and a woodpecker in an old oak tree? One orchestrates beautiful music with precise timing and artistic vision, the other creates rhythmic percussion! Both are equally peck-uliar artists with their own drumming techniques and tree-mendous dedication to their craft!",
        "Why did the seal become a marine biologist at the aquarium during shark week? Because it had seal-ed expertise in aquatic life, flipper-fect swimming skills, and could navigate any depth of knowledge! Talk about water-tight qualifications with seal-iously impressive marine credentials!",
        "What do you call a raccoon that works as a recycling consultant, teaches environmental science, and runs a cleaning service while wearing tiny gloves? A mask-ed environmental hero with paws-itively green initiatives, ring-tailed dedication, and trash-to-treasure expertise! That's what I call raccoon-ciliation between nature and human progress!",
        "I told my chinchilla friend about dust-free computing while we were deep-cleaning a server room in Silicon Valley. It said 'That's dust-urbingly relevant!' Then it added 'But also fur-rightening complex!' Finally it concluded 'Overall, it's whisker-ing good technology!' I thought, 'This chinchilla is absolutely soft-ware expert with dust-busting knowledge!'",
        "A platypus walked into a genetics laboratory carrying a textbook on evolution during Darwin's birthday celebration. The scientist said 'Why the educational preparation?' The platypus replied 'I'm just trying to bill-d my understanding of my unique heritage!' Everyone agreed it was duck-bill-ious learning with egg-laying mammal mysteries!",
        "What's the difference between a rocket scientist at SpaceX and a eagle soaring over the Grand Canyon? One reaches for the stars with mathematical precision and rocket fuel, the other soars with natural grace! Both are equally fly-ing high with their own methods of achieving lofty goals and eagle-eye vision!",
        "Why did the lobster become a hand surgeon at the medical center during the busy emergency season? Because it had claw-some dexterity, shell-shocking precision, and could really get to the meat of any problem! Talk about crust-acean excellence with pincer-point accuracy that left patients snapping with satisfaction!",
        "What do you call a hedgehog that teaches defensive driving, practices martial arts, and runs a security company while rolling into a ball? A spike-ed protection specialist with needle-sharp reflexes, quill-ified training expertise, and point-ed business acumen! That's what I call hedge-ing your bets with prickly perfection!",
        "I told my toucan friend about tropical meteorology while we were studying weather patterns in the Amazon rainforest. It said 'That's beak-on accurate!' Then it added 'But also color-fully complex!' Finally it concluded 'Overall, it's toucan-do knowledge!' I thought, 'This toucan really has a nose for weather with beak-coming expertise and tropical intelligence!'"
    ]
    
    return {
        '2': level_2_jokes,
        '3': level_3_jokes,
        '4': level_4_jokes,
        '5': level_5_jokes
    }


def main():
    """Generate and save the remaining jokes."""
    print("🎭 Creating remaining jokes manually...")
    
    new_jokes = create_remaining_jokes()
    
    # Save to additions file
    additions_path = Path("punnyland/data/jokes_additions.json")
    
    with open(additions_path, 'w') as f:
        json.dump(new_jokes, f, indent=2, ensure_ascii=False)
    
    total_added = sum(len(jokes) for jokes in new_jokes.values())
    print(f"💾 Saved {total_added} new jokes to {additions_path}")
    
    print("\\n📊 Generated joke distribution:")
    for level, jokes in new_jokes.items():
        print(f"  Level {level}: {len(jokes)} jokes")
    
    print("✅ Generation complete!")


if __name__ == "__main__":
    main()