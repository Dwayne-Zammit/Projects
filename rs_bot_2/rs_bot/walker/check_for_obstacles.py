import pyautogui
import time
import cv2
import os
import sys
import numpy as np

# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from helpers.text_recognition import text_recognition

screenshot_path = f"{parent_directory}/screenshots/detect_gates.png"

def filter_door_gate_marker_text(image_path):
    # Load the screenshot image
    img = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the purple color range in HSV
    lower_color = np.array([70, 90, 120])
    upper_color = np.array([100, 140, 150])

    # Create a mask for the purple color range
    mask = cv2.inRange(hsv_img, lower_color, upper_color)

    # Apply the mask to the original image
    filtered_img = cv2.bitwise_and(img, img, mask=mask)

    # Save the filtered image
    cv2.imwrite(f"{parent_directory}/screenshots/filtered_color_door.png", filtered_img)
    return f"{parent_directory}/screenshots/filtered_color_door.png"

# Example usage
def locate_door_box(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the purple color range in HSV
    lower_color = np.array([70, 90, 120])
    upper_color = np.array([100, 140, 150])

    # Create a mask for the purple color range
    mask = cv2.inRange(hsv_img, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours and draw bounding boxes
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Check if the object meets the size criteria
        if w > 15 and h > 40:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Adjust coordinates to match the original region
            x += 840
            y += 435
            
            # Calculate center coordinates
            center_x = x + w // 2
            center_y = y + h // 2
            print("Possible Obstacle Detected..")
            return center_x, center_y

    # Return None if no suitable object is found
    return None

def take_screenshot_hovered_tile_area():
    screenshot = pyautogui.screenshot(region=(840, 435, 200, 200))
    screenshot.save(screenshot_path)
    filtered_image_path = filter_door_gate_marker_text(screenshot_path)
    coordinates = locate_door_box(filtered_image_path)
    return coordinates

def get_possible_obstacle_name(possible_obstacle_coordinates):
    print(possible_obstacle_coordinates)
    ## hover on possible obstacle ##
    pyautogui.moveTo(possible_obstacle_coordinates,duration=0.1)
    ## take a screenhost on the hovered text 
    screenshot = pyautogui.screenshot(region=(3,25,250,50))
    screenshot.save(f"{parent_directory}/screenshots/hovered_text.png")
    ## convert image to text
    possible_obstacle_name = text_recognition(f"{parent_directory}/screenshots/hovered_text.png")
    return possible_obstacle_name.lower()

def detect_stairs(obstacle_name, next_step_z, current_step_z, possible_obstacles_coordinates):
    if "stair" in obstacle_name:
        print("Stairs detected... checking if we need to use stairs...")
        if next_step_z > current_step_z:
            print("Going up one story/plane")
            pyautogui.rightClick(possible_obstacles_coordinates)
            pyautogui.moveTo(possible_obstacles_coordinates[0],possible_obstacles_coordinates[1]+20)
            pyautogui.click(possible_obstacles_coordinates[0],possible_obstacles_coordinates[1]+20)
            time.sleep(3)
            pyautogui.press("1")
            time.sleep(1)
            return True
        
        elif next_step_z < current_step_z:
            print("Going down one story/plane")
            pyautogui.rightClick(possible_obstacles_coordinates)
            pyautogui.moveTo(possible_obstacles_coordinates[0],possible_obstacles_coordinates[1]+20)
            pyautogui.click(possible_obstacles_coordinates[0],possible_obstacles_coordinates[1]+20) 
            time.sleep(3)
            pyautogui.press("2")
            time.sleep(1)
            return True
        else:
            print("Same story no need to click on stairs...")
            return False

# check for doors or gates ##
def detect_gates_doors(obstacle_name, possible_obstacles_coordinates):       
    if "door" in obstacle_name or "gate" in obstacle_name or "ladder" in obstacle_name:
        print("Door Detected, Opening Door")
        pyautogui.click(possible_obstacles_coordinates)
        time.sleep(3.5)
        return True
    else:
        return False
    
def detect_possible_obstacles(next_step_z, current_step_z):
    possible_obstacles_coordinates = take_screenshot_hovered_tile_area()        
    if possible_obstacles_coordinates:
        possible_obstacle_name = get_possible_obstacle_name(possible_obstacles_coordinates)
        print(f"Possible obstacle name: {possible_obstacle_name}")
        detect_stairs(possible_obstacle_name, next_step_z, current_step_z, possible_obstacles_coordinates)
        detect_gates_doors(possible_obstacle_name, possible_obstacles_coordinates)
        return True
    return False