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
sys.path.append(current_directory)

from bank_items import locate_banker_x_y
from helpers.api_request_events import check_if_bank_is_open
from helpers.mouse_helpers import smooth_move_to

api_url = "http://localhost:5050/"
api_route = "bank"

bank_items = requests.get(api_url + api_route).text
bank_items = orjson.loads(bank_items)


def open_bank():
    bank_open = False
    ## attemppt to locate banker and open bank ##
    banker_coordinates_on_screen = locate_banker_x_y()
    banker_coordinates_on_screen_x, banker_coordinates_on_screen_y = banker_coordinates_on_screen[0], banker_coordinates_on_screen[1]
    smooth_move_to(banker_coordinates_on_screen_x, banker_coordinates_on_screen_y)
    time.sleep(0.5)
    pyautogui.click(banker_coordinates_on_screen)
    time.sleep(5)
    print("Bank is now open, procceeding...")

    ## check if bank is open, if not click reattempt to open bank ##
    # while not bank_open:
    #     bank_open = check_if_bank_is_open()
    #     banker_coordinates_on_screen = locate_banker_x_y()
    #     pyautogui.moveTo(banker_coordinates_on_screen,duration=0.3)
    #     pyautogui.click(banker_coordinates_on_screen)
    #     ## wait until we arrived at banker ##
    #     bank_open = check_if_bank_is_open()
    #     time.sleep(3)
    # if bank_open == True:
    #    print("Bank is now open, procceeding...")
    return


def close_bank():
    bank_open = True
    time.sleep(0.6)
    ## attemmpt to close bank ##
    pyautogui.press("esc")
    time.sleep(0.6)
    # bank_open = True
    # while bank_open:
    #     bank_open = check_if_bank_is_open()
    #     pyautogui.press("esc")
    #     time.sleep(1)
    # if bank_open == False:
    #     print("Bank is now closed, proceeding.")
    return

def click_on_search_item_button_in_bank():
    bank_search_button_location_x, bank_search_button_location_y = 977, 823
    smooth_move_to(bank_search_button_location_x, bank_search_button_location_y)
    pyautogui.click(bank_search_button_location_x,bank_search_button_location_y)
    time.sleep(0.8)
    return


def retrieve_item_from_bank(item_name, quantity):
    click_on_search_item_button_in_bank()
    first_item_in_bank_slot_location = 662, 142
    pyautogui.typewrite(item_name, interval=0.1)
    time.sleep(0.2)
    smooth_move_to(first_item_in_bank_slot_location[0], first_item_in_bank_slot_location[1])
    time.sleep(1)
    # pyautogui.moveTo(first_item_in_bank_slot_location, duration=random.uniform(0.6,1))
    if quantity.lower() == "all":
        
        withdraw_all_coordinates = 630,245
        pyautogui.rightClick()
        time.sleep(0.6)
        # click on withdraw all
        smooth_move_to(withdraw_all_coordinates[0],withdraw_all_coordinates[1])
        pyautogui.click(withdraw_all_coordinates)
        time.sleep(0.6)
    elif int(quantity) < 5:
        for count in range(0,int(quantity)):
            pyautogui.click(first_item_in_bank_slot_location)
            time.sleep(0.6)
    else:
        pyautogui.rightClick()
        time.sleep(1)
        withdraw_x_coordinates = 634,229
        smooth_move_to(withdraw_x_coordinates[0], withdraw_x_coordinates[1])
        time.sleep(1)
        pyautogui.click(withdraw_x_coordinates)
        pyautogui.typewrite(str(quantity), interval=random.uniform(0.1,2))
        time.sleep(1)
        pyautogui.press("enter")

    # Close search box #
    click_on_search_item_button_in_bank()
    return


def deposit_all_items_to_bank():
    empty_all_button_x_y = (1020,825)
    smooth_move_to(empty_all_button_x_y[0],empty_all_button_x_y[1])
    # time.sleep(1)
    pyautogui.click(empty_all_button_x_y)
    time.sleep(0.6)
    return

