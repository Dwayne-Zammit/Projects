import pyautogui
import time
import os
import sys
from PIL import Image
import random
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import keyboard

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)


from walker.walker import walk_to_destination
from walker.get_destination_coordinates import search_place_coordinates
from bank_functions.bank_functions import open_bank,close_bank, check_if_bank_is_open, retrieve_item_from_bank,deposit_all_items_to_bank
from helpers.mouse_helpers import smooth_move_to 


## settings ##
hide = "Cowhide"
tanned_hide = "HARD_LEATHER"
bank_location = "Al Kharid Bank"
tannery_location = "Al Kharid Tannery"
toll_gate = False


def go_to_location(destination_name):
    destination_coordinates = search_place_coordinates(destination_name)
    destination_x, destination_y,destination_z = destination_coordinates[0], destination_coordinates[1], destination_coordinates[2]
    walk_to_destination(destination_x,destination_y,destination_z)
    return  

tanning_options_coords = {"LEATHER": (690,390), "HARD_LEATHER":(786,390), "snakeskin light green":(890,390),"snakeskin dark green": (1005,390)}

def take_screenshot(filename):
    # Take a screenshot and save it to the specified filename
    screenshot = pyautogui.screenshot(region=(597,305,490,300))
    screenshot.save(filename)


def ensure_tanery_menu_is_open(tenary_location):
    smooth_move_to(960,540)
    take_screenshot(f"{parent_directory}/hide_tanning/images/locate_tanery_attempt.png")

    # Compare the screenshot with another image
    similarity = compare_images(f"{parent_directory}/hide_tanning/images/locate_tanery_attempt.png", f"{parent_directory}/hide_tanning/images/tannery_menu.PNG")
    print(f"This is the similarity: {similarity}")
    if similarity:
        print("Screenshots are similar!")
    else:
        go_to_location(tenary_location)
        talk_to_guard = open_bank()
        ensure_tanery_menu_is_open(tenary_location)
    return

def pay_gate_toll():
    ## press click here to continue twice ##
    click_here_to_continue_x_y = 265,985
    for count in range(0,2):
        pyautogui.moveTo(click_here_to_continue_x_y,duration=1)
        pyautogui.click(click_here_to_continue_x_y)
        time.sleep(1)
    ## click on yes okay ##
    confirm_payment_button_x_y = 261, 927
    pyautogui.moveTo(confirm_payment_button_x_y)
    pyautogui.click(confirm_payment_button_x_y)
    time.sleep(1)
    ## confirm selection
    pyautogui.click(click_here_to_continue_x_y)
    time.sleep(2)
    return        

def compare_images(image1_path, image2_path, threshold=0.5):
    # Open and load the images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # Convert images to grayscale
    img1_gray = img1.convert('L')
    img2_gray = img2.convert('L')

    # Resize the images to the same dimensions
    width = min(img1_gray.width, img2_gray.width)
    height = min(img1_gray.height, img2_gray.height)
    img1_gray = img1_gray.resize((width, height))
    img2_gray = img2_gray.resize((width, height))

    # Convert images to NumPy arrays
    img1_array = np.array(img1_gray)
    img2_array = np.array(img2_gray)

    # Compute the Structural Similarity Index (SSIM)
    similarity_index = ssim(img1_array, img2_array)

    # Return True if similarity index is greater than threshold, False otherwise
    return similarity_index > threshold


def go_to_bank_and_get_cowhide():
    go_to_location(bank_location)
    try:
       open_bank()
    except:
       time.sleep(3)
       go_to_location(bank_location)
       open_bank()
    time.sleep(1)   
    while check_if_bank_is_open() == False:   
        go_to_location(bank_location)
        open_bank()
        
    deposit_all_items_to_bank()
    retrieve_item_from_bank("coins",quantity="all")
    retrieve_item_from_bank(hide, quantity="all")
    close_bank()
    return

def start_hide_tannery():
    go_to_bank_and_get_cowhide()
    while not keyboard.is_pressed("q"):
        # go to tanning location
        # if tannery_location == "Al Kharid Tanning":
        #     if toll_gate:
        #         bank_location = "Al Kharid Bank"
        #         go_to_location("Toll Gate West Side")
        #         talk_to_guard = open_bank()
        #         pay_gate_toll()
        #         go_to_location("Al Kharid Tanning")
        #     else:
        #         go_to_location(tannery_location)
        go_to_location(tannery_location)
        ## Wait a few till we arrive ##
        time.sleep(1)
        ## click on tannery_npc ##
        click_tannery_npc = open_bank()
        ensure_tanery_menu_is_open(tannery_location)

        ## click on the tanned hide we want to tan to ##
        tanned_leather_option_on_menu_x, tanned_leather_option_on_menu_y = tanning_options_coords[tanned_hide][0], tanning_options_coords[tanned_hide][1]
        smooth_move_to(tanned_leather_option_on_menu_x, tanned_leather_option_on_menu_y)
        pyautogui.rightClick(tanned_leather_option_on_menu_x, tanned_leather_option_on_menu_y)
        time.sleep(0.6)

        ## click on tan all ##
        tan_all_button_location = tanned_leather_option_on_menu_x, tanned_leather_option_on_menu_y + 70
        smooth_move_to(tanned_leather_option_on_menu_x,tanned_leather_option_on_menu_y + 70)
        time.sleep(0.3)
        pyautogui.click(tan_all_button_location)
        time.sleep(0.3)
        
        ## close tannery menu ##
        pyautogui.press("esc")
        
        ## go back to bank and deposit all loot to bank ##
        if tannery_location == "Al Kharid Tannery":
            if toll_gate:
                bank_location = "Al Kharid Bank"
                go_to_location("Toll Gate East Side")
                pay_gate_toll()
                go_to_location(bank_location)
            else:
                bank_location = "Al Kharid Bank"
                go_to_location(bank_location)   
        try:
           
           open_bank()
        except:
           time.sleep(3)
           go_to_location(bank_location)
           open_bank()
        time.sleep(2)
        deposit_all_items_to_bank()
        retrieve_item_from_bank("coins",quantity="all")
        retrieve_item_from_bank(hide, quantity="all")
        close_bank()
        