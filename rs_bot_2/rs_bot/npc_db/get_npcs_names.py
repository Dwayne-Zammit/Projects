import os
import sys
import orjson

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

npcs_list = f"{current_directory}\\npc_db.json"

with open(npcs_list, "r") as npcs_db_file:
    npcs_file = npcs_db_file.read()
    npcs_json = orjson.loads(npcs_file)

def get_npcs_names():
    return npcs_json
