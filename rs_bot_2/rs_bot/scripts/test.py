# import requests
# import os
# import sys
# import orjson
# import pyautogui
# import time
# import random

# current_directory = os.path.dirname(os.path.realpath(__file__))
# parent_directory = os.path.dirname(current_directory)

# sys.path.append(parent_directory)
# from bank_functions.bank_items import locate_banker_x_y

# api_url = "http://localhost:5050/"
# api_route = "bank"

# bank_items = requests.get(api_url + api_route).text
# bank_items = orjson.loads(bank_items)

# def open_bank():
#     banker_coordinates_on_screen = locate_banker_x_y()
#     pyautogui.moveTo(banker_coordinates_on_screen, duration=random.uniform(0.5,1))
#     pyautogui.click(banker_coordinates_on_screen)
#     ## wait until we arrived at banker ##
#     time.sleep(5)
#     return

# def close_bank():
#     pyautogui.press("esc")
#     time.sleep(0.5)
#     return

# def click_on_search_item_button_in_bank():
#     bank_search_button_location = 977, 823
#     pyautogui.moveTo(bank_search_button_location, duration=random.uniform(0.5,1))
#     pyautogui.click(bank_search_button_location)
#     time.sleep(1)
#     return


# def retrieve_item_from_bank(item_name, quantity):
#     click_on_search_item_button_in_bank()
#     first_item_in_bank_slot_location = 662, 142
#     time.sleep(1)
#     pyautogui.typewrite(item_name, interval=random.uniform(0.1,0.3))
#     time.sleep(1)
    
#     pyautogui.moveTo(first_item_in_bank_slot_location, duration=random.uniform(0.5,1))
#     if quantity.lower() == "all":
#         pyautogui.rightClick()
#         time.sleep(0.5)
#         # click on withdraw all
#         pyautogui.click(630,230)
#     else:
#         for count in range(0,int(quantity)):
#             pyautogui.click(first_item_in_bank_slot_location)
#             time.sleep(0.5)

#     # Close search box #
#     click_on_search_item_button_in_bank()
#     return

# time.sleep(2)

# ## open bank function ##


# retrieve_item_from_bank("body rune", quantity="1")
# retrieve_item_from_bank("cowhide", quantity="all")
# close_bank()
import win32gui

# Function to get the window location and size
def get_window_rect(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("Window not found.")
        return None

    rect = win32gui.GetWindowRect(hwnd)
    x, y, w, h = rect

    print("Window Title:", window_title)
    print("Location: ({}, {})".format(x, y))
    print("Size: {}x{}".format(w - x, h - y))
    
    return x, y, w, h

# if __name__ == "__main__":
#     # Define the item coordinates of the large window and the item in the full screen
#     full_screen_coords = (935, 323)  # Assuming this is the item's position in the full-screen context

#     # Get the current window's location and size
#     window_title = "RuneLite - Dukadelmin"
#     window_x, window_y, window_w, window_h = get_window_rect(window_title)

#     # Calculate the ratio of the full screen size to the current window size
#     ratio_x = window_w / 941  # Current window width
#     ratio_y = window_h / 432   # Current window height

#     # Adjust the item's coordinates to fit the current window
#     adjusted_x = window_x + (full_screen_coords[0] - 940) * ratio_x
#     adjusted_y = window_y + (full_screen_coords[1] - 174) * ratio_y  + 40

#     # Since the desired coordinates are very close, we can round them to integers
#     adjusted_x = round(adjusted_x)
#     adjusted_y = round(adjusted_y)

#     print("Adjusted Coordinates for Small Window: ({}, {})".format(int(adjusted_x), int(adjusted_y)))

# Function to calculate the coordinates of the point within the window
def transform_x_to_window(x_full_screen, window_width, window_x):
    x_window_context = x_full_screen * window_x / window_width
    return x_window_context

# Example usage
if __name__ == "__main__":
    # Full screen width
    full_screen_width = 1920

    # Window width and location
    window_width = 1026
    window_x = 629

    # Original x-coordinate in the full screen
    x_full_screen = 941

    # Transform the x-coordinate to the window context
    x_window_context = transform_x_to_window(x_full_screen, window_width, window_x)
    x_window_context /= 2
    print("Transformed x-coordinate in the window context:", int(x_window_context))
