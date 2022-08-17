# import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# import SQLalchemy dependencies
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import flask dependencies and jsonify ( a flask.json module)
from flask import Flask, jsonify

# create a database engine to be used for flask application. 
engine = create_engine("sqlite:///hawaii.sqlite") # gives access to the sqlite database

# reflect the database into class Base
Base = automap_base()

Base.prepare(engine, reflect = True) # each viable Table within the MetaData will get a new mapped class generated automatically

# create a variable for each class (table in database)
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a flask application by defining it
app = Flask(__name__)

# create route
@app.route("/")


# create a function for the welcome page of the website with references to other routes
def welcome():

    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''')
# /api/v1.0/ followed by the name of the route is a convention that signifies that this is version 1 of our application. 

# create a route for the precipitation 
@app.route("/api/v1.0/precipitation")

# create a new function to query precipitation statistics for each date in prev_year
# note: .\ is used to signify that the query goes on to the next line
def precipitation():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    session.close()
    # this will return a list of tuples. Tuples contain two indexes: tuple[0] contains date and tuple[1] contains precipitation amount 
    precip = {date:prcp for date,prcp in precipitation}
    return jsonify(precip)

# create a route for the station
@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    #unravel results into a one-dimensional array using the numpy function np.ravel()
    stations = list(np.ravel(results))
    # to return our list as JSON, we need to add stations=stations. This is a convention that formats our list into JSON.
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps = temps)

# create route for a summary statistics report 
@app.route("/api/v1.0/temp/<start>")

# this route is different from the previous ones in that we will have to provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats
def stats(start = None, end = None):
    session = Session(engine)
# create a query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # create an if-not statement to query our database using the list that we just made. 
    # Then unravel the results into a one-dimensional array and convert them to a list. 
    # Finally, we will jsonify our results and return them.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps = temps)
    session = Session(engine)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps = temps)  

# using this if statement along with running a new terminal (right-click VS Code and copy and paste URL into browser)

# terminal must be closed for each instance 
if __name__ == '__main__':
    app.run()

# For each function create a new session and close it so that an internal server error does not occur