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

#-----------------------------------------------------------------------------#
# Création croisement.geojson avec pour airbnb avec au moins un score > seuil #
#-----------------------------------------------------------------------------#

    df_results = pd.read_csv('results_rd150_nb100.csv', sep=',', header ='infer')

    df_bnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                        usecols=['latitude','longitude'],
                        dtype={'longitude':'float', 'latitude':'float'})

    seuil = 4
    condition_colonne = df_results['score0'] > seuil
    for i in range(1,99):
        colonne_inter = df_results['score'+str(i)] > seuil
        condition_colonne = condition_colonne + colonne_inter

    df_results = pd.concat([df_results,df_bnb], ignore_index=False, sort=False, axis=1)
    df_results.loc[:, 'seuil'] = condition_colonne
    df_results = df_results.loc[df_results.seuil==True]
    df_results = df_results[['latitude','longitude']]
    print(df_results.head())

    gdf = gpd.GeoDataFrame(df_results, geometry=gpd.points_from_xy(df_results.longitude, df_results.latitude))
    gdf.drop(columns=['longitude','latitude'], inplace=True)
    gdf.to_file("static/donneesgeos/croisementBis.geojson", driver='GeoJSON')

                       


