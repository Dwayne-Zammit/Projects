import pyautogui
from PIL import Image
import time
import math
from helpers.text_recognition import text_recognition
import numpy as np
import cv2

def take_screenshot_top_left():
    # Define the coordinates of the top-left and bottom-right points
    top_left_x, top_left_y = 0, 23
    bottom_right_x, bottom_right_y = 85, 40
    screenshot = pyautogui.screenshot()
    crop_area = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    # Crop the screenshot using the defined area
    cropped_image = screenshot.crop(crop_area)
    cropped_image.save('screenshot.png')
    return cropped_image.size


# while True:
time.sleep(3)
take_screenshot_top_left()
if str(text_recognition("screenshot.png")) == "Attack Cow":
    pyautogui.click(pyautogui.position())
# locate_all_items_highlighted()
