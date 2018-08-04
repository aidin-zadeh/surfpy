# import dependencies
import os, sys, inspect
from flask import Flask

# sqlalchemy dependecies
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session



CURR_FILE = inspect.getabsfile(inspect.currentframe())
CURR_DIR = os.path.dirname(CURR_FILE)
ROOT_DIR = os.path.dirname(CURR_DIR)

# create sqlite engine
filename = os.path.join(CURR_DIR, "data", "int", "hawaii.sqlite")
print(filename)
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

from surfpy import views
