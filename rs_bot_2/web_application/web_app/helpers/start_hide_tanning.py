import os
import sys
import threading

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, "../../../"))
sys.path.append(f"{parent_directory}")

from rs_bot.walker.walker import walk_to_destination
from rs_bot.walker.get_destination_coordinates import search_place_coordinates
from helpers.open_runelite_client import open_runelite_client
from rs_bot.hide_tanning.hide_tanning import start_hide_tannery


def auto_walk_to_destination(destination_name):
    open_runelite_client_result = open_runelite_client()
    # Open Runelite client in a separate thread
    runelite_thread = threading.Thread(target=open_runelite_client)
    runelite_thread.start()
    runelite_thread.join()  # Wait for the thread to finish

    # Now, check the result after the thread has finished
    try:
        start_hide_tannery()
    except:
        return "Error"
    return "Completed"
