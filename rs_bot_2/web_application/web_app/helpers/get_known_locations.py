import os

# Get the parent directory of the file
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, "../../../"))
print(parent_directory)
# Construct a new path based on the parent directory
known_places_file = os.path.join(parent_directory, "rs_bot/walker/walker/known_places.json")

print("Parent Directory:", parent_directory)
print("New Path:", known_places_file)
import json


def known_places():
    with open(known_places_file, "r") as known_places:
        known_places = known_places.read()
        
    return json.loads(known_places)['locations']
