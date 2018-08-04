
from flask import (
    jsonify,
    render_template,
)
from sqlalchemy import desc
from datetime import datetime
from dateutil.relativedelta import relativedelta
from surfpy import app, Measurements, Stations, session
from surfpy.src import (
    query_prcps,
    query_tobs,
    query_prcp_stats,
    query_top_stats,
    to_dict)


# home route
# @app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/v1.0/pobs")
def prcps():
    days_before = 0
    years_before = 1
    months_before = 0
    # get the most recent measurements acquired
    end_date = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    start_date = end_date - relativedelta(years=years_before, months=months_before, days=days_before)
    d = query_prcps(session, start_date, end_date)
    return jsonify(d)


@app.route("/api/v1.0/tobs")
def tobs():

    days_before = 0
    years_before = 1
    months_before = 0
    # get the most recent measurements acquired
    end_date = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    start_date = end_date - relativedelta(years=years_before, months=months_before, days=days_before)
    d = query_tobs(session, start_date, end_date)
    return jsonify(d)


@app.route("/api/v1.0/stations")
def stations():

    keys = ["station_id", "station", "name", "longitude", "latitude", "elevation"]
    query = session.query(Stations).distinct()

    d = to_dict(query, keys=keys)
    return jsonify(d)


@app.route("/api/v1.0/normals/tobs/<start>")
def tobs_stat_start(start):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    d = query_top_stats(session, start, end)
    return jsonify(d)


@app.route("/api/v1.0/normals/tobs/<start>/<end>")
def tobs_stat_between(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    d = query_top_stats(session, start, end)
    return jsonify(d)


@app.route("/api/v1.0/stats/pobs/<start>")
def prcp_stat_start(start):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = session.query(Measurements.date).order_by(desc(Measurements.date)).first()[0]
    d = query_prcp_stats(session, start, end)
    return jsonify(d)


@app.route("/api/v1.0/stats/pobs/<start>/<end>")
def prcp_stat_between(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    d = query_prcp_stats(session, start, end)
    return jsonify(d)


