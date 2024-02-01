import os
import sys
import pyautogui

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)
from helpers.mouse_helpers import smooth_move_to_realistic

inventory_button_x, inventory_button_y = 1565,1010
open_inventory_button_rgb = (117, 40, 30)
magic_book_button_x, magic_book_button_y = 1665, 1010
magic_book_button_rgb = (137, 122, 101)

def open_inventory():
    rgb = pyautogui.pixel(inventory_button_x,inventory_button_y)
    if rgb != open_inventory_button_rgb:
        print("Opening inventory...")
        smooth_move_to_realistic(inventory_button_x+5,inventory_button_y+5)
        pyautogui.click()
    elif rgb == open_inventory_button_rgb:
        print("Inventory is open...")
        return True


def close_inventory():
    rgb = pyautogui.pixel(inventory_button_x,inventory_button_y)
    if rgb == open_inventory_button_rgb:
        print("Closing inventory...")
        smooth_move_to_realistic(inventory_button_x+5,inventory_button_y+5)
        pyautogui.click()
        return True
    elif rgb == open_inventory_button_rgb:
        print("Inventory is open...")
        return True

def open_magic_book():
    rgb = pyautogui.pixel(magic_book_button_x,magic_book_button_y)
    if rgb == magic_book_button_rgb:
        print("Opening inventory...")
        smooth_move_to_realistic(magic_book_button_x+5,magic_book_button_y+5)
        pyautogui.click()
    elif rgb == magic_book_button_rgb:
        print("Inventory is open...")
        return True


def close_magic_book():
    rgb = pyautogui.pixel(magic_book_button_x,magic_book_button_y)
    print(rgb)
    if rgb != magic_book_button_rgb:
        print("Closing inventory...")
        smooth_move_to_realistic(magic_book_button_x+5,magic_book_button_y+5)
        pyautogui.click()
        return True
    elif rgb == magic_book_button_rgb:
        print("Inventory is open...")
        return True
