import requests
import json

url = "http://localhost:5050/events"

def get_all_events():
    result = requests.get(url)
    result = json.loads(result.text)
    return result


def get_current_health():
    api_result = get_all_events()
    return api_result['playerObject']['currentHealth']

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
    