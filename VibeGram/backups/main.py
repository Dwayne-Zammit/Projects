from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)


# def validate_login(username, password):
#     ## sqlite db connection
#     conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
#     cursor = conn.cursor()

#     ## check if user is already logged in
#     cookie_expiry_time_db = datetime.strptime(cookie_expiry_time_db, '%d/%m/%y %H:%M')
#     time_diff = datetime.utcnow() - cookie_expiry_time_db
#     # Check if an hour has passed
#     if time_diff >= timedelta(hours=1):
#         return True

#     # Execute a SELECT query
#     cursor.execute(f'SELECT * FROM Login where username = "{username}"')
#     # Fetch the results
#     results = cursor.fetchall()
#     password_db = ""
#     cookie_expiry_time = ""
#     # now = datetime.utcnow()
#     # formatted_time = now.strftime('%d/%m/%y %H:%M')

#     # if formatted_time 
#     ## map the results to variables
#     for result in results:
#         username_db = result[0]
#         password_db = result[1]
#         cookie_expiry_time = result[2]

#     if password == password_db:
#         return True
#     else:
#         return False    


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         return render_template("login.html")
#     elif request.method == "POST":
#         username = request.form['username']
#         password = request.form['password']
#         print(username)
#         print(password)
#         # validate_login("Admin", "Password") 
#         # if validate_login(username, password) == True:
#         #     return("logged in")
#         # else:
#         #     return("Incorrect login")

# @app.route("/home")
# def home():
#     # print("This is the home")
#     return render_template("home.html")


if (__name__) == "__main__":
    app.run(debug=True, port=8080)
