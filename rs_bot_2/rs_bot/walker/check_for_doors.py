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
            print("Door/Stairs Detected")
            return center_x, center_y

    # Return None if no suitable object is found
    return None

def detect_for_any_gates():
    screenshot = pyautogui.screenshot(region=(840, 435, 200, 200))
    screenshot.save(screenshot_path)
    filtered_image_path = filter_door_gate_marker_text(screenshot_path)
    coordinates = locate_door_box(filtered_image_path)
    return coordinates

