import pandas as pd
# importation des données, pour l'instant sans nettoyage préalable : on se contente d'ignorer les lignes ayant le mauvais format.
dataRPLS=pd.read_csv("RPLS2018.csv",sep=';',error_bad_lines=False)
dataAirbnb=pd.read_csv("airbnb.csv")
# On s'interesse uniquement aux données de latitude et longitude des différentes annonces airbnb.
dfLocalisationAirbnb=dataAirbnb[['id','latitude','longitude']]
#On cherche à obtenir une adresse en un string via le RPLS
Adresses=dataRPLS['NUMVOIE'].fillna("")+" "+dataRPLS['TYPVOIE'].fillna("")+" "+dataRPLS['NOMVOIE'].fillna("")+" "+dataRPLS['COMPLGEO'].fillna("")
print(Adresses)
