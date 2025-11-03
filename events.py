import time
import random
from helpers import slow_print, random_armour_drop

def event_goblin(player):  
    slow_print("\n --- EVENT: A Goblin in the Shadows ---")
    time.sleep(.5)
    slow_print("The battlefield falls silent. The last echo of the creature's roar fades into the mist.")
    time.sleep(.5)
    slow_print("You steady yourself, shaken up, but alive")
    time.sleep(.5)
    slow_print("Then...*Rustle*")
    time.sleep(.5)
    slow_print("Something moves behind a nearby rock. A pair of small, nervous eyes glint in the shadows.")
    time.sleep(.5)
    slow_print("Before you can react, a small voice whimpers out. \"Nice Hero...No hurt little Goblin...yes?\"")
    time.sleep(.5)
    slow_print("You step forward and the creatures panics. It runs off, dropping its sack in terror, and tripping over its rags as it flees into the darkness")
    time.sleep(.5)
    slow_print("""\n What do you do?
A) Open the sack
B) Call after the Goblin
C) Kick the sack aside""")  
    while True:
        choice = input("> ").lower()
        if choice == "a":
            gold = random.randint(1, 10)
            slow_print(f"You check the contents of the sack. Inisde you find {gold} gold!")
            player.gold += gold
            slow_print(f"{gold} gold added to your purse!")
            break
        elif choice == "b":
            gold = random.randint(1, 10)
            slow_print("\"Wait!\" you call out, but the creature is long gone. Still, finders keepers!")
            slow_print(f"You check the contents of the sack. Inisde you find {gold} gold!")
            player.gold += gold
            slow_print(f"{gold} gold added to your purse!")
            break
        elif choice == "c":
            slow_print("You kick the sack aside. You aren't falling for any tricksy goblins today!")
            slow_print("Still...curiosity gnaws at you as you walk away...")
            break
        else:
            slow_print("Invalid choice! Please type \"A\", \"B\", or \"C\"!")
    return False

def event_attack_tome(player):
    slow_print("\n --- EVENT: Knowledge of a Warrior ---")
    time.sleep(.5)
    slow_print("After wandering for what seems like days, you come across an abandoned cabin.")
    time.sleep(.5)
    slow_print("You venture inside and find a single, old chest. You open it and within find an ancient tome.")
    time.sleep(.5)
    slow_print("\"The Way of the Warrior\"")
    time.sleep(.5)
    slow_print("""Do you read the tome?
-Yes
-No""")
    while True:
        choice = input("> ").lower()
        if choice == "yes":
            player.base_attack += 3
            slow_print("You spend hours pouring over the knowledge of an ancient warrior. Your attack increases by 3!")
            time.sleep(.5)
            slow_print(f"Your attack is now {player.base_attack}!")
            break
        elif choice == "no":
            slow_print("You drop the tome back into the chest and leave the cabin. Who has time for reading when there are monsters to slay?")
            break
        else:
            slow_print("Invalid choice! Please type \"Yes\" or \"No\"!")
    return False

def event_hobbits(player):
    slow_print("\n --- EVENT: Tricksy little Hobbitses ---")
    time.sleep(.5)
    slow_print("The putrid smell of orc guts seems to coat everything")
    time.sleep(.5)
    slow_print("*Snff sniff*, what's that? The smell of smoke and and crispy bacon fills your lungs")
    time.sleep(.5)
    slow_print("You follow the heavenly smell and stumble across two small creatures around a campfire")
    time.sleep(.5)
    slow_print("You are starving, yet they refuse to share their food. They babble on about some quest. Something about a ring and a mountain of fire.")
    time.sleep(.5)
    slow_print("These...Hobbits they call themselves talk too much for their own good. You leave their bodies by the fire and take the bacon, scoffing it down in seconds")
    time.sleep(.5)
    player.hp = min(player.hp + 3, player.base_hp)
    slow_print(f"Health increased by 3 to {player.hp}")
    slow_print("The smaller hobbit also dropped his ring. You toss it into a nearby river, probably fake gold anyway")
    return False

def event_armour(player, armour_inventory, all_armour):
    slow_print("\n --- EVENT: Dead Man's Chest...or helmet, or greaves ---")
    time.sleep(.5)
    slow_print("Sunlight filters through the dense canopy, illuminating particles of dust that dance like tiny spirits.")
    time.sleep(0.5)
    slow_print("Something glints faintly in the underbrush—a metallic shimmer, half-buried beneath fallen leaves and tangled roots.")
    time.sleep(0.5)
    slow_print("You approach cautiously, your heartbeat quickening, wondering if this is a trap or a forgotten treasure...")
    time.sleep(.5)
    slow_print("Pushing aside moss and debris, you discover an old wooden chest, worn by time and weather.")
    time.sleep(0.5)
    slow_print("Its surface is scratched and dented, yet faint symbols of a long-forgotten smith glow softly as you approach.")
    time.sleep(0.5)
    slow_print("""\nWhat do you do?
A) Open the chest
B) Knock on the chest
C) Walk Away""")

    while True:
        choice = input ("> ").lower()
        if choice == "a":
                slow_print("You yank open the chest without caution!")
                time.sleep(0.5)
                slow_print("Suddenly, an imp leaps from the shadows, screeching and clawing at you!")
                damage = random.randint(1, 3)
                player.hp -= damage
                slow_print(f"You are scratched and bruised, taking {damage} damage! Your current HP is {player.hp}")
                if player.hp <= 0:
                    slow_print("You have died. Game Over.")
                    return True
                else:
                    slow_print("Despite the attack, you grab a piece of armour from the chest!")
                    random_armour_drop(armour_inventory, all_armour)
                    return False
        elif choice == "b":
            slow_print("You inspect the chest carefully - it seems to belong to someone...or something")
            time.sleep(.5)
            slow_print("After waiting patiently, you decide that there is no imminent danger.")
            time.sleep(.5)
            slow_print("You open the chest, finding a piece of armour inside!")
            random_armour_drop(armour_inventory, all_armour)
            return False
        elif choice == "c":
            slow_print("Deciding the risk is too great, you back away. The forest swallows the glint once more, leaving only curiosity behind.")
            return False
        else:
            slow_print("Invalid choice! Please type \"A\", \"B\", or \"C\"!")