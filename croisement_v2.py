import pandas as pd
import geopandas as gpd

def converter_cp(string):
    try:
        return int(string)
    except:
        return 0

# importation des données, pour l'instant sans nettoyage préalable : on se contente d'ignorer les lignes ayant le mauvais format.
reader = pd.read_csv("geo-rpls2017.csv", sep=',',error_bad_lines=False, header='infer',            
                     usecols=['codepostal','numvoie','typvoie','nomvoie'
                              ,'numappt','longitude','latitude','geo_type'
                              ,'geo_adresse'],
                     converters={'codepostal':converter_cp})

data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          usecols=['street','neighbourhood', 'neighbourhood_cleansed'
                                   ,'city','state','zipcode','market'
                                   ,'smart_location', 'country_code', 'country'
                                   ,'latitude','longitude', 'is_location_exact'])

data_rpls = reader.loc[(reader['codepostal'] >= 75000) & (reader['codepostal'] < 76000)]

#data_rpls = reader.get_chunk(100000)

data_rpls.loc[:, 'id_rpls'] = data_rpls.index
data_airbnb.loc[:, 'id_bnb'] = data_airbnb.index

data_rpls.reset_index(drop=True, inplace=True)

merge = pd.concat([data_rpls, data_airbnb])

merge.loc[:,'new_id'] = merge.groupby([merge.latitude.round(4), merge.longitude.round(4)]).ngroup()

merge.sort_values(by='new_id', inplace=True)

#data_rpls = gpd.GeoDataFrame(
#    data_rpls, geometry=gpd.points_from_xy(data_rpls.longitude, data_rpls.latitude))
#
#dataAirbnb = gpd.GeoDataFrame(
#    data_airbnb, geometry=gpd.points_from_xy(data_airbnb.longitude, data_airbnb.latitude))

"""
# On s'interesse uniquement aux données de latitude et longitude des différentes annonces airbnb.
dfLocalisationAirbnb = dataAirbnb.loc[:,['id_bnb','latitude','longitude']]
dfLocalisationRPLS = dataRPLS.loc[:,['id_rpls','latitude','longitude']]

dfLocalisationAirbnb.drop_duplicates(subset=['latitude','longitude'], inplace=True)

dfLocalisationAirbnb.fillna(0.0, inplace=True)
dfLocalisationRPLS.fillna(0.0, inplace=True)

dfLocalisationAirbnb.sort_values(by='latitude', inplace=True)
dfLocalisationRPLS.sort_values(by='latitude', inplace=True)
MergedLat = pd.merge_asof(dfLocalisationAirbnb,dfLocalisationRPLS
                        ,on='latitude',direction='nearest')

dfLocalisationAirbnb.sort_values(by='longitude', inplace=True)
dfLocalisationRPLS.sort_values(by='longitude', inplace=True)
MergedLong = pd.merge_asof(dfLocalisationAirbnb,dfLocalisationRPLS
                        ,on='longitude',direction='nearest')

MergedTotal = MergedLat.merge(MergedLong,how='inner',on=['id_bnb','id_rpls'])
"""