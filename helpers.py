import random
import time

def slow_print(text, delay=0.03):
    """
    Prints the given text to the console with a delay between each character,
    creating a "typing" effect for better user experience.

    Parameters:
    text (str): The string to be printed slowly.
    delay (float): Time delay (in seconds) between printing each character. Default is 0.03s.
    """
    for char in text: #loops through each character in the text
        print(char, end='', flush=True) #prints without a new line, flush ensures it appears immediately
        time.sleep(delay) #pause for delay num of seconds between characters
    print()#prints newline after finishing the text


def random_armour_drop(armour_inventory, all_armour):
    """
    Selects a random armour piece from all available armour that the player
    does not currently own and adds it to their inventory.

    Parameters:
    armour_inventory (list): List of armour pieces currently owned by the player.
    all_armour (list): List of all possible armour pieces in the game.

    Behavior:
    - Checks which armour pieces are not yet owned.
    - If all armour is already owned, notifies the player accordingly.
    - Otherwise, randomly selects a new armour piece to add to inventory and informs the player.
    """
    armour_not_owned = [] #initilaise list to hold armour pieces player doen't yet own
    for armour in all_armour: #Loop through all armour pieces to find ones now owned
        already_owned = False
        for owned in armour_inventory:
            if armour['name'] == owned['name']:
                already_owned = True
                break
        if not already_owned:
            armour_not_owned.append(armour)
    #Notify player if all armour is owned and return
    if not armour_not_owned:
        slow_print("No new armour to find – you already have everything!")
        return
    #Randomly select a new armour piece from those not owned.
    armour_drop = random.choice(armour_not_owned)
    armour_inventory.append(armour_drop)
    slow_print(f"{armour_drop['name']} added to inventory!")
    time.sleep(.5)