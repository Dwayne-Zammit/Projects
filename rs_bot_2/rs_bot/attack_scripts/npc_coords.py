from PIL import Image
import pyautogui
import time
import keyboard
import os
import sys

from helpers.api_request_events import get_current_health, check_npc_name

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

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
    cropped_image.save(os.path.join(parent_directory,'screenshot_all.png'))
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

def attack_npc():
    # Example usage
    image_path = os.path.join(parent_directory,"screenshot_all.png")
    target_color = (0, 255, 255)
    time.sleep(7)
    take_screenshot_all()
    coordinates = get_coordinates(image_path, target_color)
    if coordinates != "None":
        x = coordinates[0]
        y = coordinates[1]
        pyautogui.move(x+10,y+3)
        pyautogui.rightClick(x+10,y+5)
        pyautogui.rightClick(x+10,y+5)
    else:
        print("Color not found in the image.")

def run_away():
    print("Running away")
    pyautogui.rightClick(1799,83)
    return


while True:
    if keyboard.is_pressed('q'):
        print("Quitting script since q was pressed")
        exit(1)
    pyautogui.FAILSAFE = False
    try:
        move_mouse_to_middle_of_screen()
        print("Attempting to find npc and start attacking")
        if int(get_current_health()) >= 13:
            attack_npc()
            while True:
                if keyboard.is_pressed('q'):
                    print("Quitting script since q was pressed")
                    exit(1)
                npc = check_npc_name()
                if len(npc) > 1:
                    print(f"we are fighting a {npc}")
                    time.sleep(1)
                    print(int(get_current_health()))
                    if int(get_current_health()) < 5:
                        print("We are running out of health")
                        run_away()
                else:
                    break
        elif int(get_current_health()) < 13:
            print("Not attempting to fight now due to low health")
            for number in range(0,5):
                if len(check_npc_name) > 0:
                    run_away()
            time.sleep(10)
    except Exception as e:
        print(e)
        print("error occured")
