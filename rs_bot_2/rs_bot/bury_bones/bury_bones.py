import time
import os
import sys
import pyautogui
import numpy as np
from skimage.metrics import structural_similarity as ssim
import numpy as np

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from helpers.mouse_helpers import smooth_move_to_realistic
from helpers.runelite_gui_functions import open_inventory, close_inventory
from helpers.api_request_events import check_if_item_in_inventory

def detect_for_bones():
    bones_image_path = f'{current_directory}/images/bones.jpg'
    location = pyautogui.locateOnScreen(bones_image_path)
    if location != None:
        return (location)
    else:
        return None

def attempt_to_bury_bones():
    
    bones_coords_in_inventory = detect_for_bones()
    if bones_coords_in_inventory != None:
        
        left = bones_coords_in_inventory.left
        top = bones_coords_in_inventory.top
        width = bones_coords_in_inventory.width
        height = bones_coords_in_inventory.height

        # Calculate the center coordinates
        center_x = left + width // 2
        center_y = top + height // 2
        print("bones detected")
        smooth_move_to_realistic(center_x,center_y)
        pyautogui.click()
        time.sleep(2)
        return True
    else:
        print("No bones detected")
        return False    


def check_for_bones_in_inventory_and_bury_if_found():
    bones_id = 526
    bones_in_inventory = check_if_item_in_inventory(bones_id)
    if bones_in_inventory:
        open_inventory()
        bury_bones_result = attempt_to_bury_bones()
        while bury_bones_result == True:
            print("Bones have been burried")
            bury_bones_result = attempt_to_bury_bones()
        else:
            return "No more bones in inventory..."
    else:
        return "No bones in invetory"
    