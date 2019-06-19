from flask import Flask, render_template

from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later' # NOT SECURE WILL BE REPLACED LATER

#Configure database NOT SECURE WILL BE REPLACED LATER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cuomvdlweplpwg:80ecc365d98601348d547312a5188354195e0598491be14294331b99524ab4d0@ec2-23-21-186-85.compute-1.amazonaws.com:5432/d3uj4gf635g8c1'
db = SQLAlchemy(app)



@app.route("/", methods=['GET', 'POST'])

def index():
  reg_form = RegistrationForm()
  if reg_form.validate_on_submit():
   username = reg_form.username.data
   password = reg_form.password.data

   #check username exists
   user_object = User.query.filter_by(username=username).first()

  return render_template('index.html', form=reg_form)

#synatax will flow in smoothly when bringing socket.io not really necessayre in current evrsion of flaask
if __name__ == '__main__':
  app.run(debug=True)