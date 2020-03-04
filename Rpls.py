import pandas as pd
import re
import numpy as np
class Rpls(pd.DataFrame): 
        """ Classe modélisant la base de donnée des logements sociaux parisiens.
         c'est une extension de la classe DataFrame de la bibliothèque Pandas. 

        """
        def __init__(self,data):
            """ Initialise un objet Rpls comme un dataframe en extrayant les informations d'un csv.
            Parameters:
            data : une adresse menant au csv contenant les informations sur le rpls parisien que l'utilisateur souhaite exploiter.        
            """
            super(Rpls, self).__init__(
                pd.read_csv(data, sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'}))
    
        def converter_cp(self,string):
            try:
                return int(string)
            except:
                return 0   
        
        def converter_etage(self,string):
            try: 
                return float(string)
            except:
                if string == 'RC':
                    return 0.0
                match_temp = re.search(r"[1-9][0-9]*", string)
                if match_temp != None:
                    return float(match_temp.group())
                else:
                    return np.nan

        #renvoie les coordonnées du rpls
        def coordonnee(self,id):
            return 0
        
        #renvoie la surface indiquée dans les données si présente.
        def surface(self,id):
            return 0
        
        #renvoie le nombre de piece du logement social concerné
        def nbpiece(self,id):
            return 0
        #renvoie l'arrondissement du logement social concerné
        def arrondissement(self,id):
            return 0
        #renvoie l'étage du logement social concerné
        def etage(self,id):
            return 0
        #renvoie l'adresse du logement social concerné
        def adresse(self,id):
            return 0
    