import requests
import json
import pyautogui
import time
import easyocr



import keyboard
import os
import sys

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

from helpers.text_recognition import text_recognition
from walker.get_path_coordinates import get_coordinates_to_destination
from walker.check_for_doors import detect_for_any_gates
pyautogui.FAILSAFE = False

events_url = "http://localhost:5050/events"
coord_file_path = os.path.join(parent_directory, "walker/walker/coords.txt")
all_coords_list= []
screenshot_path = os.path.join(parent_directory,"screenshots/screenshot_cooordinates.png")



def get_current_coordinates():
    try:
        result = requests.get(events_url)
    except:
        print("Error sleeping for 5 hoping that conmnection comes up")
        time.sleep(5)
        result = requests.get(events_url)
    result_json = json.loads(result.text)
    x = str(result_json['playerObject']['playerCoordinates']['x'])
    y = str(result_json['playerObject']['playerCoordinates']['y'])
    z = str(result_json['playerObject']['playerCoordinates']['plane'])
    return x,y,z


def get_current_coordinates_from_screenshot():
    pyautogui.moveTo(942,557)
    screenshot = pyautogui.screenshot(region=(947,565, 100,40))
    screenshot.save(screenshot_path)
    reader = easyocr.Reader(['en', 'en'])
    img_text = reader.readtext(screenshot_path, detail=0)
    print(img_text)
    # image = Image.open(screenshot_path)
    # text = pytesseract.image_to_string(image)
    result = img_text[0]
    curr_x, curr_y, curr_z = result[0], result[1], result[2]
    return curr_x.strip(), curr_y.strip(), curr_z.strip()


def get_list_of_path_coords():
    with open (coord_file_path, "r") as coords_file:
        path_coords = coords_file.readlines()
        print(path_coords)
        # for step_coords in all_coords:
            # all_coords_list.append(step_coords.strip())
    return path_coords


one_tile_pixels = 32
middle_of_screen_x = 942
middle_of_screen_y = 535

def walk_to_destination_function(destination_x,destination_y,destination_z):
    time.sleep(2)
    current_coordinates = get_current_coordinates()
    start_x, start_y,start_z = int(current_coordinates[0]), int(current_coordinates[1]), int(current_coordinates[2])
    print(current_coordinates)
    print(f"destinatiion: {destination_x}, {destination_y}")
    get_coordinates_to_destination(start_x,start_y,start_z,destination_x,destination_y,destination_z)
    path_coordinates = get_list_of_path_coords()
    

    for next_step in path_coordinates:
        current_coordinates = get_current_coordinates()
        if keyboard.is_pressed("q"):
            print("exitting since Q was pressed")
            exit(0)
        next_step = next_step.strip().split(",")
        print(f"next_step is: {next_step}")
        # print(next_step)
        next_step_x, next_step_y,next_step_z = int(next_step[0]), int(next_step[1]), int(next_step[2])
        ## check for any gates ##
        print("checking for gates found")
        gates_stairs_coordinates = detect_for_any_gates()
        if gates_stairs_coordinates:
            pyautogui.moveTo(gates_stairs_coordinates)
            time.sleep(0.2)
            screenshot = pyautogui.screenshot(region=(3,25,250,50))
            screenshot.save(f"{parent_directory}/screenshots/hovered_text.png")
            text = text_recognition(f"{parent_directory}/screenshots/hovered_text.png")
            if "stair" in text.lower():
                print("Stairs detected")
                print(current_coordinates)
                # print(int(next_step[2]), int(current_coordinates[2]))
                # print(int(next_step[2]), int(current_coordinates[2]))
                print(f"next step in iteration is: {next_step[2]}")
                if next_step_z > int(current_coordinates[2]):
                    print("clicking to go up stairs")
                    pyautogui.rightClick(gates_stairs_coordinates)
                    pyautogui.moveTo(gates_stairs_coordinates[0],gates_stairs_coordinates[1]+20)
                    pyautogui.click(gates_stairs_coordinates[0],gates_stairs_coordinates[1]+20)
                    time.sleep(1)
                    pyautogui.press("1")
                    time.sleep(2)
                elif next_step_z < int(current_coordinates[2]):
                    print("clicking to go down stairs")
                    pyautogui.rightClick(gates_stairs_coordinates)
                    pyautogui.moveTo(gates_stairs_coordinates[0],gates_stairs_coordinates[1]+20)
                    pyautogui.click(gates_stairs_coordinates[0],gates_stairs_coordinates[1]+20) 
                    time.sleep(1)
                    pyautogui.press("2")
                    time.sleep(2)
                else:
                    print("Same story no need to click on stairs...")
                    time.sleep(1)
            elif "door" in text.lower() or "gate" in text.lower() or "ladder" in text.lower():
                print("Door Detected")
                pyautogui.click(gates_stairs_coordinates)
                time.sleep(2)
            # time.sleep(2)
        # if len(next_step_z) == 0:
            # next_step_z = 0
        current_coordinates = get_current_coordinates()
        x, y = int(current_coordinates[0]), int(current_coordinates[1])
        print(f"next step x is: {next_step_x}, next step y is: {next_step_y}, next_Step_z is: {next_step_z}")
        if next_step_x != x or next_step_y != y:
            # print(f"We need to move to step: {next_step_x}, {next_step_y}")
            # while x != next_step_x and y != next_step_y:
            current_coordinates = get_current_coordinates()
            x, y = int(current_coordinates[0]), int(current_coordinates[1])
            # print(f"Current Player x:{x},and y: {y}")
            difference_in_x = next_step_x - x
            # print(f"Difference in x: {difference_in_x}")
            difference_in_y = next_step_y - y
            # print(f"Difference in y: {difference_in_y}")
            # print(f"Player Current x is: {x}\nPlayer Current y is: {y}")
            if difference_in_x < 0:
                screen_x_location = middle_of_screen_x + difference_in_x * one_tile_pixels
            else:
                screen_x_location = middle_of_screen_x + difference_in_x * one_tile_pixels
            if difference_in_y > 0:
                screen_y_location = middle_of_screen_y - difference_in_y * one_tile_pixels
            else:
                screen_y_location = middle_of_screen_y -  difference_in_y * one_tile_pixels
            # print(screen_x_location,screen_y_location)
            if screen_y_location < 392 or screen_y_location > 1107 or screen_x_location < 692 or screen_x_location > 1236:
                print("We are going to fast... pausing the script for a bit...")
                
                time.sleep(0.5) 
            pyautogui.moveTo(screen_x_location,screen_y_location)
            time.sleep(0.5)
            pyautogui.click(screen_x_location,screen_y_location)  
        else:
            print("Player Already on this tile...")
    print("Arrived in destination")
    time.sleep(2)

def walk_to_destination(destination_x,destination_y,destination_z):
    for count in range(0,2):
        walk_to_destination_function(destination_x,destination_y,destination_z)
    