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
