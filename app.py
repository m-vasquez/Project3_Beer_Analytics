import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct, desc
import os
import itertools
from operator import itemgetter
from config import pw
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# import joblib

# model = joblib.load("beer_data_model.joblib")

# Flask Setup

app = Flask(__name__)

# Database Setup

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', '') or f"postgresql://postgres:{pw}@localhost:5432/beer_db"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# reflect db and save references to the table
Base = automap_base()
Base.prepare(db.engine, reflect=True)
print(Base.classes.keys())

# print(base.classes)
# for table in Base.classes:
#     print(table)

Beer_Data = Base.classes.beerdata
Location_Data = Base.classes.locationdata

# # set up home route and page routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/beerdata") 
def beerdata():
    return render_template("beer.html") # charts to go here

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/scatter")
def scatter():
    return render_template("3Dscatter.html")

# # pull in beer data
@app.route("/api/beerdata")
def get_data():

    beer_results = db.session.query(Beer_Data).all()
    beer_data = []
    for entry in beer_results:
        beer_dict = {}
        beer_dict["name"] = entry.beer_name
        beer_dict["style"] = entry.beer_style
        beer_dict["abv"] = entry.beer_abv
        beer_dict["brewery_name"] = entry.brewery_name
        beer_dict["overall_review"] = round(entry.overall_review,2)
        beer_dict["aroma_review"] = round(entry.aroma_review,2)
        beer_dict["appearance_review"] = round(entry.taste_review,2)
        beer_dict["taste_review"] = round(entry.appearance_review,2)
        beer_dict["palate_review"] = round(entry.palate_review,2)
        beer_dict["cluster"] = entry.cluster_group
        
        beer_data.append(beer_dict)

    return jsonify(beer_data)

# # # pull in brewery location data for map and charts etc.
@app.route("/api/locationdata")
def get_location():

    location_results = db.session.query(Beer_Data, Location_Data).filter(Beer_Data.brewery_name == Location_Data.brewery_name).distinct()
    location_data = {}
    for bd, ld in location_results:
        brew_dict={
            "beers":[],
            "brewery_name": bd.brewery_name,
            "city": ld.City,
            "country":ld.Country,
            "state": ld.State,
            "lat": float(ld.Latitude),
            "lng": float(ld.Longitude)   
        }  
        beers={ "beer_name":bd.beer_name,
            "style": bd.beer_style,
            "abv": bd.beer_abv,
            "aroma": float(bd.aroma_review),
            "appearance": float(bd.appearance_review),
            "palate": float(bd.palate_review),
            "taste": float(bd.taste_review),
            "group": float(bd.cluster_group)
            }
        
        if bd.brewery_name not in location_data:
            location_data[bd.brewery_name] = brew_dict
            location_data[bd.brewery_name]["beers"].append(beers)
        else:
            location_data[bd.brewery_name]["beers"].append(beers)
            
    return jsonify(location_data)




if __name__ == "__main__":
    app.run(debug=True)
