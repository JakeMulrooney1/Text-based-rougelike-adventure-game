import time
import random

#import helper functions and events
from helpers import slow_print, random_armour_drop
from events import event_goblin, event_attack_tome, event_hobbits, event_armour

class Player:
    """
    Represents the player character with stats and methods
    """
    def __init__(self, hp=10, attack=3, crit_chance=0, mana =0):
        self.hp = hp
        self.attack = attack
        self.base_hp = hp            
        self.base_attack = attack 
        self.damage_multiplier = 1
        self.xp = 0
        self.crit_chance = crit_chance
        self.base_crit_chance = crit_chance
        self.mana = mana
        self.base_mana = mana
        self.unlocked_spells = ["fireball"]
        self.gold = 0
        
    def take_damage(self, damage):
        """
        Reduces player HP after applying armour defence.
        Uses get_total_defence() to calculate armour protection.
        """
        defence = get_total_defence(player_armour)
        self.hp -= max(damage - defence, 0) # damage can't be negative
        slow_print(f"You have {self.hp} HP remaining")
        time.sleep(.5)

#initialise player object
player = Player()

#control variables
quit_game = False
player_dead = False

#stats available for levelling up
stats = {
    "hp": ("base_hp", 2),
    "attack": ("base_attack", 1),
    "crit chance": ("base_crit_chance", 5),
    "mana": ("base_mana", 5)
}

#List of enemy dictionaries contating name, HP, and attack
enemies = [
    {"name": "Orc", "hp": 8, "base_hp": 8, "attack": 2},
    {"name": "Goblin", "hp": 10, "base_hp": 10, "attack": 3},
    {"name": "Bandit", "hp": 6, "base_hp": 6, "attack": 5},
    {"name": "Warg", "hp": 10, "base_hp": 10, "attack": 5},
    {"name": "Zombie", "hp": 6, "base_hp": 6, "attack": 6},
    {"name": "Skeleton Warrior", "hp": 11, "base_hp": 11, "attack": 5},
    {"name": "Giant Rat", "hp": 8, "base_hp": 8, "attack": 5},
    {"name": "Ghoul", "hp": 10, "base_hp": 10, "attack": 6},
    {"name": "Imp", "hp": 11, "base_hp": 11, "attack": 6},
    {"name": "Troll", "hp": 15, "base_hp": 15, "attack": 8},
    {"name": "Gremlin", "hp": 12, "base_hp": 12, "attack": 6},
    {"name": "Golem", "hp": 15, "base_hp": 15, "attack": 7},
    {"name": "Banshee", "hp": 8, "base_hp": 8, "attack": 10},
    {"name": "Orc Chieftan", "hp": 15, "base_hp": 15, "attack": 10},
    {"name": "Giant Spider", "hp": 15, "base_hp": 15, "attack": 8},
    {"name": "Ogre", "hp": 17, "base_hp": 17, "attack": 12},
    {"name": "Dark Sorceror", "hp": 15, "base_hp": 15, "attack": 13},
    {"name": "Flame Elemental", "hp": 18, "base_hp": 18, "attack": 13},
    {"name": "Frost Troll", "hp": 20, "base_hp": 20, "attack": 15},
    {"name": "Dark Knight", "hp": 25, "base_hp": 25, "attack": 20}
    
]

#all available spells, their mana cost and damage
all_spells = [
    {"name": "Fireball", "mana_cost": 3, "damage": 10},
    {"name": "Blizzard", "mana_cost": 15, "damage": 30},
    {"name": "Chaos Storm", "mana_cost": 30, "damage": 50}
]

#shop inventory of items available to buy
shopkeeper_items = [
    {"name": "Potion of Healing", "cost": 5},
    {"name": "Potion of Mana Regeneration", "cost": 5},
    {"name": "Elixir of Strength", "cost": 5}
]

#player's equipped armour slots initalised as empty
player_armour = {"head": None,
                 "body": None,
                 "legs": None
                }

#all armour pieces that can be found
all_armour = [
    {"name": "Leather Helmet", "defence": 1, "slot": "head"},
    {"name": "Leather Chestplate", "defence": 1, "slot": "body"},
    {"name": "Leather Greaves", "defence": 1, "slot": "legs"},
]

def equip_armour(player_armour, item):
    """
    Equip armour piece in the appropriate slot.
    If slot is occupied, replace old armour and notify player.
    """
    slot = item['slot']
    old_armour = player_armour[slot]
    player_armour[slot] = item
    if old_armour:
        slow_print(f"{old_armour['name']} replaced with {item['name']} in {slot} slot!")
    else:
        slow_print(f"{item['name']} equipped in {slot} slot!")


def get_total_defence(player_armour):
    """
    Sum total defence from all equipped armour.
    """
    total_defence = 0
    for slot in player_armour.values():
        if slot:
            total_defence += slot['defence']
    return total_defence


