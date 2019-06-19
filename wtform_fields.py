from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
  '''Reg Form'''

  username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="must be btwn 4-25 chars")])

  password = PasswordField('password_label', validators=[InputRequired(message="password required"), Length(min=4, max=25, message="must be btwn 4-25 chars")])

  confirm_pswrd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Username required"), EqualTo('password', message="Passwords must match")] )

  submit_button = SubmitField('Create')