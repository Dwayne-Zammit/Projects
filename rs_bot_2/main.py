import pyautogui
from PIL import Image
import time
import math


def take_screenshot_minimap():
    # Define the coordinates of the top-left and bottom-right points
    top_left_x, top_left_y = 1721, 23
    bottom_right_x, bottom_right_y = 1882, 201
    screenshot = pyautogui.screenshot()
    crop_area = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    # Crop the screenshot using the defined area
    cropped_image = screenshot.crop(crop_area)
    cropped_image.save('screenshot.png')
    return cropped_image.size


def get_furthest_point_path():
    top_left_x, top_left_y = 1721, 23
    cropped_image = Image.open("screenshot.png")
    width, height = cropped_image.size
    # Calculate the center coordinates
    center_x = width // 2
    center_y = height // 2
    # create the variables for furthest point detection
    max_distance = 0
    furthest_x = 0
    furthest_y = 0
    # Iterate over each pixel in the cropped image
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            r, g, b = cropped_image.getpixel((x, y))

            # Check if the pixel is red
            if r == 255 and g == 0 and b == 0:
                # Calculate the distance from the center to the current pixel
                distance = math.sqrt((center_x - x)**2 + (center_y - y)**2)

                # Check if the current pixel is further from the center than previous points
                if distance > max_distance:
                    max_distance = distance
                    furthest_x = x + top_left_x
                    furthest_y = y + top_left_y

    # Display the coordinates of the furthest point of the path
    print("Furthest point coordinates: ({}, {})".format(furthest_x, furthest_y))
    return [furthest_x, furthest_y]

def follow_path():
    take_screenshot_minimap()
    coordinates = get_furthest_point_path()
    x= coordinates[0]
    y = coordinates[1]
    pyautogui.rightClick(x, y)

while True:
    time.sleep(25)
    follow_path()