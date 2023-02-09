from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref



db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
   """Connect database"""

   db.app = app
   db.init_app(app)

class User(db.Model):

   __tablename__ = "users"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   username = db.Column(db.Text, nullable=False, unique=True)
   first_name = db.Column(db.Text, nullable=False)
   last_name = db.Column(db.Text, nullable=False)
   email = db.Column(db.Text, nullable=False, unique=True)
   password = db.Column(db.Text, nullable=False)
   image_url = db.Column(db.Text)
   contribute_id = db.relationship('Contribute', backref='users', lazy=True)


   @classmethod
   def register(cls, username, first_name, last_name, email,  pwd, image_url):

      hashed = bcrypt.generate_password_hash(pwd)

      hashed_utf8 = hashed.decode("utf8")

      return cls(username=username, first_name=first_name, last_name=last_name, email=email, password=hashed_utf8, image_url=image_url)

   
   @classmethod
   def authenticate(cls, username, pwd):

      u = User.query.filter_by(username=username).first()

      if u and bcrypt.check_password_hash(u.password, pwd):
         return u
      else:
         return False



class Hero(db.Model):

   __tablename__ = "heroes"

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.Text, nullable=True)
   full_name = db.Column(db.Text, nullable=True)
   gender = db.Column(db.Text, nullable=True)
   race = db.Column(db.Text, nullable=True)
   height = db.Column(db.Text, nullable=True)
   weight = db.Column(db.Text, nullable=True)
   eye_color = db.Column(db.Text, nullable=True)
   hair_color = db.Column(db.Text, nullable=True)
   alter_egos = db.Column(db.Text, nullable=True)
   aliases = db.Column(db.Text, nullable=True)
   birthplace = db.Column(db.Text, nullable=True)
   first_appearance = db.Column(db.Text, nullable=True)
   intelligence = db.Column(db.Text, nullable=True)
   strength = db.Column(db.Text, nullable=True)
   speed = db.Column(db.Text, nullable=True)
   durability = db.Column(db.Text, nullable=True)
   power = db.Column(db.Text, nullable=True)
   combat = db.Column(db.Text, nullable=True)
   occupation = db.Column(db.Text, nullable=True)
   base = db.Column(db.Text, nullable=True)
   affiliation = db.Column(db.Text, nullable=True)
   relatives = db.Column(db.Text, nullable=True)
   publisher = db.Column(db.Text, nullable=True)
   alignment = db.Column(db.Text, nullable=True)
   image = db.Column(db.Text, nullable=True)






class Contribute(db.Model):

   __tablename__ = "contributions"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   attribute = db.Column(db.Text)
   value = db.Column(db.Text, nullable=False)
   url = db.Column(db.Text, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'))










  



