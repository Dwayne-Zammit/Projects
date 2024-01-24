import requests
import json
import datetime
import time
from playsound import playsound
from api_request_events import get_current_health


def get_date_time():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

def send_discord_message(webhook_url, message):
    payload = {
        'content': message
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print("Failed to send message. Status code:", response.status_code)
    return    

def check_last_npc_fight():
    url = "http://127.0.0.1:5050/events"
    log_file = "monitor_last_npc_fight.log"
    result = requests.get(url)
    print(result.text)
    result = json.loads(result.text)
    npc = result['npcObject']
    if len(npc['name']) > 0:
        with open(log_file, "a") as log_file:
            log_file.write(f"\n{get_date_time()} Currently Fighting a {npc['name']}")
    else:
        with open(log_file, "a") as log_file:    
            log_file.write(f"\n{get_date_time()} Not Fighting an npc")
    return

def check_logs_in_last_lines(file_path, search_string):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the last 5 lines from the file
        lines = file.readlines()[-10:]

        # Check if the search string is present in any of the lines
        for line in lines:
            if search_string in line:
                return True
    return False


def monitor_npc_log():
    file_path = "monitor_last_npc_fight.log"
    search_string = "Currently"
    found = check_logs_in_last_lines(file_path, search_string)
    return found

def play_alarm_sound(sound_file_path):
    playsound(sound_file_path)

def alert_discord_if_we_are_in_combat():
    url = "http://127.0.0.1:5050/events"
    result = requests.get(url)
    result = json.dumps(result.text)
    npc = result['npc']['name']
    if len(npc) > 0:
        health = get_current_health()
        print("We have not been fighting an npc for the last 10 minutes. Will inform an admin")
        webhook_url = "https://discord.com/api/webhooks/1117257987308916847/fBjvuFhx9K1hsfxFP6v9u4FleyNWEBabvAfJo8tE9l_p_Fzm3JHmMqk6AIquSlThjy-m"
        message = f"We are currently fighting a {npc}"
        send_discord_message(webhook_url, message)
    return
        

while True:
    check_last_npc_fight()
    found = monitor_npc_log()
    if found == True:
        print("In the last 10 minutes we fought an npc, everything is running fine")
    else:
        print("We have not been fighting an npc for the last 10 minutes. Will inform an admin")
        webhook_url = "https://discord.com/api/webhooks/1117257987308916847/fBjvuFhx9K1hsfxFP6v9u4FleyNWEBabvAfJo8tE9l_p_Fzm3JHmMqk6AIquSlThjy-m"
        message = "Runescape Bot has not been fighting any npcs for the last 10 minutes. Kindly check what went wrong."
        send_discord_message(webhook_url, message)
        print("Attempting to sound alarm")
        sound_file_path = "../sounds/alarm.wav"
        play_alarm_sound(sound_file_path)
        print("Closing Monitorring script since we are currently not fighting npcs. Admin has been informed.")
        exit(0)
    time.sleep(60)
