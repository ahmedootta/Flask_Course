from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import string
import random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=7)) # session key
app.permanent_session_lifetime = timedelta(minutes=30) # session_lifetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'

db = SQLAlchemy(app)

# define tables schema
class User(db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    

    def __init__(self, username, password, isAdmin=False):
        self.username = username
        self.password = password
        self.isAdmin = isAdmin

    def __repr__ (self):
        return f"<User {self.isAdmin}>"

# create all models
with app.app_context():
    db.create_all() 
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
            with app.app_context():
                exists = User.query.filter_by(username=username).first()
                if exists:
                    return 'This User already exists!'
                new_user = User(username, generate_password_hash(password)) 
                db.session.add(new_user)
                db.session.commit()   
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
            target_user = User.query.filter_by(username=username).first()
            if target_user:
                if check_password_hash(target_user.password, password):
                        session['user_id'] = target_user.id
                        return redirect(url_for('index'))
                else:
                        return 'Incorrect Password!'    
            else:
                return 'Incorrect username entered!'
           
            return ("Invalid, Incorrect username or password!!")   
        else:    
            return render_template("login.html", images=['images_3.png', 'images_4.png'])

@app.route('/profile')
def profile():
    if 'user_id' in session.keys():
        id = session['user_id']
        logged_user = User.query.filter_by(id=id).first()
        print(logged_user)
        return render_template('profile.html', user= logged_user)
        
    else: # session ends
        return redirect(url_for("login"))               

@app.route('/admin_panel')
def adminpanel():
    if 'user_id' in session.keys():
        id = session['user_id']
        logged_user = User.query.filter_by(id=id).first()
        
        if logged_user and logged_user.isAdmin == 1:  # Explicitly check for 1 (True)
            return render_template('admin.html', user=logged_user)
        else:
            flash("You are not authorized to access this page.", "error")  # Flash error message
            return redirect(url_for("login"))
    else:  # If no user is logged in
        flash("Please log in to continue.", "error")  # Flash error message
        return redirect(url_for("login"))
         

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__== '__main__':
    app.run(debug = True, port=5000)
