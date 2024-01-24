from flask import render_template
from web_app import app

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():
    return "Hello World"