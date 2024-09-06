from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import timedelta
import string
import random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=7)) # session key
app.permanent_session_lifetime = timedelta(minutes=30) # session_lifetime


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])  
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        p_confirm = request.form.get('confirm_password')
        if username and password == p_confirm:
            session['username'] = username
            session['password'] = password
            return redirect(url_for('login'))
        else:
            return ("Invalid, Passwords don't match !!")   
    else:
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login(): 
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')
            if username == session['username'] and password == session['password']:
                session.permanent = True 
                flash("Successfully login", "info")
                return redirect(url_for('profile'))
            else:
                return ("Invalid, Incorrect username or password!!")   
        else:    
            return render_template("login.html", images=['images_3.png', 'images_4.png'])

@app.route('/profile')
def profile():
    if 'username' in session.keys():
        name = session['username']
        return render_template("profile.html", name=name)
    else: # session ends
        return redirect(url_for("login"))               

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__== '__main__':
    app.run(debug = True, port=5000)
