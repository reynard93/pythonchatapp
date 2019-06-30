import os
# https://www.youtube.com/watch?v=FWU_tJqr1Po
from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
#current_user is a proxy for user object
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from wtform_fields import *
from models import *

#note: cookies are used here, not sessions

# Configure app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')
 

#Configure database NOT SECURE WILL BE REPLACED LATER
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

#initiaise Flask-SocketIO
socketio = SocketIO(app)
ROOMS = ["lounge", "news", "games", "coding"]

#configure flask login refer to flask login documentation
login = LoginManager(app)
login.init_app(app)

#loader function for when user logins, take in a userid and returns user object
@login.user_loader
def load_user(id):
  # User.query.filter(id=id).first() but look below for easier approach (since retrieving by pri key but has to be int for the id)
  return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():
  reg_form = RegistrationForm()

  #update db if validation success
  if reg_form.validate_on_submit():
    username = reg_form.username.data
    password = reg_form.password.data

    # hash password
    hashed_pswd = pbkdf2_sha256.hash(password)

    #Add user to DB
    user = User(username=username, password=hashed_pswd)
    db.session.add(user)
    db.session.commit()

    #when login page is rendered message from flash will be passed to it, 2nd parameter is optional : the category
    flash('Registered successfully. Please login.', 'success')
    return redirect(url_for('login')) 

  return render_template('index.html', form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  #allow login if validation succeeded
  if login_form.validate_on_submit():
    user_object = User.query.filter_by(username=login_form.username.data).first()
    login_user(user_object)
    return redirect(url_for('chat'))

  return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
# @login_required
def chat():

  # if not current_user.is_authenticated:
  #   flash('Please login.', 'danger')
  #   return redirect(url_for('login')) 

    #displays flashed msg on login page , not showing not authenticated on chat pg
    # return "you do not possess the credentials" #alternative is using login_required from flask login
  # note previous you have implemented login_required yourself under a helpers.py file

  return render_template('chat.html',username=current_user.username, rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():
  logout_user()
  flash('You have logged out successfully', 'success')
  return redirect(url_for('login'))

@socketio.on('message')
def message(data):
  print(f"\n\n{data}\n\n")
  send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, 
  room=data['room']) #send to a predefined bucket called 'message'

@socketio.on('join')
def join(data):
  join_room(data['room'])
  send({'msg': data['username'] + " has joined the " + data['room'] + "room."}, room=data['room'])

@socketio.on('leave')
def leave(data):
  leave_room(data['room'])
  send({'msg': data['username'] + " has left the " + data['room'] + "room."}, room=data['room'])

#syntax will flow in smoothly when bringing socket.io not really necessay in current evrsion of flask
if __name__ == '__main__':
  # app.run(debug=True)
  app.run()