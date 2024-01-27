import os
import sys
import requests
import json

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

def get_coordinates_to_destination(start_x,start_y,current_z,destination_x,destination_y, destination_z):
    url = "https://explv-map.siisiqf.workers.dev/"
    body = {
        "start": {"x": start_x, "y": start_y, "z": current_z},
        "end": {"x": destination_x, "y": destination_y, "z": destination_z},
        "player": {"members": "false"}
    }

    # Make the POST request with the json parameter
    result = requests.post(url, json=body, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://explv.github.io',
        'Connection': 'keep-alive',
        'Referer': 'https://explv.github.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'TE': 'trailers'
    })
    path = result.text
    path = json.loads(path)
    if not path['path']:
        return "Error obtaining path from https://explv.github.io"
    path = path['path']
    coords_file_path = os.path.join(parent_directory, "walker/walker/coords.txt")
    with open(coords_file_path, "w") as coordinates_file:
        pass
    with open(coords_file_path, "a") as coordinates_file:
        # coordinates_file.write(f"{path[0]['x']},{path[0]['y']},{path[0]['z']}\n")
        # print(path)
        if len(path) < 5:
            for next_step in path:
                coordinates_file.write((f"{next_step['x']},{next_step['y']},{next_step['z']}\n"))
        else:
            coordinates_file.write(f"{path[0]['x']},{path[0]['y']},{path[0]['z']}\n")
            for i in range(1, len(path) - 1, 2):
                coordinates_file.write(f"{path[i]['x']},{path[i]['y']},{path[i]['z']}\n")
            coordinates_file.write(f"{path[-1]['x']},{path[-1]['y']},{path[-1]['z']}\n")
        return  
