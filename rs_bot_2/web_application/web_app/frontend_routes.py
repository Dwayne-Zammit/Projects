import sys
import os

from flask import render_template, redirect, url_for, request, flash
from web_app import app

# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, "../"))
print(f"{parent_directory}\\web_app\\helpers")
# Add the parent directory to sys.path
sys.path.append(f"{parent_directory}\\web_app\\")

# Import the desired module from the parent directory
from helpers.get_known_locations import known_places
from helpers.walk_to_destination_helper import auto_walk_to_destination


@app.route('/')
def index():
    return redirect(url_for('menu_page'))

@app.route('/menu', methods=['GET'])
def menu_page():
        if request.method == "GET":
            return render_template('main_menu.html')

@app.route('/auto_attack')
def auto_attack():
    return "auto attack page"

@app.route('/auto_walker',  methods=['GET', 'POST'])
def auto_walker():
    known_places_names = [name['name'] for name in known_places()]

    if request.method == "GET":
        message = "Note: Press Q to stop script if needed"
        return render_template("auto_walker.html", places=known_places_names, message=message)
    
    elif request.method == "POST":
        destination_place = request.form.get('destinationPlace')
        flash("Walking to destination")
        auto_walk_to_destination(destination_place)
        message = f"Arrived at destination: {destination_place}"

        # Redirect to the same route to ensure flashed messages are not cleared
        return redirect(url_for('auto_walker'))

    # If it's a GET request, or after the POST redirect
    return render_template("auto_walker.html", places=known_places_names, message=message)

@app.route('/pick_up_and_bank_items')
def pick_up_and_bank_items():
    return "pick_up_and_bank_items"