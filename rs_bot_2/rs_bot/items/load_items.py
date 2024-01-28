import os
import orjson

current_directory = os.path.dirname(os.path.realpath(__file__))

items_info_file = f"{current_directory}\item_ids.json"

with open(items_info_file, "r") as items_information_file:
    items_file = items_information_file.read()

items_json = orjson.loads(items_file)

def get_item_id(target_items):
    json_string = ""
    for target_item in target_items:
        json_string += (f'"{target_item}":{items_json[target_item.upper()]},')
    json_string = "{" + json_string[0:-1] + "}"
    items_json_return = orjson.loads(json_string)
    return items_json_return
