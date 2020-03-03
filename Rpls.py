import pandas as pd
class Rpls(pd.DataFrame): 
      """ Classe modélisant la base de donnée des logements sociaux parisiens.
         c'est une extension de la classe DataFrame de la bibliothèque Pandas. 

    """
    
    def __init__(self,data):
         """ Initialise un objet Rpls comme un dataframe en extrayant les informations d'un csv.
        
        Parameters:
            data : une adresse menant au csv contenant les informations sur le rpls parisien que l'utilisateur souhaite exploiter.
                  
        """
        data_rpls = pd.read_csv(data sep=',',error_bad_lines=False, 
                                header='infer', index_col=0,
                                converters={'codepostal':self.converter_cp
                                            , 'etage':self.converter_etage},
                                dtype={'longitude':'float', 'latitude':'float'})
        self = data_rpls
    
    @property
    def _constructor(self):
        return Rpls
    
    
    #renvoie les coordonnées du rpls
    def coordonnee(id):
    
    #renvoie la surface indiquée dans les données si présente.
    def surface(id):
    
    #renvoie le nombre de piece du logement social concerné
    def nbpiece(id):
    
    #renvoie l'arrondissement du logement social concerné
    def arrondissement(id):

    #renvoie l'étage du logement social concerné
    def etage(id):
    
    #renvoie l'adresse du logement social concerné
    def adresse(id):

    