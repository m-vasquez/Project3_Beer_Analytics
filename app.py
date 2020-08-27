import warnings
warnings.filterwarnings('ignore')

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct, desc
import os
from config import pw


from flask import Flask, jsonify, render_template, request

# Flask Setup

app = Flask(__name__)

# Database Setup

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or f"postgresql://postgres:{pw}@localhost:5432/beer_db"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# reflect db and save references to the table
base = automap_base()
base.prepare(db.engine, reflect=True)
print(base.classes.keys())
for table in base.classes:
    print(table)

Beer_Data = base.classes.beerdata 
Location_Data = base.classes.locationdata 

# set up home route and page routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/beerdata")
def county():
    return render_template("beer.html")

@app.route("/locationdata")
def state():
    return render_template("location.html")

# pull in beer data 
@app.route("/api/beerdata")
def get_data():

    beer_results = db.session.query(Beer_Data).all()
    beer_data = {}
    for entry in beer_results:
        beer_data[entry.beer_name] = {
            # "beer_name": entry.beer_name,
            "style": entry.beer_style,
            "group": float(entry.cluster_group),
            "abv": entry.beer_abv,
            "overall": float(entry.overall_review),
            "aroma": float(entry.aroma_review),
            "appearance": float(entry.appearance_review),
            "palate": float(entry.palate_review),
            "taste": float(entry.taste_review)
        }  
    return jsonify(beer_data)

# # dict in order by pk id
# @app.route("/api/beerdata")
# def get_data():

#     beer_results = db.session.query(Beer_Data).all()
#     beer_data = []
#     for entry in beer_results:
#        beer_dict = {}
#        beer_dict["beer_name"] = entry.beer_name
#        beer_dict["style"] = entry.beer_style
#        beer_dict["group"] = float(entry.cluster_group)
#        beer_dict["abv"] = entry.beer_abv
#        beer_dict["overall"] = float(entry.overall_review)
#        beer_dict["aroma"] = float(entry.aroma_review)
#        beer_dict["appearance"] = float(entry.appearance_review)
#        beer_dict["palate"] = float(entry.palate_review)
#        beer_dict["taste"] = float(entry.taste_review)

#        beer_data.append(beer_dict)
       
#     return jsonify(beer_data)
    
# pull in brewery location data for map and charts etc.
@app.route("/api/locationdata")
def get_location():

    location_results = db.session.query(Beer_Data, Location_Data).filter(Beer_Data.brewery_name == Location_Data.brewery_name).all()
    location_data = {}
    for bd, ld in location_results:
        location_data[bd.brewery_name] = {
            # "brewery_name": bd.brewery_name,
            "city": ld.City,
            "state": ld.State,
            "lat": float(ld.Latitude),
            "lng": float(ld.Longitude),
            "style": bd.beer_style,
            "group": float(bd.cluster_group),
            "abv": bd.beer_abv,
            "overall": float(bd.overall_review),
            "aroma": float(bd.aroma_review),
            "appearance": float(bd.appearance_review),
            "palate": float(bd.palate_review),
            "taste": float(bd.taste_review)
        }  
    return jsonify(location_data)
    

if __name__== "__main__":
    app.run(debug=True)
