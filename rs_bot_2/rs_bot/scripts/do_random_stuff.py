import os
import sys
import time
import keyboard

# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

# Import the desired modules from the parent directory
from attack_scripts.attack_highlighted_npc import start_attacking_marked_npcs
from walker.walker import walk_to_destination
from walker.get_destination_coordinates import search_place_coordinates
from helpers.api_request_events import check_if_inventory_is_full
from bank_items.bank_items import put_inventory_in_bank
from helpers.pickup_items import pickup_dropped_items


def tannery():
    print("This will be the function to go tannery, we would need to have cowhide in bank...")
    return