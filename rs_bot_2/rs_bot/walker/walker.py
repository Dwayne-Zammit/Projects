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
from walker.running_functions import is_running, press_running_button
from walker.check_if_changing_plane_soon import check_if_change_plane_soon
from helpers.api_request_events import get_current_run_energy
from helpers.mouse_helpers import smooth_move_to

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
        smooth_move_to(900,495)
        # pyautogui.moveTo(873,495,duration=0.6)
        pyautogui.click()
        time.sleep(1.5)
    try:
        result = requests.get(events_url)
    except:
        print("Error most probably disturbed by an interaction. Will click to somewhere to stop interaction.")    
        smooth_move_to(300,540)
        result = requests.get(events_url)
    # result = requests.get(events_url)
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


def check_if_running():
    is_player_running = is_running()
    # print(f"Player running: {is_player_running}")
    if is_player_running:
        sleep_interval = 0.3
    else:
        sleep_interval = 0.6
    return is_player_running, sleep_interval



def walk_to_destination_function(destination_x,destination_y,destination_z):
    
    current_coordinates = get_current_coordinates()
    start_x, start_y,start_z = int(current_coordinates[0]), int(current_coordinates[1]), int(current_coordinates[2])
    
    ## get path to destination
    get_coordinates_to_destination(start_x,start_y,start_z,destination_x,destination_y,destination_z)
    path_coordinates = get_list_of_path_coords()
    # print(path_coordinates)
    ## iterate through each step in the path list
    total_coordinates = len(path_coordinates)
    current_line_iteration = 1

    for next_step in path_coordinates:
        if keyboard.is_pressed("q"):
            print("Exitting since Q was Pressed")
            exit(0)
        else:
            current_coordinates = get_current_coordinates()
            current_step_x, current_step_y, current_step_z = int(current_coordinates[0]), int(current_coordinates[1]), int(current_coordinates[2])
            
            next_step = next_step.strip().split(",")
            next_step_x, next_step_y,next_step_z = int(next_step[0]), int(next_step[1]), int(next_step[2])
            # print(current_step_x,current_step_y, next_step_x, next_step_y)
            ## check aand handle any obstacles examples, doors, stairs, gates etc ##
            detect_possible_obstacles(next_step_z, current_step_z)
                # walk_to_destination(destination_x,destination_y,destination_z)

            ################# Obstacles handled so we attempt to follow path #################
            if next_step_x != current_step_x or next_step_y != current_step_y:

                ## change time interval based on running
                is_player_running, sleep_interval = check_if_running()


                ## check current run_energy ##
                current_run_energy = get_current_run_energy()
                if current_run_energy < 9999:
                    print(f"Current run enery = {current_run_energy}")
                elif current_run_energy == 10000 and is_player_running == False:
                    print("Clicking on run button")
                    press_running_button()

                ## check if we will soon arrive in order to increase sleep interval for smoother clicking ##
                total_steps_left = total_coordinates - current_line_iteration
                if total_steps_left < 5:
                    print("We are arriving soon, slowing down...")
                    if is_player_running == True:
                        sleep_interval += 1.3
                    elif is_player_running == False:
                        sleep_interval += 0.7
                # elif total_coordinates - current_line_iteration >= 5:
                #     sleep_interval = 1.2       

                ## change time interval based on whether we will change z/plane soon and whether running.
                changing_plane_soon = check_if_change_plane_soon(current_coord_z=current_step_z, path_line_iteration=current_line_iteration)
                if changing_plane_soon == True :
                    print("changing plane soon")
                    if is_player_running:
                        sleep_interval += 0.8
                    else:
                        # time.sleep(1)
                        sleep_interval += 0.4

                ## tile difference between next step and current step
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

                ## move and click on next tile
                smooth_move_to(screen_x_location,screen_y_location)
                # pyautogui.moveTo((screen_x_location,screen_y_location), duration=0.2)
                # time.sleep(0.2)
                print("still going")
                pyautogui.click(screen_x_location,screen_y_location)  
                print(difference_in_x,difference_in_y)
                ## check if we are going too fast, if yes wait a few.. ##
                if difference_in_x > -2 or difference_in_x < 2 or difference_in_y > -2 or difference_in_y < 2:
                    print("Pausing due too tile difference being greater than 2...")
                    time.sleep(sleep_interval)
                if screen_y_location < 360 or screen_y_location > 800 or screen_x_location < 670 or screen_x_location > 1250:    
                    print("Pausing due too mouse being too far from player...")
                    time.sleep(sleep_interval * 2.7)
                if difference_in_x < -7 or difference_in_x > 7 or difference_in_y < -7 or difference_in_y > 7:
                    print("Difference in tile is greater than 9, re working path")
                    # return 
                    # walk_to_destination(destination_x,destination_y,destination_z)
                    return False
                    # time.sleep(1)
            else:
                print(f"Player Already on {destination_x}, {destination_y}")
            
            print("Arrived in destination Tile...\n")
        current_line_iteration += 1
    time.sleep(3)
    return True

def walk_to_destination(destination_x,destination_y,destination_z):    
    print(f"Request to walk to destination: {destination_x},{destination_y}")
    ## run this twice to ensure that you arrive on the desired tile
    # for count in range(0,2):
        # walk_result = walk_to_destination_function(destination_x,destination_y,destination_z)
    walk_result = walk_to_destination_function(destination_x,destination_y,destination_z)
    if walk_result == False:
        walk_to_destination(destination_x,destination_y,destination_z)
    else:
        return True    
    # walk_to_destination_function(destination_x,destination_y,destination_z)    
    