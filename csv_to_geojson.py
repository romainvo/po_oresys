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
    keep_columns = ['id_bnb']
    for i in range(100):
        keep_columns.append('id_rpls{}'.format(i))
        keep_columns.append('score{}'.format(i))
    dtype = {key:'int64' for key in keep_columns}
    
    df_results = pd.read_csv('results_rd150_nb100_score.csv', header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb')
    
    df_results.index.rename('id_bnb', inplace=True)

    df_bnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                        usecols=['latitude','longitude'],
                        dtype={'longitude':'float', 'latitude':'float'})

    # On crée des colonnes de booléens pour la condition score > seuil
    seuil = 4
    condition_colonne = df_results['score0'] > seuil
    df_results.loc[:,'seuil0'] = condition_colonne
    for i in range(1,100):
        colonne_inter = df_results['score'+str(i)] > seuil
        df_results.loc[:, 'seuil'+str(i)] = condition_colonne
        condition_colonne = condition_colonne + colonne_inter

    df_results = pd.concat([df_results,df_bnb], ignore_index=False, sort=False, axis=1)
    df_results.loc[:, 'seuil_total'] = condition_colonne
    print(df_results.shape)
#    df_results = df_results.loc[df_results.seuil_total]  
#    print(df_results.shape)

    # On identifie et stocke les id_rpls pour lesquels le score est supérieur au seuil
    id_sup_seuil = []
    for i in range(100):
        id_sup_seuil.append(
                df_results.loc[
                        df_results.loc[:,'seuil{}'.format(i)]
                        ,'id_rpls{}'.format(i)
                        ].reindex(index=range(df_results.shape[0])))
   
    df_results = df_results.loc[:,['latitude','longitude']]

    for i in range(100):
        df_results = pd.concat([df_results,id_sup_seuil[i]], ignore_index=False
                               , sort=False, axis=1)

    df_results = df_results.loc[df_results.isna().sum(axis=1) != 100]
    print(df_results.head())
    print(df_results.shape)
    
    gdf = gpd.GeoDataFrame(df_results, geometry=gpd.points_from_xy(df_results.longitude, df_results.latitude))
    gdf.drop(columns=['longitude','latitude'], inplace=True)

    gdf.to_file("static/donneesgeos/croisementBis.geojson", driver='GeoJSON')

#-----------------------------------------------------------------------------#
#---------------------------- Création coord_rpls --------------------------- #
#-----------------------------------------------------------------------------#
"""
df = pd.read_csv('paris_rpls_2017.csv', sep=',', header='infer',
                      usecols=['longitude','latitude'])

df.to_json('static/donneesgeos/coord_rpls.json')
"""

                       


