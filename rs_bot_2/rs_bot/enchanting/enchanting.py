import os
import sys
import pyautogui
import time
import random


current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from bank_functions.bank_functions import deposit_all_items_to_bank, retrieve_item_from_bank, open_bank, close_bank
from walker.walker import walk_to_destination
from walker.get_destination_coordinates import search_place_coordinates
from helpers.runelite_gui_functions import open_inventory, open_magic_book, close_inventory, close_magic_book
from helpers.mouse_helpers import smooth_move_to_realistic
from helpers.api_request_events import check_if_inventory_is_full, check_if_item_in_inventory, item_quantity_in_bank
from items.load_items import get_item_id


ring_name = "Emerald Ring"
runes = "Cosmic Rune"
cast_2_level_enchant_x, cast_2_level_enchant_y = 1761, 796


def go_to_location(bank_name):
    destination_coordinates = search_place_coordinates(bank_name)
    destination_x, destination_y,destination_z = destination_coordinates[0], destination_coordinates[1], destination_coordinates[2]
    walk_to_destination(destination_x,destination_y,destination_z)
    return


def detect_for_ring_in_inventory(ring_name):
    bones_image_path = f'{current_directory}/images/{ring_name}.jpg'
    location = pyautogui.locateOnScreen(bones_image_path)
    if location != None:
        return (location)
    else:
        return None
    


def enchant_main_function(ring_name):
    ## check if ring in bank
    ring_id = get_item_id([ring_name])
    runes_id = get_item_id([runes])
    ring_in_bank = item_quantity_in_bank(ring_name)
    runes_in_bank = item_quantity_in_bank(runes)
    runes_in_inventory = check_if_item_in_inventory(ring_id)
    ## break script if no rings
    if ring_in_bank < 2:
        print("You must own the ring in your bank")
        exit(1)
    ## break script if no runes in bank or in inventory
    if not runes_in_bank and not runes_in_inventory:
        print("You must own the runes in your bank or inventory")
        exit(1)
    go_to_location("Al Kharid Bank")
    while ring_in_inventory:
        ring_in_inventory = check_if_item_in_inventory(ring_id)
        ## go to bank location
        ## retrieve items from bank
        open_bank()
        time.sleep(random.uniform(0.3,1))
        inventory_full = check_if_inventory_is_full()
        if inventory_full:
            deposit_all_items_to_bank()
        retrieve_item_from_bank(runes, quantity="all")
        retrieve_item_from_bank(ring_name, quantity="all")
        close_bank()
        time.sleep(random.uniform(0.3,1))
        ## open magic book
        open_magic_book()
        time.sleep(random.uniform(0.2,0.6))
        ## click on cast level 2 enchant
        smooth_move_to_realistic(cast_2_level_enchant_x, cast_2_level_enchant_y)
        pyautogui.click()
        time.sleep(random.uniform(0.2,0.6))
        ## locate ring in inventory
        while not inventory_full:
            ring_coords_in_inventory = detect_for_ring_in_inventory(ring_name)
            if ring_coords_in_inventory != None:

                left = ring_coords_in_inventory.left
                top = ring_coords_in_inventory.top
                width = ring_coords_in_inventory.width
                height = ring_coords_in_inventory.height

                # Calculate the center coordinates
                center_x = left + width // 2
                center_y = top + height // 2
                print("ring detected")
                smooth_move_to_realistic(center_x,center_y)
                time.sleep(random.uniform(0.3,1))
                pyautogui.click()
                time.sleep(random.uniform(0.8,3.5))
                ## click on cast level 2 enchant
                smooth_move_to_realistic(cast_2_level_enchant_x, cast_2_level_enchant_y)
                pyautogui.click()
                time.sleep(random.uniform(0.2,0.6))
                return True
            else:
                print("No ring detected")
                return False
            

enchant_main_function()            