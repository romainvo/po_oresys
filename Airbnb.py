import pandas as pd

class Airbnb(pd.DataFrame): 
    """ Classe modélisant un problème de flowshop de permutation. 
    
    Attributes:
        nb_jobs (int): Nombre de jobs dans le problème.

        nb_machines (int): Nombre de machine dans le problème.

        l_job (list<Job>): Liste contenant les objets Job.

    """
    
    def __init__(self, *args, **kwargs):
        """ Initialise un objet Fourmi.
        
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
#    def complete_description(id):
#    
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