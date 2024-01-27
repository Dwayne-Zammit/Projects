# import pyautogui
# import time
# from PIL import Image

# image_path = ("screenshot_all.png")

# def take_screenshot_all():
#     # Define the coordinates of the top-left and bottom-right points
#     top_left_x, top_left_y = 1, 1
#     bottom_right_x, bottom_right_y = 1915, 1043
#     screenshot = pyautogui.screenshot()
#     crop_area = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
#     # Crop the screenshot using the defined area
#     cropped_image = screenshot.crop(crop_area)
#     cropped_image.save('screenshot_all.png')
#     return


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


# ---------------------------------------------------------#


# import pyautogui
# import time
# from PIL import Image

# image_path = ("screenshot_all.png")

# def take_screenshot_all():
#     # Define the coordinates of the top-left and bottom-right points
#     top_left_x, top_left_y = 1, 1
#     bottom_right_x, bottom_right_y = 1915, 1043
#     screenshot = pyautogui.screenshot()
#     crop_area = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
#     # Crop the screenshot using the defined area
#     cropped_image = screenshot.crop(crop_area)
#     cropped_image.save('screenshot_all.png')
#     return


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


# ---------------------------------------------------------#
import pyautogui
from PIL import Image
import numpy as np
import cv2
import time
import os
import sys

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

sys.path.append(parent_directory)

def filter_purple_text(image_path):
    # Load the screenshot image
    img = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the purple color range in HSV
    lower_purple = np.array([130, 0, 200])
    upper_purple = np.array([150, 255, 255])

    # Create a mask for the purple color range
    mask = cv2.inRange(hsv_img, lower_purple, upper_purple)

    # Apply the mask to the original image
    filtered_img = cv2.bitwise_and(img, img, mask=mask)

    # Save the filtered image
    cv2.imwrite(os.path.join(parent_directory, "screenshots/filtered_purple.png"), filtered_img)
    return
# Example usage


def locate_purple_box(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the purple color range in HSV
    lower_purple = np.array([130, 50, 50])
    upper_purple = np.array([160, 255, 255])

    # Create a mask for the purple color range
    mask = cv2.inRange(hsv_img, lower_purple, upper_purple)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours and draw bounding boxes

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return x+750,y+305,w,h
        # return x+15,y+15,w,h
    return None

def pickup_dropped_items():
    
    screenshot_path = (os.path.join(parent_directory, "screenshot_all.png"))

    # Take a screenshot
    pyautogui.screenshot(screenshot_path, region=(750,305,400,400))
    # pyautogui.screenshot(screenshot_path, region=(820,482,200,220))

    # Filter out purple text in the screenshot and save it
    filter_purple_text(screenshot_path)
    dropped_item = locate_purple_box(os.path.join(parent_directory, "screenshots/filtered_purple.png"))
    if dropped_item:
        print("Found a dropped item")
        pyautogui.moveTo(dropped_item, duration=0.3)
        pyautogui.click(dropped_item)
        print("Sleeping for 3 seconds till we pick up item...")
        time.sleep(2)
        return True
    else:
        print("No dropped item located.")
        return False    
    print("done")

# screenshot_path = "screenshot_all.png"
# filter_purple_text(screenshot_path)    