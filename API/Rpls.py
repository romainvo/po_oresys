import pandas as pd
class Rpls(pd.DataFrame): 
    def __init__(self,data):
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
    def get_coordonnee(id)
    
    #renvoie la surface indiquée dans les données si présente.
    def get_surface(id):
    
    def get_nbpiece(id):
    
    def get_adresse(id):

    def get_