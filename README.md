# Roguelike Text-Based Adventure Game

## Overview

This is a roguelike text-based adventure game implemented in Python. Players explore events, engage in battles, collect armour, and make choices that influence their journey. The game features immersive storytelling enhanced by a slow-typing effect and random event outcomes.

---

## File Descriptions

### `helpers.py`

Utility functions supporting game mechanics and user experience. Contains only functions used in events:

- **`slow_print(text, delay=0.03)`**: Prints text to the console with a character-by-character delay to simulate typing.
- **`random_armour_drop(armour_inventory, all_armour)`**: Randomly adds a new piece of armour (that the player does not yet own) to the player's inventory.

---

### `events.py`

Contains event functions that represent encounters and choices during gameplay. Each function modifies the player's state or inventory based on decisions made:

- **`event_goblin(player)`**: Encounter with a frightened goblin and options to interact with its dropped sack.
- **`event_attack_tome(player)`**: Discover an ancient tome that can increase the player's base attack if read.
- **`event_hobbits(player)`**: Encounter hobbits, which results in health recovery and some narrative flavor.
- **`event_armour(player, armour_inventory, all_armour)`**: Find a chest that may contain armour but could also be a trap.

---

### `battle_simulator.py`

The main game script that orchestrates gameplay:

- Initializes player stats and inventory.
- Manages the game loop, invoking events from `events.py`.
- Processes player choices and updates game state.
- Handles win/loss conditions and progression through the roguelike adventure.

---

## How to Run

1. Make sure Python 3 is installed on your system.
2. Place `helpers.py`, `events.py`, and `battle_simulator.py` in the same directory.
3. Open a terminal or command prompt and navigate to this directory.
4. Run the game using:
   ```bash
   python battle_simulator.py