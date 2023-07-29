# from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import DateField, SubmitField
# from wtforms.validators import DataRequired

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

# class CalendarForm(FlaskForm):
#     date = DateField('Date', validators=[DataRequired()])
#     submit = SubmitField('Submit')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = CalendarForm()

#     if form.validate_on_submit():
#         # Process the submitted form data here
#         selected_date = form.date.data
#         # Perform further actions with the selected date

#     return render_template('index.html', form=form)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField
import sqlite3
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint


from email import message
from fnmatch import translate
import pyodbc as pyodbc
import pandas as pd
from flask import Flask, render_template, request
import os
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from pathlib import Path
from flask import Flask, render_template, request, url_for, redirect
import subprocess
import time
import os.path
from flask import session
import csv
import logging
from datetime import datetime
from flask import send_from_directory
import shutil
import zipfile
from os import listdir
from os.path import isfile, join
import os
import base64
from io import BytesIO
from flask import Flask, render_template, redirect, url_for, flash, session, \
    abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
import onetimepass
import pyqrcode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from flask_paginate import Pagination, get_page_parameter
import numpy as np
import requests

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    otp = db.Column(db.Integer)

class AppointmentForm(FlaskForm):
    date = DateField('Date', render_kw={"placeholder": "DD/MM/YYYY"})
    name = StringField('Name')
    submit = SubmitField('Submit')


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    otp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=DevOps Tool' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)

#get current_user id:
def current_user_username():
    cur_user = str(current_user)
    cur_user = cur_user.replace('<User ','')
    cur_user = cur_user.replace('>','')
    user = User.query.filter_by(id=cur_user).all()
    for line in user:
        dict = (line.__dict__)    
    for key, value in dict.items():
        if key == 'username':
            username = value
    return(username)

@lm.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Retype Password',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    token = StringField('Token', validators=[DataRequired(), Length(6, 6)])
    submit = SubmitField('Login')


@app.route('/registration_index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('register'))
        # add new user to the database
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # redirect to the two-factor auth page, passing username in session
        session['username'] = user.username
        return redirect(url_for('two_factor_setup'))
    return render_template('register.html', form=form)


@app.route('/twofactor')
def two_factor_setup():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('login'))
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('two-factor-setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('admin_view_appointments'))
    if request.method == 'GET':
        return render_template('login.html')    
    # form = LoginForm()
    if request.method == 'POST':
    # if form.validate_on_submit():
        
        user = User.query.filter_by(username=request.form['username']).first()
        print(user)
        print(user.verify_totp(request.form['token']))
        if user is None or not user.verify_password(request.form['password']) or \
            not user.verify_totp(request.form['token']):
            flash('Invalid username, password or token.')
            # return redirect(url_for('login', message="Incorrect Credentials"))
            return render_template('login.html', message="Incorrect credentials")
        # log user in
        login_user(user)
        flash('You are now logged in!')
        return redirect(url_for('admin_view_appointments'))


@app.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('index'))


# create database tables if they don't exist yet



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         otp = request.form['otp']
        
#         user = User.query.filter_by(username=username).first()
        
#         if user and user.password == password and user.otp == int(otp):
#             session['username'] = username
#             return redirect('/home')
#         else:
#             return render_template('login.html', message='Invalid credentials')
    
#     return render_template('login.html')


@app.route('/home')
def home():
    if 'username' in session:
        return session['username']
    else:
        return redirect('/')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         # Check if the username already exists in the database
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             return render_template('register.html', message='Username already exists')
        
#         # Generate a random one-time passcode
#         otp = randint(100000, 999999)
        
#         # Create a new user object
#         new_user = User(username=username, password=generate_password_hash(password), otp=otp)
        
#         # Add the user to the database
#         db.session.add(new_user)
#         db.session.commit()
        
#         return render_template('register.html', message='Registration successful')
    
