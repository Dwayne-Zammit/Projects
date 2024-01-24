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


## Settings ##
bank_location = "Lumbridge Bank"
npc_location = "Cow Location"

pickup_items_only_and_bank_them = True

attack_npc = True
pickup_items = False


## Settings ##


def go_to_location(destination_name):
    destination_coordinates = search_place_coordinates(destination_name)
    destination_x, destination_y,destination_z = destination_coordinates[0], destination_coordinates[1], destination_coordinates[2]
    walk_to_destination(destination_x,destination_y,destination_z)
    return

def main():
    while True:
        while not keyboard.is_pressed('q'):
            inventory_full = check_if_inventory_is_full()
            if inventory_full:
                print("We have a full loot going to Bank items")    
                go_to_location(bank_location)
                put_inventory_in_bank("")
                go_to_location(npc_location)
            else:
                go_to_location(npc_location)
                pass
            while not inventory_full or keyboard.is_pressed("q"):
                inventory_full = check_if_inventory_is_full()
                if pickup_items_only_and_bank_them:
                    # running script to pick up items only from np_location #
                    no_items_left = pickup_dropped_items()
                    print(no_items_left)
                    if no_items_left == None or no_items_left == False:
                        start_attacking_marked_npcs(pickup_items=False)

                elif attack_npc == True and pickup_items == False:
                    # attack npcs script, do not attempt to pickup loot
                    start_attacking_marked_npcs(pickup_items=False)

                elif attack_npc == True and pickup_items == True:
                    # attack npcs script, attempt to pickup loot
                    start_attacking_marked_npcs(pickup_items=True)
                    

                time.sleep(2)

if __name__ == "__main__":
    main()
