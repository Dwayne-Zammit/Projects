import requests
import json
import time
import os
import sys

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)
from items.load_items import get_item_id

url = "http://localhost:5050/events"
coord_file_path = os.path.join(parent_directory, "walker/walker/coords.txt")

def get_all_events():
    result = requests.get(url)
    result = json.loads(result.text)
    return result


def get_current_health():
    api_result = get_all_events()
    return api_result['playerObject']['currentHealth']


def get_current_run_energy():
    api_responded = False
    while api_responded == False:
        try:
            api_result = get_all_events()
            api_responded = True
        except:
            time.sleep(1)
    return int(api_result['playerObject']['runEnergy'])


def check_npc_name():
    api_result = get_all_events()
    return api_result['npcObject']['name']

def check_npc_health():
    api_result = get_all_events()
    return api_result['npcObject']['currentHealth ']

def check_if_inventory_is_full():
    url = "http://localhost:5050/inv"
    result = requests.get(url)
    inventory = json.loads(result.text)
    inventory_length = len(inventory)
    # print(f"inventory length = {inventory_length}")
    print(inventory_length)
    if inventory_length == 28:
        last_inv_slot = inventory[inventory_length-1]
        last_slot_item_id = last_inv_slot['id']
        if last_slot_item_id == -1:
            return False
        else:
            return True
    else:
        # print("inventory not full")
        return False

def check_if_bank_is_open():
    api_result = get_all_events()
    return api_result['bankOpen']
    

# def item_quantity_in_bank(item_name):
#     url = "http://localhost:5050/bank"
#     result = requests.get(url)
#     bank_items = json.loads(result.text)
#     print(item_name)
#     item_id_from_list = str(get_item_id([item_name])[2:-2].replace("'","").split(":"))
#     print(item_id_from_list)
#     # (str(item_id_from_list)[2:-2]).replace("'","").split(":")
#     for bank_item in bank_items:
#         quantity = 0
#         id = bank_item['id']
        
#         if item_id_from_list == str(item_name):
#             quantity = bank_item['quantity']
#         return quantity
#     return quantity

# item_name = "Cowhide".upper()
# item_quantity_in_bank(item_name)