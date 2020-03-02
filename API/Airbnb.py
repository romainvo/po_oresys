import pandas as pd
class Airbnb(pd.DataFrame): 
     def __init__(self,data):
        data_airbnb = pd.read_csv(data, sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
        self.data_airbnb.loc[:, 'id_bnb'] = self.data_airbnb.index.astype(int)
        self =  data_airbnb.copy(deep=True)


    @property
    def _constructor(self):
        return Airbnb
    #renvoie l'ensemble des descriptions textuelles du logement airbnb
    def get_complete_description(id):
    
    #renvoie les coordonnées du airbnb
    def get_coordonnee(id)

    #renvoie le nom de l'annonce si présent
    def get_name(id):
    
    #renvoie le sommaire de l'annonce si présent
    def get_summary(id):
    
    #renvoie la description de l'annonce si présente
    def get_description(id):
    
    #renvoie la surface indiquée dans les données si présente.
    def get_surface(id):
    
    #extraction de l'étage dans la description du airbnb id
    def extraire_etage(id):
    
    #extraction de l'étage dans la description du airbnb id
    def extraire_surface(id):
    
    #extraction de l'étage dans la description du airbnb id
    def extraire_nb_piece(id):

