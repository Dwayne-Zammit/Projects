import os
import sys
import time
import keyboard
import configparser

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


# Initialize ConfigParser
config = configparser.ConfigParser()
config.read('config.ini')

## Settings ##
bank_location = config['Attack Options']['bank_location']
npc_location = config['Attack Options']['npc_location']
pickup_items_only_and_bank_them = config.getboolean('Attack Options', 'pickup_items_only_and_bank_them')
attack_npc = config.getboolean('Attack Options', 'attack_npc')
pickup_items = config.getboolean('Attack Options', 'pickup_items')
## Settings ##


def go_to_location(destination_name):
    destination_coordinates = search_place_coordinates(destination_name)
    destination_x, destination_y,destination_z = destination_coordinates[0], destination_coordinates[1], destination_coordinates[2]
    walk_to_destination(destination_x,destination_y,destination_z)
    return

def main():
    ## go to npc marked location ##
    print(f"Going To location {npc_location}")
    # exit(1)
    go_to_location(npc_location)

    while True:
        if keyboard.is_pressed('q'):
            exit(1)
        else:    
            inventory_full = check_if_inventory_is_full()
            if pickup_items or pickup_items_only_and_bank_them:
                if inventory_full:
                    print("We have a full loot going to Bank items")    
                    go_to_location(bank_location)
                    put_inventory_in_bank("")
                    go_to_location(npc_location)
                    print(f"We have a full inventory. Going to bank items at {bank_location}.")
                else:
                    print(f"Inventory is not full. Walking to {npc_location}")
                    go_to_location(npc_location)
                    pass
            while not inventory_full or keyboard.is_pressed("q"):
                inventory_full = check_if_inventory_is_full()
                if pickup_items_only_and_bank_them:
                    # go_to_location(bank_location)
                    # running script to pick up items only from np_location #
                    no_items_left = pickup_dropped_items()
                    print(no_items_left)
                    if no_items_left == None or no_items_left == False:
                        start_attacking_marked_npcs(pickup_items=False)
                    # attack npcs script, do not attempt to pickup loot
                    go_to_location(npc_location)
                    start_attacking_marked_npcs(pickup_items=False)
                elif attack_npc == True and pickup_items == True:
                    # attack npcs script, attempt to pickup loot
                    start_attacking_marked_npcs(pickup_items=True)
                elif attack_npc == True and pickup_items == False:
                    start_attacking_marked_npcs(pickup_items=False)    
                time.sleep(2)

if __name__ == "__main__":
    # go_to_location(npc_location)
    main()
