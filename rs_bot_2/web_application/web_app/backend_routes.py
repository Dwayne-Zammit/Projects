from flask import jsonify
from web_app import app

@app.route('/api/data')
def api_data():
    data = {'message': 'This is data from the backend API.'}
    return jsonify(data)

