# import pyautogui
# import time
# from PIL import Image
# from npc_coords import take_screenshot_all

# image_path = ("screenshot_all.png")
# def check_white_box(image_path, box_size=20):
#     img = Image.open(image_path)

#     # Define the region of interest (top left)
#     box_region = (0, 0, box_size, box_size)

#     # Iterate over each pixel in the region
#     for x in range(box_region[0], box_region[2]):
#         for y in range(box_region[1], box_region[3]):
#             pixel_color = img.getpixel((x, y))
#             if pixel_color != (255, 255, 255):
#                 return False

#     return True

# # Example usage
# image_path = "screenshot_all.png"
# box_size = 20
# time.sleep(3)
# take_screenshot_all()
# result = check_white_box(image_path, box_size)
# if result:
#     print("White box found at the top left.")
# else:
#     print("White box not found at the top left.")

import pyautogui
from PIL import Image
import numpy as np
import cv2
import time

time.sleep(3)

def filter_purple_text(image_path):
    # Load the screenshot image
    img = Image.open(image_path)

    # Convert the image to the HSV color space
    hsv_img = img.convert("HSV")

    # Define the purple color range in HSV
    lower_purple = np.array([130, 50, 50])
    upper_purple = np.array([160, 255, 255])

    # Create a mask for the purple color range
    mask = cv2.inRange(hsv_img, lower_purple, upper_purple)

    # Apply the mask to the original image
    filtered_img = cv2.bitwise_and(img, img, mask=mask)

    # Convert the filtered image back to RGB color space
    filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_HSV2RGB)

    # Save the filtered image
    filtered_img.save("filtered_purple.png")

# Example usage

screenshot_path = "screenshot_all.png"

# Take a screenshot
pyautogui.screenshot(screenshot_path)

# Filter out purple text in the screenshot and save it
filter_purple_text(screenshot_path)

