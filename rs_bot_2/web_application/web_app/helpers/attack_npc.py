import os
import sys
import threading
import configparser

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, "../../../"))
sys.path.append(f"{parent_directory}")

from rs_bot.walker.walker import walk_to_destination
from rs_bot.walker.get_destination_coordinates import search_place_coordinates
from rs_bot.attack_scripts.attack_npc_or_pickup_items_and_bank_them import start_attacking_npcs
from rs_bot.runelite_config.update_runelite_properties import highlight_npc_on_screen, highlight_ground_items_loot
from helpers.open_runelite_client import open_runelite_client

config_file = os.path.join(f"{parent_directory}/rs_bot/attack_scripts/config.ini")
print(config_file)
def attack_npc(bank_location, npc_location, pickups_items_only_and_bank_them, attack_npc, pickup_items,dropped_item_name, bank_items, npc_name):

    # Load the config file
    config = configparser.ConfigParser()
    config.read(config_file) 
    print(npc_name)  
    # Update the variables
    print(bank_location)
    config['Attack Options']['bank_location'] = bank_location
    config['Attack Options']['npc_location'] = npc_location
    config['Attack Options']['pickup_items_only_and_bank_them'] = pickups_items_only_and_bank_them
    config['Attack Options']['attack_npc'] = attack_npc
    if attack_npc == None:
        config['Attack Options']['attack_npc'] = "False"
    else:
        config['Attack Options']['attack_npc'] = "True"        
    if pickup_items == None:
        config['Attack Options']['pickup_items'] = "False"
    else:
        config['Attack Options']['pickup_items'] = "True"
    if bank_items == None:
        config['Attack Options']['bank_items'] = "False"
    else:
        config['Attack Options']['bank_items'] = "True"    
    
    config['Attack Options']['npc_name'] = npc_name
    config['Attack Options']['dropped_item_name'] = dropped_item_name

    # Save the updated config file
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    # destination_name_coords = search_place_coordinates(destination_place=destination_name)
    # print(f"Attempting to walk to {destination_name}")

    # print(f"Coordinates for destination: {destination_name_coords}")
    # destination_x, destination_y, destination_z = destination_name_coords[0], destination_name_coords[1], destination_name_coords[2]
    open_runelite_client_result = open_runelite_client()
    # Open Runelite client in a separate thread
    runelite_thread = threading.Thread(target=open_runelite_client)
    runelite_thread.start()
    runelite_thread.join()  # Wait for the thread to finish
    ## in runelite update the plugin to display guards npcs
    highlight_npc_on_screen([npc_name])
    highlight_ground_items_loot([dropped_item_name])
    # Now, check the result after the thread has finished
    try:
        ## start attcaking npcs ##
        start_attacking_npcs()
    except:
        return "Error"
    return "Completed"