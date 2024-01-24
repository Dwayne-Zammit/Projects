from flask import Flask

app = Flask(__name__)

# Include backend (API) routes
from web_app import backend_routes

# Include frontend routes
from web_app import frontend_routes

app.secret_key = 'SecureKey'