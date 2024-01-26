import requests
import os
import sys
import orjson
import pyautogui
import time
import random

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

sys.path.append(parent_directory)
from bank_functions.bank_items import locate_banker_x_y

api_url = "http://localhost:5050/"
api_route = "bank"

bank_items = requests.get(api_url + api_route).text
bank_items = orjson.loads(bank_items)

def open_bank():
    banker_coordinates_on_screen = locate_banker_x_y()
    pyautogui.moveTo(banker_coordinates_on_screen, duration=random.uniform(0.5,1))
    pyautogui.click(banker_coordinates_on_screen)
    ## wait until we arrived at banker ##
    time.sleep(5)
    return

def close_bank():
    pyautogui.press("esc")
    time.sleep(0.5)
    return

def click_on_search_item_button_in_bank():
    bank_search_button_location = 977, 823
    pyautogui.moveTo(bank_search_button_location, duration=random.uniform(0.5,1))
    pyautogui.click(bank_search_button_location)
    time.sleep(1)
    return


def retrieve_item_from_bank(item_name, quantity):
    click_on_search_item_button_in_bank()
    first_item_in_bank_slot_location = 662, 142
    time.sleep(1)
    pyautogui.typewrite(item_name, interval=random.uniform(0.1,0.3))
    time.sleep(1)
    
    pyautogui.moveTo(first_item_in_bank_slot_location, duration=random.uniform(0.5,1))
    if quantity.lower() == "all":
        pyautogui.rightClick()
        time.sleep(0.5)
        # click on withdraw all
        pyautogui.click(630,230)
    else:
        for count in range(0,int(quantity)):
            pyautogui.click(first_item_in_bank_slot_location)
            time.sleep(0.5)

    # Close search box #
    click_on_search_item_button_in_bank()
    return

time.sleep(2)

## open bank function ##


retrieve_item_from_bank("body rune", quantity="1")
retrieve_item_from_bank("cowhide", quantity="all")
close_bank()
