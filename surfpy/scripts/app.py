# import dependencies
import os, sys, inspect
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify

# sqlalchemy dependecies
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy.sql import label


CURR_FILE = inspect.getabsfile(inspect.currentframe())
CURR_DIR = os.path.dirname(CURR_FILE)
ROOT_DIR = os.path.dirname(CURR_DIR)

# create sqlite engine
filename = os.path.join(ROOT_DIR, "data", "int", "hawaii.sqlite")
engine = create_engine(f"sqlite:///{filename}")

# reflect the database
Base = automap_base()
Base.prepare(engine=engine, reflect=True)

# dave references to each tables
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# create session
session = Session(bind=engine)

# set up flask
app = Flask(__name__)

# home route
@app.route("/")
def home():
    return ("Hawaii Weather Data API<br/>"
            "/api/v1.0/precipitation<br/>"
            "/api/v1.0/stations<br/>"
            "/api/v1.0/tobs<br/>"
            "/api/v1.0/stats/prcp/yyyy-mm-dd/<br/>"
            "/api/v1.0/stats/prcp/yyyy-mm-dd/yyyy-mm-dd<br/>"
            "/api/v1.0/stats/tobs/yyyy-mm-dd/<br/>"
            "/api/v1.0/stats/tobs/yyyy-mm-dd/yyyy-mm-dd")


@app.route("/api/v1.0/precipitation")
def prcps():

    days_before = 0
    years_before = 1
    months_before = 0
    # get the most recent measurements acquired
    end_date = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    start_date = end_date - relativedelta(years=years_before, months=months_before, days=days_before)
    d = query_prcps(start_date, end_date)
    return jsonify(d)


@app.route("/api/v1.0/tobs")
def tobs():

    days_before = 0
    years_before = 1
    months_before = 0
    # get the most recent measurements acquired
    end_date = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    start_date = end_date - relativedelta(years=years_before, months=months_before, days=days_before)
    d = query_tobs(start_date, end_date)
    return jsonify(d)


@app.route("/api/v1.0/stations")
def stations():

    keys = ["station_id", "station", "name", "longitude", "latitude", "elevation"]
    query = session.query(Stations).distinct()

    d = to_dict(query, keys=keys)
    return jsonify(d)


@app.route("/api/v1.0/stats/tobs/<start>")
def tobs_stat_start(start):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    d = query_top_stats(start, end)
    return jsonify(d)


@app.route("/api/v1.0/stats/tobs/<start>/<end>")
def tobs_stat_between(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    d = query_top_stats(start, end)
    return jsonify(d)


@app.route("/api/v1.0/stats/prcp/<start>")
def prcp_stat_start(start):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    d = query_prcp_stats(start, end)
    return jsonify(d)


@app.route("/api/v1.0/stats/prcp/<start>/<end>")
def prcp_stat_between(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    d = query_prcp_stats(start, end)
    return jsonify(d)


def query_tobs(start, end):
    stations = session.query(Measurements.station).filter(
        Measurements.date.between(start, end)).distinct().all()

    # query between start and end dates
    d_stations = dict()
    for station in stations:
        station = station[0]
        query = session.query(Measurements).filter(
            Measurements.date.between(start, end), Measurements.station == station)
        query = query.order_by(desc("date"))
        d_station = dict()
        for elem in query.all():
            d_station.update({elem.date.strftime("%Y-%m-%d"): elem.tobs})
        d_stations.update({station: d_station})

    return d_stations


def query_prcps(start, end):
    stations = session.query(Measurements.station).filter(
        Measurements.date.between(start, end)).distinct().all()

    # query between start and end dates
    d_stations = dict()
    for station in stations:
        station = station[0]
        query = session.query(Measurements).filter(
            Measurements.date.between(start, end), Measurements.station == station)
        query = query.order_by(desc("date"))
        d_station = dict()
        for elem in query.all():
            d_station.update({elem.date.strftime("%Y-%m-%d"): elem.prcp})
        d_stations.update({station: d_station})

    return d_stations


def query_prcp_stats(start, end):

    stations = session.query(Measurements.station).filter(
        Measurements.date.between(start, end)).distinct().all()

    # query between start and end dates
    d_stations = dict()
    for station in stations:
        station = station[0]
        sel = [label("minprcp", func.min(Measurements.prcp)),
               label("avgprcp", func.avg(Measurements.prcp)),
               label("maxprcp", func.max(Measurements.prcp))]

        query = session.query(*sel).filter(
            Measurements.date.between(start, end), Measurements.station == station)
        d_station = dict()
        for elem in query.all():
            d_station.update({"minprcp": elem.minprcp,
                              "avgprcp": elem.avgprcp,
                              "maxprcp": elem.maxprcp})
        d_stations.update({station: d_station})

    return d_stations


def query_top_stats(start, end):

    stations = session.query(Measurements.station).filter(
        Measurements.date.between(start, end)).distinct().all()

    # query between start and end dates
    d_stations = dict()
    for station in stations:
        station = station[0]
        sel = [label("mintob", func.min(Measurements.tobs)),
               label("avgtob", func.avg(Measurements.tobs)),
               label("maxtob", func.max(Measurements.tobs))]

        query = session.query(*sel).filter(
            Measurements.date.between(start, end), Measurements.station == station)
        d_station = dict()
        for elem in query.all():
            d_station.update({"mintob": elem.mintob,
                              "avgtob": elem.avgtob,
                              "maxtob": elem.maxtob})
        d_stations.update({station: d_station})

    return d_stations


def to_dict(query, keys):

    if hasattr(query, "__iter__"):
        d = []
        for elem in query:
            d.append({k: elem.__dict__[k] for k in keys})
    else:
        d = {k: query.__dict__[k] for k in keys}
    return d


if __name__ == "__main__":
    app.run(debug=True)
