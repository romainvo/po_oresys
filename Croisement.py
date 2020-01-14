import pandas as pd
# importation des données, pour l'instant sans nettoyage préalable : on se contente d'ignorer les lignes ayant le mauvais format.
dataRPLS = pd.read_csv("georpls2017.csv",sep=',',error_bad_lines=False)
dataAirbnb = pd.read_csv("airbnb.csv")
dataRPLS['id'] = dataRPLS.index
# On s'interesse uniquement aux données de latitude et longitude des différentes annonces airbnb.
dfLocalisationAirbnb = dataAirbnb[['latitude','longitude']]
dfLocalisationRPLS = dataRPLS[['latitude','longitude']]

Airbnb_grouped=dfLocalisationAirbnb.drop_duplicates(['latitude','longitude']).fillna(0.0)
RPLS_grouped=dfLocalisationRPLS.drop_duplicates(['latitude','longitude']).fillna(0.0)

Airbnb_grouped['indexAirbnb']=Airbnb_grouped.index
RPLS_grouped['indexRPLS']=RPLS_grouped.index

Airbnb_grouped=Airbnb_grouped.sort_values(['latitude'])
RPLS_grouped=RPLS_grouped.sort_values(['latitude'])

# base de donnée issue de RPLS et airbnb, merged par rapport a la plus proche latitude pour chaque element 
# -> on a acces a un numero d'index airbnb et rpls comme identificateur de l'immeuble (solution provisoire, peut etre utiliser direct les adresses pour RPLS?)
MergedLat=pd.merge_asof(Airbnb_grouped,RPLS_grouped,on='latitude',direction='nearest')

# on merge ensuite par rapport à la longitude.

Airbnb_grouped=Airbnb_grouped.sort_values(['longitude'])
RPLS_grouped=RPLS_grouped.sort_values(['longitude'])

MergedLong=pd.merge_asof(Airbnb_grouped,RPLS_grouped,on='longitude',direction='nearest')

# on créé ensuite l'intersection entre les deux base de donnée merged par rapport aux index : 
# on a donc les index étant à la fois les plus proches en latitude et longitude (1ere approche)

MergedTotal=MergedLat.merge(MergedLong,how='inner',on=['indexAirbnb','indexRPLS'])

print(MergedTotal.head())

# il y en a pas-> 
# pb ou normal car methode trop approximative?  2ème méthode possible : utilier une fonction pour calculer les distances entre les differentes coordonnées.