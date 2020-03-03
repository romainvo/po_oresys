import pandas as pd

@pd.api.extensions.register_dataframe_accessor("bnb")
class GeoAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        # verify there is a column latitude and a column longitude
        if 'latitude' not in obj.columns or 'longitude' not in obj.columns:
            raise AttributeError("Must have 'latitude' and 'longitude'.")

    def complete_description(self, id : int):
        
        columns = ['name', 'summary', 'space', 'description']
        print("Champs affichés :", " ")
        for elt in columns:
            print(", ", elt)
            
        return self._obj.loc[id, columns]  

    @property
    def center(self):
        # return the geographic center point of this DataFrame
        lat = self._obj.latitude
        lon = self._obj.longitude
        return (float(lon.mean()), float(lat.mean()))

    def plot(self):
        # plot this array's data on a map, e.g., using Cartopy
        pass

class Airbnb(pd.DataFrame): 
    """ Classe modélisant l'ensemble des annonces airbnb. Hérite de la classe
    DataFrame de pandas.
    
    Attributes:
        nb_jobs (int): Nombre de jobs dans le problème.

        nb_machines (int): Nombre de machine dans le problème.

        l_job (list<Job>): Liste contenant les objets Job.

    """
    
    def __init__(self, *args, **kwargs):
        """ Initialise un objet Airbnb.
        
        Parameters:
            flowshop (Flowshop): Instance d'un problème de flowshop de permutation

            piste (Piste): Instance d'une piste, aggrège les principales caractéristiques
            de la piste parcourue par les fourmis.
            
        Keyword arguments:
            nb_jobs (int): Nombre de jobs dans le problème.

            nb_machines (int): Nombre de machine dans le problème.

            l_job (list<Job>): Liste contenant les objets Job.
                        
        """
        
        super(Airbnb, self).__init__(
                pd.read_csv("csv/airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'}))
    
        self.index.rename('id_bnb', inplace=True)       
    
    
#    @property
#    def _constructor(self):
#        return Airbnb
    
    #renvoie l'ensemble des descriptions textuelles du logement airbnb
    def complete_description(self, id : int):
        
        columns = ['name', 'summary', 'space', 'description']
        print("Champs affichés :", " ")
        for elt in columns:
            print(", ", elt)
            
        return self.loc[id, columns]
    
#    #renvoie les coordonnées du airbnb
#    def coordonnee(id):
#
#    #renvoie le nom de l'annonce si présent
#    def name(id):
#    
#    #renvoie le sommaire de l'annonce si présent
#    def summary(id):
#    
#    #renvoie la description de l'annonce si présente
#    def description(id):
#    
#    #renvoie la surface indiquée dans les données si présente.
#    def surface(id):
#    
#    #extraction de l'étage dans la description du airbnb id
#    def extraire_etage(id):
#    
#    #extraction de l'étage dans la description du airbnb id
#    def extraire_surface(id):
#    
#    #extraction de l'étage dans la description du airbnb id
#    def extraire_nb_piece(id):
        
if __name__ == '__main__':

    data_airbnb = pd.read_csv("csv/airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})