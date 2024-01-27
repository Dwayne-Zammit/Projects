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

from helpers.api_request_events import get_current_health, check_npc_name
from helpers.pickup_items import pickup_dropped_items
pyautogui.FAILSAFE = False

def move_mouse_to_middle_of_screen():
    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    # Calculate the middle coordinates
    middle_x = screen_width // 2
    middle_y = screen_height // 2

    # Move the mouse to the middle of the screen
    pyautogui.moveTo(middle_x, middle_y)
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
                return x, y

    # If the color is not found, return None
    return "None"

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
    image_path = f"{parent_directory}/screenshots/screenshot_all.png"
    target_color = (0, 255, 255)
    take_screenshot_all()
    coordinates = get_coordinates(image_path, target_color)
    if coordinates != "None":
        x = coordinates[0]
        y = coordinates[1]
        pyautogui.move(x+10,y+3)
        pyautogui.click(x+20,y+10)
        pyautogui.click(x+20,y+10)
        time.sleep(1)
    else:
        print("Color not found in the image.")

def run_away():
    for count in range(0,3):
        print("Running away")
        pyautogui.click(1799,83)
        return


def start_attacking_marked_npcs(pickup_items):
    try:
        print("Attempting to find npc and start attacking")

        if int(get_current_health()) >= 13:
            move_mouse_to_middle_of_screen() 
            
            while True:
                if keyboard.is_pressed('q'):
                    print("Quitting script since q was pressed")
                    exit(1)
                attack_npc()
                npc = check_npc_name()
                
                while len(npc) > 1:
                    npc = check_npc_name()
                    print(f"we are fighting a {npc}")
                    time.sleep(3)
                    print(int(get_current_health()))
                    if int(get_current_health()) < 5:
                        print("We are running out of health")
                        run_away()
                else:
                    time.sleep(1)
                    break
        
        elif int(get_current_health()) < 13:
            print("Not attempting to fight now due to low health")
            if len(check_npc_name()) > 0:
                print("attempting to run away")
                run_away()
            time.sleep(10)

        if pickup_items:
            pickup_dropped_items()

    except Exception as e:
        print(e)
        print("error occured")