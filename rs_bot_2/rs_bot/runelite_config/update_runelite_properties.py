import pyautogui
import pyautogui
import time
import os
import sys

# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from helpers.mouse_helpers import smooth_move_to

def open_plugin(plugin_name):
    ## click on gear icon
    gear_icon_coordinates_x, gear_icon_coordinates_y = 1904,34
    smooth_move_to(gear_icon_coordinates_x,gear_icon_coordinates_y)
    pyautogui.click()
    time.sleep(0.2)
    ## click on gear icon
    configuration_icon_coordinates_x,configuration_icon_coordinates_y = 1691,50
    smooth_move_to(configuration_icon_coordinates_x,configuration_icon_coordinates_y)
    pyautogui.click()
    time.sleep(0.2)
    ## click on plugin name filter this exact location correspons to the x which will clear existing text if any
    plugin_search_clear_input_field_x, plugin_search_clear_input_field_y = 1834,90
    smooth_move_to(plugin_search_clear_input_field_x,plugin_search_clear_input_field_y)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press("backspace")
    ## input plugin name
    pyautogui.typewrite(plugin_name, interval=0.1)
    ## open plugin gear icon
    first_plugin_in_plugin_list_x, first_plugin_in_plugin_list_y = 1841,134
    smooth_move_to(first_plugin_in_plugin_list_x,first_plugin_in_plugin_list_y)
    time.sleep(0.2)
    pyautogui.click()
    return

def close_plugin_panel():
    ## click on back from plugin
    plugin_back_button_x,plugin_back_button_y = 1668,84
    smooth_move_to(plugin_back_button_x,plugin_back_button_y)
    time.sleep(0.2)
    pyautogui.click()
    ## clear filter
    plugin_search_clear_input_field_x, plugin_search_clear_input_field_y = 1864,90
    smooth_move_to(plugin_search_clear_input_field_x-20,plugin_search_clear_input_field_y)
    pyautogui.click()

    ## click on gear icon
    gear_icon_coordinates_x, gear_icon_coordinates_y = 1904,34
    smooth_move_to(gear_icon_coordinates_x,gear_icon_coordinates_y)
    pyautogui.click()
    time.sleep(0.2)
    return


def highlight_npc_on_screen(npcs_to_highlight):
    default_npcs = ["Banker", "Ellis"]
    open_plugin("npc indicator")
    npcs_to_highlight_input_field_x, npcs_to_highlight_input_field_y = 1855,464
    smooth_move_to(npcs_to_highlight_input_field_x,npcs_to_highlight_input_field_y)
    pyautogui.click()
    time.sleep(0.2)
    ## clear text
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press("backspace")
    for npc_name in default_npcs:
        pyautogui.typewrite(f"{npc_name},", interval=0.1)
    for npc_name in npcs_to_highlight:
        pyautogui.typewrite(f"{npc_name},", interval=0.1)
        
    time.sleep(0.5)
    close_plugin_panel()
    return
    

def highlight_ground_items_loot(items_to_highlight):
    open_plugin("ground items")
    items_to_highlight_input_field_x, items_to_highlight_input_field_y = 1706,167
    smooth_move_to(items_to_highlight_input_field_x,items_to_highlight_input_field_y)
    pyautogui.click()
    time.sleep(0.2)
    ## clear text
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press("backspace")   
    ## input text
    for item_name in items_to_highlight:
        pyautogui.typewrite(f"{item_name},", interval=0.1) 
    time.sleep(0.5)
    close_plugin_panel()   
    return