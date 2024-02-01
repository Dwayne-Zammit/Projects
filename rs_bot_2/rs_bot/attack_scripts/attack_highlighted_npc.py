from PIL import Image
import pyautogui
import time
import keyboard
import os
import sys

# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from helpers.api_request_events import get_current_health, check_npc_name, check_npc_health, get_max_health
from helpers.pickup_items import pickup_dropped_items
from helpers.mouse_helpers import smooth_move_to
from bury_bones.bury_bones import check_for_bones_in_inventory_and_bury_if_found
pyautogui.FAILSAFE = False

def move_mouse_to_middle_of_screen():
    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    # Calculate the middle coordinates
    middle_x = screen_width // 2
    middle_y = screen_height // 2

    # Move the mouse to the middle of the screen
    pyautogui.moveTo((middle_x, middle_y), duration=0.3)
    return


def take_screenshot_all():
    # Define the coordinates of the top-left and bottom-right points
    top_left_x, top_left_y = 1, 1
    bottom_right_x, bottom_right_y = 1915, 1043
    screenshot = pyautogui.screenshot()
    crop_area = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    # Crop the screenshot using the defined area
    cropped_image = screenshot.crop(crop_area)
    cropped_image.save(f"{parent_directory}/screenshots/screenshot_all.png")
    return


def get_coordinates(image_path, target_color):
    img = Image.open(image_path)
    width, height = img.size

    # Iterate over each pixel to find the target color
    for x in range(width):
        for y in range(height):
            pixel_color = img.getpixel((x, y))
            if pixel_color == target_color:
                # Check if there are at least 5x5 pixels around the target pixel
                if check_surrounding_pixels(img, x, y, target_color, size=10):
                    # Return the middle pixel's coordinates
                    return x, y

    # If the color is not found or 5x5 square is not found, return None
    return None

def check_surrounding_pixels(img, x, y, target_color, size):
    # Calculate the boundaries for the 5x5 square
    left_bound = max(0, x - size // 2)
    upper_bound = max(0, y - size // 2)
    right_bound = min(img.width, x + size // 2)
    lower_bound = min(img.height, y + size // 2)

    # Iterate over the square region
    for i in range(left_bound, right_bound):
        for j in range(upper_bound, lower_bound):
            # Check if the pixel color matches the target color
            if img.getpixel((i, j)) != target_color:
                return False
    return True

def get_coordinates_of_closest_marked_npc(image_path, target_color):
    img = Image.open(image_path)
    width, height = img.size

    # Calculate the center of the image
    center_x, center_y = width // 2, height // 2

    # Initialize variables to store the closest coordinates and distance
    closest_coords = None
    closest_distance = float('inf')  # Initialize with a large value

    # Iterate over each pixel to find the target color
    for x in range(width):
        for y in range(height):
            pixel_color = img.getpixel((x, y))
            if pixel_color == target_color:
                # Calculate the distance to the center
                distance_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5

                # Update closest coordinates if the current pixel is closer to the center
                if distance_to_center < closest_distance:
                    closest_coords = x, y
                    closest_distance = distance_to_center

    # If the color is not found, return None
    if closest_coords is not None:
        return closest_coords
    else:
        return None

def attack_npc():
    # Example usage
    # for count in range(0,2):
    image_path = f"{parent_directory}/screenshots/screenshot_all.png"
    target_color = (0, 255, 255)
    take_screenshot_all()
    coordinates = get_coordinates(image_path, target_color)
    if coordinates != "None":
        x = coordinates[0]
        y = coordinates[1]
        pyautogui.moveTo((x,y), duration=0.1)
        pyautogui.click()
        # pyautogui.move(x+10,y+3)
    else:
        print("Color not found in the image.")
        return
    
    # pyautogui.click(x+10,y+10)
    time.sleep(3)


def run_away():
    for count in range(0,3):
        print("Running away")
        smooth_move_to(1799,83)
        pyautogui.click(1799,83)
        return


def start_attacking_marked_npcs(pickup_items):
    try:
        print("Attempting to find npc and start attacking")
        max_health = get_max_health()
        health_to_start_attacking = max_health * 20 / 100
        if health_to_start_attacking < 4:
            health_to_start_attacking = 4
        health_to_stop_attacking = max_health *  10 / 100
        if health_to_stop_attacking < 4:
            health_to_stop_attacking = 3
        if int(get_current_health()) >= int(health_to_start_attacking):
            # move_mouse_to_middle_of_screen() 
            
            while True:
                if keyboard.is_pressed('q'):
                    print("Quitting script since q was pressed")
                    exit(1)
                attack_npc()
                npc = check_npc_name()
                
                while len(npc) > 1:
                    if keyboard.is_pressed("q"):
                        exit(0)
                    npc = check_npc_name()
                    print(f"We are fighting a {npc}")
                    time.sleep(0.5)
                    print(f"Current Health: {get_current_health()}")
                    print(f"NPC's Health: {check_npc_health()}\n")
                    if int(get_current_health()) < 2:
                        print("We are running out of health")
                        run_away()
                else:
                    time.sleep(1)
                    check_for_bones_in_inventory_and_bury_if_found()
                    break
        
        elif int(get_current_health()) < int(health_to_stop_attacking):
            print("Not attempting to fight now due to low health...")
            if len(check_npc_name()) > 0:
                print("Possibility of dying, attempting to run away...")
                run_away()
            time.sleep(10)

        if pickup_items:
            pickup_dropped_items()
        print("\n")
    except Exception as e:
        print(e)
        print("No Marked NPC on screem")