#     return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def book_appointment():
    form = AppointmentForm()
    if request.method == "GET":

        # Fetch the taken times from the database
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT datetime FROM appointments')
        taken_times = [row[0].split(' ')[1] for row in cursor.fetchall()]
        conn.close()
        # Render the HTML template with the form and taken times
        return render_template('appointment_form.html', form=form, takenTimes=taken_times)
       
    if request.method == "POST":
    # if form.validate_on_submit():
        # date = str(form.datepicker.data)  # Convert date to string
        time = request.form.get('time')
        date = request.form.get('datepicker')
        date_object = datetime.strptime(date, "%a %b %d %Y")
        # Format the datetime object to the desired output format "2023-06-23 8:30"
        formatted_date = date_object.strftime("%Y-%m-%d")
        print(date)
        print(f"this is time {time}")
        # time = request.form.get('time')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        print(phone)
        print(email)
        # Execute the insert statement
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        print(f"INSERT INTO appointments (datetime, name, email, phone) VALUES ({formatted_date + ' ' + time}, '{name}', '{email}', {phone})")
        cursor.execute(f"INSERT INTO appointments (datetime, name, email, phone) VALUES ('{str(formatted_date + ' ' + time)}', '{name}', '{email}', {phone})")
        conn.commit()
        conn.close()
        # Redirect or render a success message
        # flash('Appointment booked successfully!')
        return 'Appointment booked successfully!'

@app.route('/fetch_taken_times_from_database', methods=['GET'])
def fetch_taken_times_from_database():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT datetime FROM appointments')
    taken_times = [row[0] for row in cursor.fetchall()]
    conn.close()
    return taken_times


@app.route('/get-available-times', methods=['GET'])
def get_available_times():
    selected_date = request.args.get('date')
    if selected_date:
        # Perform the query to fetch available times based on the selected date
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT datetime FROM appointments WHERE date(datetime) = ?', (selected_date,))
        print("hello")
        available_times = [row[0].split(' ')[1] for row in cursor.fetchall()]
        print(available_times)
        conn.close()
        return jsonify(available_times)
    else:
        return jsonify([])


@app.route('/available_times/<string:arg>')
def available_times(arg):
    # selected_date = request.form.get('datepicker')
    selected_date = arg
    print(selected_date)
    # time = request.form.get('time')
    # date = request.form.get('datepicker')
    date_object = datetime.strptime(selected_date, "%a %b %d %Y")
    # day_of_week = date_object.weekday()
    day_of_week = date_object.strftime("%A")
    print(day_of_week)
    # Format the datetime object to the desired output format "2023-06-23 8:30"
    formatted_date = date_object.strftime("%Y-%m-%d")
    print(formatted_date)
    # Fetch the taken times from the database for the selected date
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    print(f"SELECT datetime FROM appointments WHERE datetime like '%{formatted_date}%'")
    cursor.execute(f"SELECT datetime FROM appointments WHERE datetime like '%{formatted_date}%'")
    # print('SELECT datetime FROM appointments WHERE datetime = ?', (selected_date,))
    taken_times = [row[0].split(' ')[1] for row in cursor.fetchall()]
    print(taken_times)
    conn.close()
    # (f"Date: {formatted_date}")
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    print(f"SELECT start_time,end_time FROM working_hours WHERE day = '{day_of_week}'")
    cursor.execute(f"SELECT start_time,end_time FROM working_hours WHERE day = '{day_of_week}'")
    opening_hours = cursor.fetchall()
    print(opening_hours)
    start_time = opening_hours[0][0]
    end_time = opening_hours[0][1]
    print(f"this is start time {int(start_time)}")
    print(f"this is end time {int(end_time)}")
    # Generate the list of available times based on the taken times
    all_times = []
    # for hour in range(10, 19):
    for hour in range(int(start_time), int(end_time) + 1):    
        for minute in ['00', '30']:
            current_time = f'{hour}:{minute}'
            if current_time not in taken_times:
                if current_time != "12:00" and current_time != "12:30":
                    all_times.append(current_time)
    print(all_times)
    ## remove last item from list as the logic is creating an extra 30 mins ##
    all_times.pop(-1)

    # all_times = all_times.replace('12:00')
    return jsonify(availableTimes=all_times)


