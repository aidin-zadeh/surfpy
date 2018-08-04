from sqlalchemy import desc, func
from sqlalchemy.sql import label
from surfpy import Measurements


def query_tobs(session: object, start: object, end: object) -> object:
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


def query_prcps(session: object, start: object, end: object) -> object:
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


def query_prcp_stats(session: object, start: object, end: object) -> object:

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


def query_top_stats(session: object, start: object, end: object) -> object:

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


def to_dict(query: object, keys: object) -> object:

    if hasattr(query, "__iter__"):
        d = []
        for elem in query:
            d.append({k: elem.__dict__[k] for k in keys})
    else:
        d = {k: query.__dict__[k] for k in keys}
    return d

