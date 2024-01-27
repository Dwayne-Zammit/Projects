import requests
import json
import pyautogui
import time
import easyocr
import pyautogui
import keyboard
import os
import sys

pyautogui.FAILSAFE = False

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from helpers.text_recognition import text_recognition
from walker.get_path_coordinates import get_coordinates_to_destination
from walker.check_for_obstacles import detect_possible_obstacles

events_url = "http://localhost:5050/events"
coord_file_path = os.path.join(parent_directory, "walker/walker/coords.txt")
screenshot_path = os.path.join(parent_directory,"screenshots/screenshot_cooordinates.png")
all_coords_list= []

## settings variables ##
one_tile_pixels = 32
middle_of_screen_x = 942
middle_of_screen_y = 535


def get_current_coordinates():
    # result = requests.get(events_url)
    try:
        result = requests.get(events_url)
    except:
        print("Error most probably disturbed by an interaction. Will click to somewhere to stop interaction.")
        # time.sleep(5)
        
        events_api_reponded = False
        
        while not events_api_reponded:
            try:
                pyautogui.moveTo(873,495,duration=0.6)
                pyautogui.click()
                # time.sleep()
                result = requests.get(events_url)
                events_api_reponded = True
            except:
                print("Error with Api attempting to move a few steps")
                time.sleep(5)
    result_json = json.loads(result.text)
    current_step_x, current_step_y, current_step_z = str(result_json['playerObject']['playerCoordinates']['x']), str(result_json['playerObject']['playerCoordinates']['y']), str(result_json['playerObject']['playerCoordinates']['plane'])
    return current_step_x,current_step_y,current_step_z


def get_list_of_path_coords():
    with open (coord_file_path, "r") as coords_file:
        path_coords = coords_file.readlines()
        # print(path_coords)
        # for step_coords in all_coords:
            # all_coords_list.append(step_coords.strip())
    return path_coords


def walk_to_destination_function(destination_x,destination_y,destination_z):
    
    current_coordinates = get_current_coordinates()
    start_x, start_y,start_z = int(current_coordinates[0]), int(current_coordinates[1]), int(current_coordinates[2])
    
    ## get path to destination
    get_coordinates_to_destination(start_x,start_y,start_z,destination_x,destination_y,destination_z)
    path_coordinates = get_list_of_path_coords()
    # print(path_coordinates)
    ## iterate through each step in the path list
    for next_step in path_coordinates:
        if keyboard.is_pressed("q"):
            print("Exitting since Q was Pressed")
            return
        else:
            current_coordinates = get_current_coordinates()
            current_step_x, current_step_y, current_step_z = int(current_coordinates[0]), int(current_coordinates[1]), int(current_coordinates[2])

            next_step = next_step.strip().split(",")
            next_step_x, next_step_y,next_step_z = int(next_step[0]), int(next_step[1]), int(next_step[2])

            ## check aand handle any obstacles examples, doors, stairs, gates etc ##
            detect_possible_obstacles(next_step_z, current_step_z)

            ################# Obstacles handled so we attempt to follow path #################
            if next_step_x != current_step_x or next_step_y != current_step_y:
                difference_in_x = next_step_x - current_step_x
                difference_in_y = next_step_y - current_step_y
                print(f"Attempting to move to next step: {next_step_x}, {next_step_y}")

                ## work out where we should be clicking for next step x on our screen y
                if difference_in_x < 0:
                    screen_x_location = middle_of_screen_x + difference_in_x * one_tile_pixels
                else:
                    screen_x_location = middle_of_screen_x + difference_in_x * one_tile_pixels

                ## work out where we should be clicking for next step y on our screen y
                if difference_in_y > 0:
                    screen_y_location = middle_of_screen_y - difference_in_y * one_tile_pixels
                else:
                    screen_y_location = middle_of_screen_y -  difference_in_y * one_tile_pixels

                ## check if we are going too fast, if yes wait a few.. ##
                if difference_in_x > -2 or difference_in_x < 2 or difference_in_y > -2 or difference_in_y < 2:
                    # print("We are going to fast... pausing the script for a bit...")
                    time.sleep(1)
                if screen_y_location < 392 or screen_y_location > 830 or screen_x_location < 692 or screen_x_location > 1236:    
                    # print("We are going to fast... pausing the script for a bit...(off coords)")
                    time.sleep(1.5)
                
                ## move and click on next tile
                pyautogui.moveTo((screen_x_location,screen_y_location), duration=0.2)
                # time.sleep(0.2)
                pyautogui.click(screen_x_location,screen_y_location)  
            else:
                print(f"Player Already on {destination_x}, {destination_y}")
            ("Arrived in destination")
    time.sleep(2)

def walk_to_destination(destination_x,destination_y,destination_z):
    
    print(f"Request to walk to destination: {destination_x},{destination_y}")
    
    ## run this twice to ensure that you arrive on the desired tile
    for count in range(0,2):
        walk_to_destination_function(destination_x,destination_y,destination_z)
    