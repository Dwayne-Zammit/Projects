import pyautogui
import time
import os
import sys
from PIL import Image

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

def take_screenshot_all():
    # Define the coordinates of the top-left and bottom-right points
    top_left_x, top_left_y = 1, 1
    bottom_right_x, bottom_right_y = 1915, 1043
    screenshot = pyautogui.screenshot()
    crop_area = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    # Crop the screenshot using the defined area
    cropped_image = screenshot.crop(crop_area)
    screenshot_path = os.path.join(parent_directory,"screenshots/screenshot_all.png")
    cropped_image.save(screenshot_path)
    return


def get_coordinates(image_path, target_color):
    img = Image.open(image_path)
    width, height = img.size

    # Iterate over each pixel to find the target color
    for x in range(width):
        for y in range(height):
            pixel_color = img.getpixel((x, y))
            if pixel_color == target_color:
                return x, y

    # If the color is not found, return None
    return "None"

def close_bank_window():
    pyautogui.click(1061,65)
    return

def empty_inventory():
    # first_slot_x, first_slot_y = 1719, 760
    # slot_x, slot_y = first_slot_x, first_slot_y
    # for row in range(0,7):
    #     for column in range(0,4):
    #         pyautogui.click(slot_x,slot_y)
    #         time.sleep(0.5)
    #         slot_x =  slot_x + 40 
    #         print(f"Column {1}= x:{slot_x} y: {slot_y}")
    #     slot_x = first_slot_x
    #     slot_y += 35
    empty_all_button_x_y = (1020,825)
    pyautogui.click(empty_all_button_x_y)
    return


def locate_banker_x_y():
    take_screenshot_all()
    image_path = os.path.join(parent_directory,"screenshots/screenshot_all.png")
    target_color = 0,255,255
    coordinates = get_coordinates(image_path, target_color)
    coordinates = coordinates[0]+10,coordinates[1]+5
    return coordinates

def put_inventory_in_bank(location):
    print(f"Request to bank items at bank: {location}")
    
    ## click on banker
    banker_coordinates_on_screen = locate_banker_x_y()
    pyautogui.moveTo(banker_coordinates_on_screen)
    pyautogui.click(banker_coordinates_on_screen)

    ## wait until we arrived at banker ##
    time.sleep(5)
    empty_inventory()
    close_bank_window()
    return