def basic_attack(player, enemy):
    """
    Calculate and apply player's basic attack damage on enemy.
    Considers crit chance and dmg multiplier.
    Returns True is enemy defeated, False if not.
    """
    damage = player.attack * player.damage_multiplier
    if random.randint(1, 100) <= player.crit_chance:
        damage = int(player.attack * 1.5)
        slow_print("Critical hit!")
    enemy['hp'] -= damage
    slow_print(f"You attacked the {enemy['name']} for {damage} damage!")
    time.sleep(.5)

    player.damage_multiplier = 1 #rests multiplier after attack
    
    if enemy['hp'] > 0:
        slow_print(f"The {enemy['name']} has {enemy['hp']} HP remaining")
        time.sleep(.5)
        return False
    else:
        slow_print(f"{enemy['name']} defeated!")
        player.xp += 1
        time.sleep(.5)
        slow_print("1xp gained!")
        time.sleep(.5)
        #random chance enemy drops armour
        if random.randint(1, 7) == 1:
            slow_print(f"The {enemy['name']} dropped a piece of armour!")
            time.sleep(.5)
            random_armour_drop(armour_inventory, all_armour)
        return True

def cast_spell(player, enemy, spell_name):
    """
    Checks mana, spell validity, and applies amage and crit chance.
    Returns True if enemy defeated, False if still alive, of invalid  for errors.
    """
    spell_dict = {}
    for s in all_spells:
        if s['name'].lower() == spell_name:
            spell_dict = s
            break
    if not spell_dict:
        slow_print("Invalid choice! Please choose a spell from the menu.")
        return "invalid" 
    
    mana_cost = spell_dict['mana_cost']
    damage = spell_dict['damage'] * player.damage_multiplier
        
    if player.mana < mana_cost:
        slow_print(f"You don't have enough mana to use {spell_name}!")
        return "invalid"

    player.mana -= mana_cost
    if random.randint(1, 100) <= player.crit_chance:
        damage = int(damage * 1.5)
        slow_print("Critical hit!")
    enemy['hp'] -= damage
    slow_print(f"You attacked the {enemy['name']} with {spell_name} for {damage} damage!")

    player.damage_multiplier = 1
                            
    if enemy['hp'] > 0:
        slow_print(f"The {enemy['name']} has {enemy['hp']} HP remaining")
        return False
    else:
        slow_print(f"{enemy['name']} defeated!")
        player.xp += 1
        time.sleep(.5)
        slow_print("1xp gained!")
        time.sleep(.5)
        if random.randint(1, 7) == 1:
            slow_print(f"The {enemy['name']} dropped a piece of armour!")
            random_armour_drop(armour_inventory, all_armour)
        return True
                            

def enemy_attack(player, enemy):
    """
    Enemy performs an attack on player.
    Returns True if player dies, else False.
    """
    slow_print(f"The enemy {enemy['name']} attacks you for {enemy['attack']} damage!")
    time.sleep(.5)
    player.take_damage(enemy['attack'])
    if player.hp <= 0:
        slow_print("You have died. Game Over.")
        return True
    return False

def shopkeeper():
    """
    Handles shop interactions allowing the player to buy consumables.
    """
    global consumable_inventory
    
    item_dict = {}
    for i in shopkeeper_items:
        item_dict[i['name'].lower()] = i

    while True:
        slow_print(f"\n--- SHOP ---\nCurrent Gold: {player.gold}")
        for item in item_dict.values():
            slow_print(f"- {item['name']} ({item['cost']} gold)")
        slow_print("- Back")
        choice = input("> ").lower()
        if choice == "back":
            slow_print("Safe travels, Adventurer!")
            break
        elif choice in item_dict:
            item = item_dict[choice]
            if player.gold >= item['cost']:
                player.gold -= item['cost']
                if item['name'] in consumable_inventory:
                    consumable_inventory[item['name']] += 1
                else:
                    consumable_inventory[item['name']] = 1
                slow_print(f"{item['name']} added to inventory!")
                time.sleep(1)
                slow_print("Fine choice Adventurer! Anything else?")
            else:
                slow_print("Sorry adventurer. You don't have enough gold for that!")
        else:
            slow_print("Invalid choice! Please select an item from the menu")


def events(player, armour_inventory, all_armour):
    """
    Randmoly triggers one of the imported game events.
    Returns True is the event results in the player's death.
    """
    events_list = [event_goblin, event_attack_tome, event_hobbits, event_armour]
    result = random.choice(events_list)(player, armour_inventory, all_armour)
    return True if result is True else False

#tracks scoring metrics
kills = 0
deaths = 0

### MAIN GAME LOOP ###

