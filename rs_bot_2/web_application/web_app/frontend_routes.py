import sys
import os

from flask import render_template, redirect, url_for, request, flash
from web_app import app
import threading
import time

# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, "../"))
rs_bot_directory = os.path.abspath(os.path.join(current_directory, "../../"))
# Add the parent directory to sys.path
sys.path.append(f"{parent_directory}\\web_app\\")
# sys.path.append(f"..\\{parent_directory}\\items\\")
sys.path.append(f"{rs_bot_directory}\\items")
# Import the desired module from the parent directory
from helpers.get_known_locations import known_places
from helpers.walk_to_destination_helper import auto_walk_to_destination
from helpers.start_hide_tanning import start_hide_tannery
from helpers.attack_npc import attack_npc
from rs_bot.items.load_items import get_item_names
from rs_bot.npc_db.get_npcs_names import get_npcs_names



@app.route('/')
def index():
    return redirect(url_for('menu_page'))

@app.route('/menu', methods=['GET'])
def menu_page():
        if request.method == "GET":
            return render_template('main_menu.html')

@app.route('/auto_walker',  methods=['GET', 'POST'])
def auto_walker():
    known_places_names = [name['name'] for name in known_places()]
    item_names = ""
    if request.method == "GET":
        message = "Note: Press Q to stop script if needed"
        return render_template("auto_walker.html", places=known_places_names, message=message)
    
    elif request.method == "POST":
        destination_place = request.form.get('destinationPlace')
        run_task_thread = threading.Thread(target=auto_walk_to_destination, args=(destination_place,))
        run_task_thread.start()
        return render_template("auto_walker.html", places=known_places_names, message=f"Navigating to destination: {destination_place}")


# @app.route('/pick_up_and_bank_items')
# def pick_up_and_bank_items():
#     return "pick_up_and_bank_items"


@app.route('/auto_attack', methods=["GET", "POST"])
def auto_attack(): 
    known_places_names = [name['name'] for name in known_places()]
    item_names = get_item_names()
    npcs_names = get_npcs_names()
    bank_names = [name['name'] for name in known_places() if "bank" in name['name'].lower()]
    if request.method == "GET":
        return render_template("auto_attack_npc.html", places=known_places_names, dropped_item_names = item_names, npcs_names = npcs_names,bank_locations=bank_names, message = "Press Q to quit")
    elif request.method == "POST":
        npc_location = request.form.get('npcLocation')
        npc_name = request.form.get('npc_name')
        dropped_item_name = request.form.get('droppedItemName')
        bank_items = request.form.get('bankItems')
        pickup_items = request.form.get('pickupItems')
        bank_location = request.form.get('bankLocation')
        
        # Check if any variable is None and set it to an empty string if so
        npc_location = npc_location if npc_location is not None else ""
        npc_name = npc_name if npc_name is not None else ""
        dropped_item_name = dropped_item_name if dropped_item_name is not None else ""
        # bank_items = "False" if bank_items is not None else "True"
        # pickup_items = pickup_items if pickup_items is not None else ""

        if pickup_items == None:
            pickup_items = "False"
            
        if bank_items == None:
            pickup_items = "False"    
        
        pickup_items_only_and_bank_them = "False"
        attack_npc_option = "True"
        # print(pickup_items)
        run_task_thread = threading.Thread(target=attack_npc, args=(bank_location,npc_location,pickup_items_only_and_bank_them,attack_npc_option,pickup_items,dropped_item_name,bank_items, npc_name),)
        run_task_thread.start()
        return render_template("auto_attack_npc.html", places=known_places_names, dropped_item_names = item_names, npcs_names = npcs_names,bank_locations=bank_names, message="Auto Attack started")


@app.route('/hide_tannery', methods=["GET", "POST"])
def hide_tannery():
    known_places_names = [name['name'] for name in known_places() if "tannery" in name['name'].lower()]
    message = ""
    if request.method == "GET":
        return render_template("hide_tanner.html", places=known_places_names, message=message)
    
    elif request.method == "POST":
        tannery_location = request.form.get('tanneryLocation')
        run_task_thread = threading.Thread(target=start_hide_tannery)
        run_task_thread.start()
        message = "Tannery started"
        return render_template("hide_tanner.html", places=known_places_names, message=message)
