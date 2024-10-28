from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import smtplib
import random

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'emergenease'

mysql = MySQL(app)
app.secret_key = 'your_secret_key'

# Home Route
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password!')
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# SOS Button Functionality
@app.route('/sos', methods=['POST'])
def sos_alert():
    if 'loggedin' in session:
        user_id = session['id']
        location = request.form['location']
        send_emergency_alert(user_id, location)
        flash('Emergency Alert Sent!', 'success')
    else:
        flash('You need to be logged in to use this feature.', 'danger')
    return redirect(url_for('home'))

# Function to send alerts to emergency contacts
def send_emergency_alert(user_id, location):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM emergency_contacts WHERE user_id = %s', [user_id])
    contacts = cursor.fetchall()

    for contact in contacts:
        send_email(contact[3], f"Emergency at {location} for user {session['username']}")

def send_email(to_email, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    server.sendmail('your-email@gmail.com', to_email, body)
    server.quit()

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
        mysql.connection.commit()
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