while True:
    #Reset player stats at start of each run
    player_dead = False
    player.hp = player.base_hp
    player.attack = player.base_attack
    player.crit_chance = player.base_crit_chance
    player.mana = player.base_mana

    #initialise inventories
    consumable_inventory = {}
    armour_inventory = []

    #Reset enemy HP at start of encounter
    for enemy in enemies:
        enemy['hp'] = enemy['base_hp']
        slow_print(f"You encounter an enemy {enemy['name']}! What will you do?")
        time.sleep(.5)
        
        #Battle loop - runs while both player and enemy are alive
        while enemy['hp'] > 0 and player.hp > 0:

            #get equipped armour names, display "None" if no armour equipped
            head_name = player_armour['head']['name'] if player_armour['head'] else "None"
            body_name = player_armour['body']['name'] if player_armour['body'] else "None"
            legs_name = player_armour['legs']['name'] if player_armour['legs'] else "None"
            """
            Display the battle menu showing options and current stats:
            - Player HP and mana
            - Equipped armour pieces
            - Enemy HP
            """
            print(f"""\n--- MENU ---
-Attack          HP: {player.hp}/{player.base_hp}          Armour:          {enemy['name']} HP: {enemy['hp']}/{enemy['base_hp']}
-Magic           Mana: {player.mana}/{player.base_mana}          Head: {head_name}        
-Inventory                          Body: {body_name}
-Quit                               Legs: {legs_name}""")
            choice = input("> ").lower() #get player's input choice
            
            if choice == "attack":
                #player performs basic attack
                enemy_defeated = basic_attack(player, enemy)
                if enemy_defeated:
                    kills += 1 #increase kill count
                    #25% chance for each enemy to drop gold
                    if random.randint(1, 100) <= 25:
                        player.gold += 1
                        time.sleep(1)
                        slow_print(f"{enemy['name']} dropped 1 gold!")
                        time.sleep(1)
                        #open shop after every 5 kills
                    if player.xp % 5 == 0:
                        slow_print("Shopkeeper: Welcome Adventurer! Take a look at my wares. Anything strike your fancy?")
                        shopkeeper()
                        #1 in 9 chance for random event to occur (33% chance each 3 xp)
                    if player.xp % 3 == 0 and random.randint(1, 3) == 1:
                        player_dead = events(player, armour_inventory, all_armour)
                        if player_dead:
                            deaths += 1
                            break
                    break #end current fight loop to next enemy
                #enemy attacks if not dead
                player_dead = enemy_attack(player, enemy)
                if player_dead:
                    deaths += 1
                    break
                    
            elif choice == "magic":
                #spellcasting menu loop
                while True:
                    slow_print("Select a spell to use, or type \"back\" to return to the menu.")
                    time.sleep(1)
                    slow_print("\n--- SPELLS ---")
                    slow_print(f"Current mana: {player.mana}")

                    #show only unlcoked spells in spells menu
                    spell_dict = {}
                    for s in all_spells:
                        if s['name'].lower() in player.unlocked_spells:
                            spell_dict[s['name'].lower()] = s

                    for s in spell_dict.values():
                        slow_print(f"-{s['name']} (Cost: {s['mana_cost']})")
                    slow_print("-Back")

                    spell = input("> ").lower()
                    if spell == "back":
                        break
                    #attempt to cast spell on emeny
                    enemy_defeated = cast_spell(player, enemy, spell)
                    if enemy_defeated == "invalid":
                        #invalid choice, prompt again
                        continue
                    elif enemy_defeated:
                        #if enemy dead, handles drops/events and increase kill counter
                        kills +=1
                        if random.randint(1, 100) <= 25:
                            player.gold += 1
                            time.sleep(1)
                            slow_print(f"{enemy['name']} dropped 1 gold!")
                            time.sleep(1)
                        if player.xp % 5 == 0:
                            slow_print("Shopkeeper: Welcome Adventurer! Take a look at my wares. Anything strike your fancy?")
                            shopkeeper()
                        if player.xp % 3 == 0 and random.randint(1, 3) == 1:
                            player_dead = events(player, armour_inventory, all_armour)
                            if player_dead:
                                deaths += 1
                                break
                        break
                    else:
                        player_dead = enemy_attack(player, enemy) #enemt ayyacks if not dead
                        if player_dead:
                            deaths += 1
                            break
                        break
                        
            elif choice =="inventory":
                #Inventory menu: access consumables and armour
                while True:
                    print("\n--- INVENTORY ---")
                    print("""-Consumables
-Armour
                    \n-Exit""")
                    inv_choice = input("> ").lower()
                    
                    if inv_choice == "exit":
                        slow_print("Closing inventory...\n")
                        break
                        
                    elif inv_choice == "consumables":
                        #Display and use consumables if available
                        if not consumable_inventory:
                            slow_print("You have no consumables in your inventory.")
                            break
                            
                        for item_name, count in consumable_inventory.items():
                            slow_print(f" - {item_name} x{count}")
                        slow_print("\n-Back")
                        consumable_choice = input("> ").lower()
                        if consumable_choice == "back":
                            break
                        elif consumable_choice == "potion of healing" and "Potion of Healing" in consumable_inventory:
                            player.hp = min(player.hp + 10, player.base_hp)#Heal player by 10 (up to max)
                            consumable_inventory["Potion of Healing"] -= 1
                            if consumable_inventory["Potion of Healing"] == 0:
                                del consumable_inventory["Potion of Healing"]
                            slow_print(f"Your health increased by 10 to {player.hp}!")
                            time.sleep(1)
                        elif consumable_choice == "potion of mana regeneration" and "Potion of Mana Regeneration" in consumable_inventory:
                            player.mana = min(player.mana + 10, player.base_mana)#Restore 10 mana (up to max)
                            consumable_inventory["Potion of Mana Regeneration"] -= 1
                            if consumable_inventory["Potion of Mana Regeneration"] == 0:
                                del consumable_inventory["Potion of Mana Regeneration"]
                            slow_print(f"Your mana increased by 10 to {player.mana}!")
                            time.sleep(1)
                        elif consumable_choice == "elixir of strength" and "Elixir of Strength" in consumable_inventory:
                            player.damage_multiplier = 1.5#Temporarily boost player damage for next attack
                            consumable_inventory["Elixir of Strength"] -= 1
                            if consumable_inventory["Elixir of Strength"] == 0:
                                del consumable_inventory["Elixir of Strength"]
                            slow_print("Your next attack will do 50% more damage!")
                            time.sleep(1)
                        else:
                            slow_print("Invalid choice!. Please select an item from your inventory, and type \"back to return\"!")
                            
                    elif inv_choice == "armour":
                        #Display armour if available in inventory
                        if not armour_inventory:
                            slow_print("You have no armour in your inventory.")
                            break
                            
                        for armour in armour_inventory:
                            slow_print(f"{armour['name']}")
                        slow_print("\n-Back")
                        armour_choice = input("> ").lower()

                        if armour_choice == "back":
                            break

                        selected_armour = None
                        for armour in armour_inventory:
                            #Equip armour
                            if armour['name'].lower() == armour_choice: 
                                selected_armour = armour
                                break

                        if selected_armour:
                            equip_armour(player_armour, selected_armour)
                        else:
                            slow_print("Invalid choice! Please choose an option from your inventory.")
                            
                        

                    else:
                        slow_print("Invalid choice! Please choose an option from the menu.")
                        
            #quit game loop cleanly
            elif choice == "quit":
                slow_print("Farewell Adventurer!")
                quit_game = True
                break

            else:
                slow_print("Invalid choice! Please choose an option from the menu.")

        #After enemy defeated, check for special spell unlocks based on enemy killed
        if enemy['hp'] <=0:
            if enemy['name'] == "Troll" and "Blizzard" not in player.unlocked_spells:
                slow_print("Blizzard spell unlocked!")
                player.unlocked_spells.append("blizzard")
            elif enemy['name'] == "Dark Knight" and "Chaos Storm" not in player.unlocked_spells:
                slow_print("Chaos Storm spell unlocked!")
                player.unlocked_spells.append("chaos storm")

        #break main enemy loop if player quits or dies
        if quit_game or player_dead == True:
            break 

    #allow levelling up afater player death and dispaly score
    if player_dead == True:
        slow_print(f"Your current score: {kills} kill(s), {deaths} death(s)")
        slow_print("You have died, but you aren't finished yet. Time to level up!")
        time.sleep(1)
        slow_print(f"You gained {player.xp} xp!")
        time.sleep(1)
        slow_print(f"""For each xp gained, you can level up one stat. Which stat would you like to level up? You can also quit now by entering \"Quit\"
\n--- MENU ---
-HP ({player.base_hp})
-Attack ({player.base_attack})
-Crit Chance ({player.base_crit_chance})
-Mana({player.base_mana})
\n-Quit""")
        
        while player.xp > 0:
            level_choice = input("> ").lower()
            if level_choice in stats:
                attr, amount = stats[level_choice]
                setattr(player, attr, getattr(player, attr) + amount) #increase chosen stat by its amount as per dict
                slow_print(f"New {level_choice}: {getattr(player, attr)}")
                player.xp -= 1
            elif level_choice == "quit":
                slow_print("Farewell Adventurer!")
                quit_game = True
                break
            else:
                slow_print("Invalid choice! Please choose an option from the menu.")
        time.sleep(1)
        slow_print("Time to go again!")
        time.sleep(1)
        
    if quit_game == True:
        break #exit game if player chose to quit