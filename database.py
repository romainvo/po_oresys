from flask_sqlalchemy import SQLAlchemy
from main import app
from sqlalchemy import Table, Column, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Airbnb(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)