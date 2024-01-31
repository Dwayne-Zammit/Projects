import time
import pygetwindow as gw
import threading
# from pywinauto import find_windows
# from pywinauto.win32functions import SetFocus
import win32gui
import pyautogui
from pywinauto import Application
import configparser
import sys
import os

# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)
sys.path.append(current_directory)
parent_directory = os.path.abspath(os.path.join(current_directory, "../../../"))
APP_CONFIG = f"{parent_directory}/rs_bot/app-config.ini"
print(APP_CONFIG)
config = configparser.ConfigParser()
print(current_directory)
config.read(APP_CONFIG)
## Settings ##
# print(config[0])
bank_location = config['credentials']['username']


def open_runelite_client_function():
    try:
        window_title = "RuneLite - Dukadelmin"
        max_attempts = 1
        delay_between_attempts = 2  # seconds

        for attempt in range(1, max_attempts + 1):
            print(f"Attempt {attempt}: Checking for window '{window_title}'")
            windows = gw.getWindowsWithTitle(window_title)
            if windows:

                window = windows[0]
                print(window)
                if not window.isActive:
                    window.activate()
                    # window.set_focus()
                    window.maximize()
                    print(f"Attempt {attempt}: Window '{window_title}' maximized and activated.")
                    break  # Break out of the loop if successful
                else:
                    print(f"Attempt {attempt}: Window '{window_title}' is already active.")
                    break  # Break out of the loop if the window is already active
            else:
                print(f"{window_title} not found, ensure that RuneLite is started.")
                return f"{window_title} not found, ensure that RuneLite is started."
        

        return "Window operation completed successfully."
    
    except Exception as e:
        pyautogui.hotkey('winleft', 'm')
        # for count in range(0,2):
        pyautogui.hotkey('alt', 'tab')
        print(f"Error: {e}")
        return f"Error: {e}"
    
def open_runelite_client():
    # open_runelite_client_function()
    result = open_runelite_client_function()
    # result = open_runelite_client_function()
    # runelite_thread = threading.Thread(target=open_runelite_client_function)
    # result = runelite_thread.start()
    if result != "Window operation completed successfully.":
        return result
