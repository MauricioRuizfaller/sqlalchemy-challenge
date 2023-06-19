from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, Date
import datetime as dt


app = Flask(__name__)
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(autoload_with=engine)
Base.classes.keys()
Station = Base.classes.station
Measurement = Base.classes.measurement


@app.route("/")
def home():
    return (
        "Welcome to the Climate App API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/tstats/&lt;start&gt;<br/>"
        "/api/v1.0/tstats/&lt;start&gt;/&lt;end&gt;<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.date.fromisoformat(most_recent_date) - dt.timedelta(days=365)
    raw_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= one_year_ago).group_by(Measurement.date).all()
    results = dict(raw_results)
    session.close()
    return jsonify(results)


#  def stations():
#     session = Session(engine)

#     results = session.query(Station.station).all()

#     session.close()

#     station_list = [station[0] for station in results]

#     return jsonify(station_list)


@app.route("/api/v1.0/tstats/<start>")
@app.route("/api/v1.0/tstats/<start>/<end>")
def tstats(start, end=None):
    if not end:
        end = dt.date.max
    session = Session(engine)
    temperatura_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .first()
    temp_results = list(temperatura_stats)
    session.close()
    return jsonify(temp_results)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
