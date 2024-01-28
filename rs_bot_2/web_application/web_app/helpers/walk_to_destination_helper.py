import os
import sys
import threading

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, "../../../"))
sys.path.append(f"{parent_directory}")

from rs_bot.walker.walker import walk_to_destination
from rs_bot.walker.get_destination_coordinates import search_place_coordinates
from helpers.open_runelite_client import open_runelite_client



def auto_walk_to_destination(destination_name):
    destination_name_coords = search_place_coordinates(destination_place=destination_name)
    print(f"Attempting to walk to {destination_name}")

    print(f"Coordinates for destination: {destination_name_coords}")
    destination_x, destination_y, destination_z = destination_name_coords[0], destination_name_coords[1], destination_name_coords[2]
    open_runelite_client_result = open_runelite_client()
    # Open Runelite client in a separate thread
    runelite_thread = threading.Thread(target=open_runelite_client)
    runelite_thread.start()
    runelite_thread.join()  # Wait for the thread to finish

    # Now, check the result after the thread has finished
    try:
        print(f"in auto walk deestination {destination_x,destination_y,destination_z}")
        
        walk_to_destination(destination_x=destination_x, destination_y=destination_y, destination_z=destination_z)
    except:
        return "Q was pressed"
    return "Completed"
