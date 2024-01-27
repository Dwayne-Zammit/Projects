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
    # body = {'start': {'x': 3293, 'y': 3151, 'z': 0}, 'end': {'x': 3274, 'y': 3191, 'z': 0}, 'player': {'members': 'false'}}
    print(body)

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

    # Now you can work with the response, for example:
    path = result.text
    # print(path)
    # print(path)
    path = json.loads(path)
    # print("path below:")
    # print(path)
    if not path['path']:
        return "Error obtaining path from https://explv.github.io"
    path = path['path']
    # print(path)
    coords_file_path = os.path.join(parent_directory, "walker/walker/coords.txt")
    # print(coords_file_path)
    # empty coords file ##
    with open(coords_file_path, "w") as coordinates_file:
        pass  # This will empty the file
    # print(path)
    ## write coordinates in_file ##
    with open(coords_file_path, "a") as coordinates_file:

        for line in path:

            coordinates_file.write(f"{line['x']},{line['y']},{line['z']}\n")
    return  
