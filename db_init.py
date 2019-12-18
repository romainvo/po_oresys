from database import db, engine, Airbnb
from  sqlalchemy.sql.expression import func
from sqlalchemy import Table, Column, Integer, Float
import csv
import pandas as pd

if __name__ == "__main__":

    db.create_all()

    # Création du dataframe à partir du csv
    airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
        usecols=['id','latitude','longitude'],
        dtype={'longitude':'float', 'latitude':'float'})

    # Alimentation de la table Airbnb via la dataframe
    airbnb.to_sql('Airbnb',
        con = engine,
        if_exists='replace',
        index=False,
        chunksize=100,
        dtype={'id': Integer,
       'longitude': Float,
       'latitude': Float})
