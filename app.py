from flask import Flask, render_template, jsonify, redirect, request, session, flash, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os
from werkzeug.utils import secure_filename
from models import connect_db, db, User, Hero, Contribute
from forms import LoginForm, PhotoForm, RegisterForm, ContributeForm, UserEditForm
from secretcode import api_key

BASE_URL = f"https://superheroapi.com/api/{api_key}"

CURR_USER_KEY = "curr_user"


app = Flask(__name__)

uploads = os.path.join('static', 'uploads')


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', "postgresql:///hero_db") 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'hellosecret2')


connect_db(app)
# db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)



@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def pull_data():

   res = requests.get(f"{BASE_URL}/search/_")
   data = res.json()
   

   i = 0
   while i < 732:

     hero = Hero(name=data["results"][i]["name"],
     full_name = data["results"][i]["biography"]["full-name"],
     gender = data["results"][i]["appearance"]["gender"],
     race = data["results"][i]["appearance"]["race"],
     height = data["results"][i]["appearance"]["height"],
     weight = data["results"][i]["appearance"]["weight"],
     eye_color = data["results"][i]["appearance"]["eye-color"],
     hair_color = data["results"][i]["appearance"]["hair-color"],
     alter_egos = data["results"][i]["biography"]["alter-egos"],
     aliases = data["results"][i]["biography"]["aliases"],
     birthplace = data["results"][i]["biography"]["place-of-birth"],
     first_appearance = data["results"][i]["biography"]["first-appearance"],
     intelligence = data["results"][i]["powerstats"]["intelligence"],
     strength = data["results"][i]["powerstats"]["strength"],
     speed = data["results"][i]["powerstats"]["speed"],
     durability = data["results"][i]["powerstats"]["durability"],
     power = data["results"][i]["powerstats"]["power"],
     combat = data["results"][i]["powerstats"]["combat"],
     occupation = data["results"][i]["work"]["occupation"],
     base = data["results"][i]["work"]["base"],
     affiliation = data["results"][i]["connections"]["group-affiliation"],
     relatives = data["results"][i]["connections"]["relatives"],
     publisher = data["results"][i]["biography"]["publisher"],
     alignment = data["results"][i]["biography"]["alignment"],
     image = data["results"][i]["image"]["url"])

     db.session.add_all([hero])

     db.session.commit()

     i = i + 1

@app.errorhandler(404)
def not_found(e):

   return render_template('404.html')


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def index():

   return render_template('index.html')

@app.route('/heroes')
def all_heroes():
   """Shows list of all characters in db"""
   heroes = Hero.query.all()

   return render_template('heroes.html', heroes=heroes)

@app.route('/marvel')
def marvel_list():
   """Shows list of all marvel characters in db"""
   
   heroes = Hero.query.filter(Hero.publisher == "Marvel Comics").all()
   

   return render_template('marvel.html', heroes=heroes)

@app.route('/DC')
def dc_list():
   """Shows list of all dc characters in db"""

   heroes = Hero.query.filter(Hero.publisher == "DC Comics").all()

   return render_template('dc.html', heroes=heroes)

   


@app.route('/register', methods=["GET", "POST"])
def register():
   """Handle user registration and store in db"""

   if CURR_USER_KEY in session:
      del session[CURR_USER_KEY]
   
   form = RegisterForm()

   if form.validate_on_submit():
      name = form.username.data.capitalize()
      first_name = form.first_name.data.capitalize()
      last_name = form.last_name.data.capitalize()
      email = form.email.data.capitalize()
      pwd = form.password.data
      image_url = form.image_url.data or User.image_url.default.arg

      user = User.register(name, first_name, last_name, email, pwd, image_url)

      if User.query.filter_by(username=name).first():
         flash(f"Whoops!, that username already exists.", "error")
         return redirect('/register')
   
      elif User.query.filter_by(email=email).first():
         flash(f"Oh no!, that email already exists.", "error")
         return redirect('/register')

      db.session.add(user)
      db.session.commit()

      do_login(user)
      flash(f"Account successfully created!", "success")

      return redirect('/')

   else:
      return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
   """Login form to login user"""

   form = LoginForm()

   if form.validate_on_submit():
      name = form.username.data.capitalize()
      pwd = form.password.data

      user = User.authenticate(name, pwd)

      if user:
         do_login(user)
         flash(f"Welcome back, { user.username }", 'success')
         return redirect("/")

      flash('Invalid password, please try again!', 'error')

   return render_template("login.html", form=form)

