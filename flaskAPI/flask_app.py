from flask import Flask, jsonify
import numpy as np
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



# Database Setup
#####################################################
engine = create_engine("sqlite:///../data/reduced_data.sqlite", echo=False)

#reflect database to new model and table
Base= automap_base()
#tables
Base.prepare(autoload_with=engine)

#save references to table
reduced_data= Base.classes.reduced_data

#Create session link from python to the DB
session= Session(engine)

#Flask Setup
#####################################################

app = Flask(__name__)

#####################################################
#Flask Routes
#####################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Electric Charge Station Finder Tool Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/chargers_by_city/<town><br/>"
        f"/api/v1.0/chargers_by_state/<state>"
    )
#Query results

@app.route("/api/v1.0/chargers_by_city/<town>")
def chargers_by_city(town):
    results = session.query(reduced_data.Title,
                              reduced_data.AddressLine1,
                              reduced_data.Town,
                              reduced_data.StateOrProvince,
                              reduced_data.Postcode,
                              reduced_data.Latitude,
                              reduced_data.Longitude,
                              reduced_data.ConnectionTypeIDs).filter(reduced_data.Town == town).all()
    #session.close()

    #Dictionary first API
    address_list = []
    for results in results:
        address = {
            "Location Name": results.Title,
            "Address": results.AddressLine1,
            "Town": results.Town,
            "State": results.StateOrProvince,
            "Zip Code": results.Postcode,
            "Latitude": results.Latitude,
            "Longitude": results.Longitude,
            "ConnectionType": results.ConnectionTypeIDs
        }
        address_list.append(address)
    #Return JSON
    return jsonify(address_list)




######################################################

if __name__ == "__main__":
    app.run(debug=True)

session.close()
