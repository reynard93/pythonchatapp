from flask_wtf import FlaskForm
from passlib.hash import pbkdf2_sha256
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User

#note form and field are automatically passed in, which is LoginForm, password(where the validator is called on) respectively 
#reason to write it like this is if u want to reuse/ in our case not at all, we write it like this to show the alternative to inline
def invalid_credentials(form, field):
  """ Username and password checker """
  #username cannot be gotten from field since the field is password
  username_entered = form.username.data
  password_entered = field.data

  #check username is valid
  user_object = User.query.filter_by(username=username_entered).first()
  if user_object is None:
    raise ValidationError("Username/password is incorrect")
  elif not pbkdf2_sha256.verify(password_entered, user_object.password):
    raise ValidationError("Username/password is incorrect")


class RegistrationForm(FlaskForm):
  '''Reg Form'''

  username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="must be btwn 4-25 chars")])

  password = PasswordField('password_label', validators=[InputRequired(message="password required"), Length(min=4, max=25, message="must be btwn 4-25 chars")])

  confirm_pswrd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Username required"), EqualTo('password', message="Passwords must match")] )

  submit_button = SubmitField('Create')

  #custom validator which is an inline validator V1 of validation
  def validate_username(self, username):
    user_object = User.query.filter_by(username=username.data).first()
    if user_object:
      raise ValidationError("Username already exists, select a diff username")

class LoginForm(FlaskForm):
  """Login form"""
  #message would likely not get triggered bcz og input field would have its default required msg when set the property 'required' but to factor in older browsers we include it
  username = StringField('username_label', validators=[InputRequired(message="Username required")])
  #V2 of validation, see above invalid_credentials passed in as arg and declared outside class
  password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
  submit_button = SubmitField('Login')

  