@app.route('/users/edit', methods=["GET", "POST"])
def edit_user():
   """Edit user profile"""

   if not g.user:
      flash("Access unauthorized.", "danger")
      return redirect('/')

   user = g.user
   form = UserEditForm(obj=user)

   if form.validate_on_submit():
      if User.authenticate(user.username, form.password.data):
         user.username = form.username.data
         user.email = form.email.data

         db.session.commit()
         return redirect(f"/users/{user.id}")
   
   return render_template('users/edit.html', form=form, user_id=user.id)


   

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()
    flash(f"Account successfully deleted", 'success')
    db.session.delete(g.user)
    db.session.commit()
    

    return redirect("/register")

@app.route('/users/<int:user_id>')
def user_profile(user_id):
   """Gets the users profile"""

   user = User.query.get(user_id)
   if g.user.id != user.id:
      return redirect(f"/users/{g.user.id}")
      
   if not g.user:
      flash("Unauthorized Access, you must be logged in to view this content", "danger")
      return redirect('/login')
      

   return render_template('users/profile.html', user=user)

@app.route('/upload', methods=["GET", "POST"])
def upload():
   """Allows user to upload photo to profile"""

   if not g.user:
      flash("Access unauthorized.", "danger")
      return redirect("/")

   user = g.user
   form = PhotoForm()

   if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            uploads, filename
        ))
        user.image_url = f"/static/uploads/{filename}"
        db.session.commit()
        return redirect(url_for('upload'))

   return render_template('upload.html', form=form)


@app.route('/profile/<int:id>')
def search_hero(id):
   """Shows character profile"""
   
   hero = Hero.query.get(id)

   attr = {
      "name": "name",
      "full name": "full name",
      "gender": "gender",
      "race": "race",
      "height": "height",
      "weight": "weight",
      "eye color": "eye color",
      "hair color": "hair color",
      "alter egos": "alter egos",
      "aliases": "aliases",
      "birthplace": "birthplace",
      "first appearance": "first appearance",
      "intelligence": "intelligence",
      "strength": "strength",
      "speed": "speed",
      "durability": "durability",
      "power": "power",
      "combat": "combat",
      "occupation": "occupation",
      "base": "base",
      "affiliation": "affiliation",
      "relatives": "relatives",
      "publisher": "publisher",
      "alignment": "alignment"
   }
   

   return render_template('profile.html', hero=hero, attr=attr)


@app.route('/contribute/<int:id>/<string:attr>', methods=["GET", "POST"])
def contribute_form(id, attr):
   """Shows contribute form to contribute to missing information"""

   if not g.user:
      flash(f"Access unauthorized", "danger")
      return redirect('/')


   form = ContributeForm()

   if form.validate_on_submit():

      contribution = Contribute(value = form.value.data, url=form.resource.data, user_id=g.user.id)

      db.session.add(contribution)
      db.session.commit()
      flash(f"Thank you!, your contribution is under review. If accepted, we'll update the missing information and credit you with the help!", "success")
      return redirect('/')
   
   hero = Hero.query.get(id)
   attr = {
      "name": "name",
      "full name": "full name",
      "gender": "gender",
      "race": "race",
      "height": "height",
      "weight": "weight",
      "eye color": "eye color",
      "hair color": "hair color",
      "alter egos": "alter egos",
      "aliases": "aliases",
      "birthplace": "birthplace",
      "first appearance": "first appearance",
      "intelligence": "intelligence",
      "strength": "strength",
      "speed": "speed",
      "durability": "durability",
      "power": "power",
      "combat": "combat",
      "occupation": "occupation",
      "base": "base",
      "affiliation": "affiliation",
      "relatives": "relatives",
      "publisher": "publisher",
      "alignment": "alignment"
   }
   
   

   return render_template('contribute.html', hero=hero, form=form, attr=attr)

@app.route('/search', methods=["GET", "POST"])
def search_results():
   """Searches for heroes"""

   hero = request.form.get('hero')
   if hero == "":
      flash(f"Uhh, sorry but I need a name!", "error")
      return redirect('/search')

   heroes = Hero.query.filter(Hero.name.ilike(f'%{hero}%'))

   # :
   #    flash(f"No results found. Try again!", "warning")  
   return render_template('search-results.html', heroes=heroes, hero=hero)





@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    do_logout()
    
    flash(f"Goodbye, you've successfully logged out", "success")
    return redirect("/")
