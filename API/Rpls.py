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
            data_rpls = pd.read_csv(data,sep = ',',error_bad_lines=False, 
                                    header='infer', index_col=0,
                                    converters={'codepostal':self.converter_cp
                                                , 'etage':self.converter_etage},
                                    dtype={'longitude':'float', 'latitude':'float'})
            self = data_rpls
    
        @property
        def _constructor(self):
            return Rpls
    
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
        def coordonnee(id):
            return null
        
        #renvoie la surface indiquée dans les données si présente.
        def surface(id):
            return null
        
        #renvoie le nombre de piece du logement social concerné
        def nbpiece(id):
            return null
        #renvoie l'arrondissement du logement social concerné
        def arrondissement(id):
            return null
        #renvoie l'étage du logement social concerné
        def etage(id):
            return null
        #renvoie l'adresse du logement social concerné
        def adresse(id):
            return null
    