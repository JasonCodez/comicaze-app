import requests
from app import BASE_URL
from models import Hero, db
from app import app




# Create all tables


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