# @app.route('/available_times/<string:arg>')
# def available_times(arg):
#     # selected_date = request.form.get('datepicker')
#     selected_date = arg
#     print(selected_date)
#     # time = request.form.get('time')
#     # date = request.form.get('datepicker')
#     date_object = datetime.strptime(selected_date, "%a %b %d %Y")
#     # Format the datetime object to the desired output format "2023-06-23 8:30"
#     formatted_date = date_object.strftime("%Y-%m-%d")
#     print(formatted_date)
#     # Fetch the taken times from the database for the selected date
#     conn = sqlite3.connect('database/database.db')
#     cursor = conn.cursor()
#     print(f"SELECT datetime FROM appointments WHERE datetime like '%{formatted_date}%'")
#     cursor.execute(f"SELECT datetime FROM appointments WHERE datetime like '%{formatted_date}%'")
#     # print('SELECT datetime FROM appointments WHERE datetime = ?', (selected_date,))
#     taken_times = [row[0].split(' ')[1] for row in cursor.fetchall()]
#     print(taken_times)
#     conn.close()

#     # Generate the list of available times based on the taken times
#     all_times = []
#     for hour in range(10, 19):
#         for minute in ['00', '30']:
#             current_time = f'{hour}:{minute}'
#             if current_time not in taken_times:
#                 if current_time != "12:00" and current_time != "12:30":
#                     all_times.append(current_time)
#     print(all_times)
#     # all_times = all_times.replace('12:00')
#     return jsonify(availableTimes=all_times)



@app.route('/contact_us', methods=['GET'])
def contact_us():
    return render_template("contact_us.html")

@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template("about_us.html")

@app.route('/services', methods=['GET'])
def services():
    return render_template("services.html")


#### Admin Stuf ####
@app.route('/admin/appointments', methods=['GET'])
def admin_view_appointments():
    if current_user.is_authenticated:
        # return render_template('prod_or_preprod.html')
        return render_template('calendar.html')
    else:
        return redirect(url_for('login'))
    # return "Admin"


@app.route('/get_appointments')
def get_appointments():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, datetime, name, email, phone FROM appointments')
    rows = cursor.fetchall()

    appointments = []
    for row in rows:
        appointment = {
            'id': row[0],
            'title': row[2],
            'start': row[1],
            'description': f'Email: {row[3]}, Phone: {row[4]}',
        }
        appointments.append(appointment)
    print(appointments)
    conn.close()

    return jsonify(appointments)

# @app.route('/admin/delete_appointment/<string:arg>/<string:arg1>', methods=['POST'])
# def delete_booking(arg,arg1):
#     print(arg)
#     # Convert epoch to datetime object
#     # arg = int(arg)
#     dt = datetime.fromtimestamp(int(arg) // 1000)  # Divide by 1000 to convert milliseconds to seconds
#     # Format the datetime object as "YYYY-MM-DD HH:mm"
#     formatted_datetime = dt.strftime("%Y-%m-%d %H:%M")
#     print(formatted_datetime)
#     conn = sqlite3.connect('database/database.db')
#     cursor = conn.cursor()
#     print(f'DELETE FROM appointments where datetime = "{formatted_datetime}" and name="{arg1}"')
#     cursor.execute(f'DELETE FROM appointments where datetime = "{formatted_datetime}" and name="{arg1}"')
#     conn.commit()
#     return redirect(url_for('admin_view_appointments'))

@app.route('/admin/delete_appointment/<string:arg>/<string:arg1>', methods=['POST'])
def delete_booking(arg, arg1):
    if current_user.is_authenticated:
        # return render_template('prod_or_preprod.html')
        dt = datetime.fromtimestamp(int(arg) // 1000)  # Divide by 1000 to convert milliseconds to seconds
        formatted_datetime = dt.strftime("%Y-%m-%d %H:%M")  # Format the datetime object with leading zeros
        formatted_datetime = formatted_datetime.replace(" 0", " ")  # Remove leading zero from hours
        print(formatted_datetime)
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM appointments where datetime = "{formatted_datetime}" and name="{arg1}"')
        conn.commit()
        return redirect(url_for('admin_view_appointments'))
    else:
        return redirect(url_for('login'))


with app.app_context():
    # Create the database tables
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')