# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:44:10 2019

@author: romain
"""

import pandas as pd
import geopandas as gpd

df = pd.read_csv('paris_rpls_2017.csv', sep=',', header='infer',
                 usecols=['longitude',
                          'latitude'])

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
gdf.drop(columns=['longitude','latitude'], inplace=True)
gdf.to_file("rpls.geojson", driver='GeoJSON')