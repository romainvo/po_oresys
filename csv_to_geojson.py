# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:44:10 2019

@author: romain
"""

import pandas as pd
import geopandas as gpd

if __name__ == '__main__':

#    df = pd.read_csv('paris_rpls_2017.csv', sep=',', header='infer',
#                    usecols=['longitude','latitude'])
#
#    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
#    gdf.drop(columns=['longitude','latitude'], inplace=True)
#    gdf.to_file("static/donneesgeos/rpls.geojson", driver='GeoJSON')

#    df = pd.read_csv("airbnb.csv", sep=',', header='infer',
#                          usecols=['latitude','longitude'],
#                          dtype={'longitude':'float', 'latitude':'float'})
#    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
#    gdf.drop(columns=['longitude','latitude'], inplace=True)
#    gdf.to_file("static/donneesgeos/airbnb.geojson", driver='GeoJSON')
    
#    results = pd.read_csv('results.csv', header='infer', index_col='id_bnb',
#                          dtype={'id_rpls':'int', 'distance':'float'})
    
#    results = results.loc[results.distance < 5]
#    gdf = gpd.GeoDataFrame(results)
    