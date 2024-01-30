import pyautogui
import time
import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from helpers.mouse_helpers import smooth_move_to

## color rgb for run button whether enabled or disabled ##
run_button_enabled_rgb = (236, 218, 103)
run_button_disabled_rgb = (112, 113, 111)

run_button_x, run_button_y = 1730, 155

def is_running():
    option_discovered = False
    currently_running = False
    pixel_rgb = pyautogui.pixel(run_button_x, run_button_y)
    if pixel_rgb == run_button_enabled_rgb:
        return True
    else:
        return False

def press_running_button():
    smooth_move_to(run_button_x, run_button_y)
    pyautogui.click(run_button_x,run_button_y)
    ## move to middle of screen ##
    smooth_move_to(960,540)
    time.sleep(1)
    return True
