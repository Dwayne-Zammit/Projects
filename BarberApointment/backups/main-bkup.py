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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class AppointmentForm(FlaskForm):
    date = DateField('Date', render_kw={"placeholder": "DD/MM/YYYY"})
    name = StringField('Name')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AppointmentForm()
    if form.validate_on_submit():
        date = str(form.date.data)  # Convert date to string
        time = request.form.get('time')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        print(phone)
        print(email)
        # Execute the insert statement
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        print(f"INSERT INTO appointments (datetime, name, email, phone) VALUES ({str(date + ' ' + time)}, '{name}', '{email}', {phone})")
        cursor.execute(f"INSERT INTO appointments (datetime, name, email, phone) VALUES ('{str(date + ' ' + time)}', '{name}', '{email}', {phone})")
        conn.commit()
        conn.close()

        # Redirect or render a success message
        return 'Appointment booked successfully!'

    # Fetch the taken times from the database
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT datetime FROM appointments')
    taken_times = [row[0].split(' ')[1] for row in cursor.fetchall()]
    conn.close()
    # Render the HTML template with the form and taken times
    return render_template('appointment_form.html', form=form, takenTimes=taken_times)

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
        
        available_times = [row[0].split(' ')[1] for row in cursor.fetchall()]
        print(available_times)
        conn.close()
        return jsonify(available_times)
    else:
        return jsonify([])

@app.route('/available_times')
def available_times():
    selected_date = request.args.get('date')
    print(selected_date)
    # Fetch the taken times from the database for the selected date
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT datetime FROM appointments WHERE datetime like '%{selected_date}%'")
    # print('SELECT datetime FROM appointments WHERE datetime = ?', (selected_date,))
    taken_times = [row[0].split(' ')[1] for row in cursor.fetchall()]
    print(taken_times)
    conn.close()

    # Generate the list of available times based on the taken times
    all_times = []
    for hour in range(8, 18):
        for minute in ['00', '30']:
            current_time = f'{hour}:{minute}'
            if current_time not in taken_times:
                all_times.append(current_time)
    print(all_times)
    return jsonify(availableTimes=all_times)



@app.route('/contact_us', methods=['GET'])
def about_us():
    return render_template("contact_us.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')