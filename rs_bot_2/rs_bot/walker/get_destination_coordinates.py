import os
import json

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

known_places_json_file = os.path.join(parent_directory, "walker/walker/known_places.json")
print(known_places_json_file)
def search_place_coordinates(destination_place):
    print(f"destination place in search place coords : {destination_place}")
    with open(known_places_json_file, "r") as known_places_file:
        known_places = json.loads(known_places_file.read())
        location_x, location_y, location_z = False, False, False
        for location in known_places.get("locations", []):
            print(location)
            print(f'{location.get("name")} vs {destination_place.lower()}')
            if location.get("name").lower() == destination_place.lower():
                location_x, location_y, location_z = location['coords'][0], location['coords'][1], location['coords'][2]
                return[location_x,location_y,location_z]
                break
        if location_x and location_y:
            return[location_x,location_y,location_z]
        else:
            return [None,None, None]