import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt/&lt;end&gt"
    )

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > "2016-08-23").all()
    
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict[measurement.date] = measurement.tobs
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

#Stations
@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).filter(Measurement.date > "2016-08-23").all()

    return jsonify(results)
#tobs
@app.route("/api/v1.0/tobs")
def tobs():

    results = session.query(Measurement.tobs).all()
    
    return jsonify(results)
#start
@app.route("/api/v1.0/<start>/")
def starty(start):

    
    results = session.query(func.max(Measurement.tobs), 
                             func.min(Measurement.tobs), 
                             func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    summary = []
    for result in results:
        max_dict={}
        max_dict['Max Temp']=result[0]
        min_dict={}
        min_dict['Min Temp']=result[1]
        avg_dict={}
        avg_dict['Avg Temp']=result[2]
        summary.append(max_dict)
        summary.append(min_dict)
        summary.append(avg_dict)
        
    return jsonify(summary)

#end
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):

    
    results = session.query(func.max(Measurement.tobs), 
                             func.min(Measurement.tobs), 
                             func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()

    summary = []
    for result in results:
        max_dict={}
        max_dict['Max Temp']=result[0]
        min_dict={}
        min_dict['Min Temp']=result[1]
        avg_dict={}
        avg_dict['Avg Temp']=result[2]
        summary.append(max_dict)
        summary.append(min_dict)
        summary.append(avg_dict)
        
    return jsonify(summary)


if __name__ == '__main__':
    app.run(debug=True)