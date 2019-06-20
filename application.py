from flask import Flask, render_template, redirect, url_for
#current_user is a proxy for user object
from flask_login import LoginManager, login_user, current_user
from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later' # NOT SECURE WILL BE REPLACED LATER

#Configure database NOT SECURE WILL BE REPLACED LATER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cuomvdlweplpwg:80ecc365d98601348d547312a5188354195e0598491be14294331b99524ab4d0@ec2-23-21-186-85.compute-1.amazonaws.com:5432/d3uj4gf635g8c1'
db = SQLAlchemy(app)

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
    return redirect(url_for('login')) 

  return render_template('index.html', form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  #allow login if validation succeeded
  if login_form.validate_on_submit():
    user_object = User.query.filter_by(username=login_form.username.data).first()
    login_user(user_object)
    if current_user.is_authenticated:
      return "Logged in, finally!"
    return "Not logged in :("
  return render_template("login.html", form=login_form)

#syntax will flow in smoothly when bringing socket.io not really necessayre in current evrsion of flaask
if __name__ == '__main__':
  app.run(debug=True)