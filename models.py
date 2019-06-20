from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

#UserMixin was added in after we imported flask_login and does not modify our db in any way
#usermixin tells flask login about our user and mixes into our class properties/mtds we can use
#the added properties/mtds comes from flask_login such as is_authenticated etc.
class User(UserMixin, db.Model):
   """User model """

   __tablename__ = "users"
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(25), unique=True, nullable=False)
   password = db.Column(db.String(), nullable=False)
