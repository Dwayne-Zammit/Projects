import os
import sys

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, "../../../"))
print(f"{parent_directory}")
# Add the parent directory to sys.path
# sys.path.append(f"{parent_directory}\\web_app\\")
sys.path.append(f"{parent_directory}")

from rs_bot.walker.walker import walk_to_destination
from rs_bot.walker.get_destination_coordinates import search_place_coordinates
from helpers.open_runelite_client import open_runelite_client_function


def auto_walk_to_destination(destination_name):
    destination_name_coords = search_place_coordinates(destination_place=destination_name)
    print(f"Attempting to walk to {destination_name}")
    destination_x, destination_y, destination_z = destination_name_coords[0],destination_name_coords[1],destination_name_coords[2]
    open_runelite_client_function()
    try:
        walk_to_destination(destination_x=destination_x, destination_y=destination_y, destination_z=destination_z)
    except:
        return
    return