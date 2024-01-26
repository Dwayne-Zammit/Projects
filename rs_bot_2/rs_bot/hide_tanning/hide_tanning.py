import pyautogui
import time
import os
import sys
from PIL import Image
import random

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)


from walker.walker import walk_to_destination
from walker.get_destination_coordinates import search_place_coordinates
from bank_functions.bank_functions import open_bank,close_bank, click_on_search_item_button_in_bank, retrieve_item_from_bank,deposit_all_items_to_bank

def go_to_location(destination_name):
    destination_coordinates = search_place_coordinates(destination_name)
    destination_x, destination_y,destination_z = destination_coordinates[0], destination_coordinates[1], destination_coordinates[2]
    walk_to_destination(destination_x,destination_y,destination_z)
    return  

tanning_options_coords = {"LEATHER": (690,390), "HARD_LEATHER":(786,390), "snakeskin light green":(890,390),"snakeskin dark green": (1005,390)}


def main():
    ## settings ##
    hide = "Cowhide"
    tanned_hide = "HARD_LEATHER"
    bank_location = "Lumbridge Bank" 
    tannery_location = "Al Kharid Tanning"

    while True:
        # ## Go To Bank and withdraw hide
        go_to_location(bank_location)
        try:
           open_bank()
        except:
           time.sleep(3)
           go_to_location(bank_location)    
        deposit_all_items_to_bank()
        retrieve_item_from_bank("coins","100")
        retrieve_item_from_bank(hide, quantity="all")
        close_bank()

        ## go to tanning location
        go_to_location(tannery_location)

        ## click on tannery_npc ##
        try:
            click_tannery_npc = open_bank()
        except:
            time.sleep(3)
            go_to_location(tannery_location)    
        ## click on the tanned hide we want to tan to ##
        pyautogui.moveTo(tanning_options_coords[tanned_hide],duration=random.uniform(0.5,1))
        tanned_leather_option_on_menu_x, tanned_leather_option_on_menu_y = tanning_options_coords[tanned_hide][0], tanning_options_coords[tanned_hide][1]
        pyautogui.rightClick(tanned_leather_option_on_menu_x, tanned_leather_option_on_menu_y)
        ## click on tan all ##
        tan_all_button_location = tanned_leather_option_on_menu_x, tanned_leather_option_on_menu_y + 70
        pyautogui.moveTo(tan_all_button_location, duration=random.uniform(0.5,1))
        pyautogui.click(tan_all_button_location)
        
        ## go back to bank and deposit all loot to bank ##
        go_to_location(bank_location)
        try:
           open_bank()
        except:
           time.sleep(3)
           go_to_location(bank_location)
        deposit_all_items_to_bank()

main()