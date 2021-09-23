from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import validate_arguments, secure_filename
from wtforms import StringField, PasswordField
from wtforms import validators
from wtforms.validators import InputRequired, URL, EqualTo, Email, ValidationError
from wtforms.widgets.core import Input
from models import User

class RegisterForm(FlaskForm):
   """Register a user"""

   username = StringField("Username", validators=[InputRequired(), validators.length(min=4, max=16)])
   first_name = StringField("First name", validators=[InputRequired(), validators.length(min=2, max=16)])
   last_name = StringField("Last name", validators=[InputRequired(), validators.length(min=2, max=16)])
   email = StringField("Email", validators=[InputRequired(), Email(), validators.length(min=6, max=35)])
   password = PasswordField("Password", validators=[InputRequired(), validators.length(min=6, max=20), EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField("Confirm Password")
   image_url = StringField('(Optional) Image URL', default="/static/imgs/user-default-image.png")


class LoginForm(FlaskForm):
   """Log in a user"""

   username = StringField("Username", validators=[InputRequired()])
   password = PasswordField("Password", validators=[InputRequired()])

class UserEditForm(FlaskForm):
   username = StringField("Username", validators=[InputRequired(), validators.length(min=4, max=16)])
   email = StringField("Email", validators=[InputRequired(), validators.length(min=6, max=35)])
   password = PasswordField('Password', validators=[InputRequired(), validators.length(min=6, max=20)])

class ContributeForm(FlaskForm):
   """Contribute to hero profiles"""

   value = StringField("Proposed Value", validators=[InputRequired()])
   resource = StringField("Resource URL", validators=[URL(message="Not a valid URL")])


class PhotoForm(FlaskForm):
   photo = FileField("Upload your profile photo", validators=[
      FileRequired(),
      FileAllowed(['jpg', 'png'], 'Images only!')
   ])
