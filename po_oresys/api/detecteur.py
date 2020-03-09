import pandas as pd
import numpy as np
import re
from po_oresys.api.comparateur import Comparateur
import po_oresys.api.decorators

class detecteur:
    
    def __init__(self , airbnb=None, rpls=None, croisement=None,score=None):
        
        if airbnb is None:
            self.airbnb = self.import_data_airbnb()
        else:
            self._validate_airbnb(airbnb)
            self.airbnb = airbnb
    
        if rpls is None:
            self.rpls = self.import_data_rpls()
        else:
            self._validate_rpls(rpls)
            self.rpls = self.import_data_rpls()
            
        if croisement is None:
            self.croisement = self.import_croisement()
        else:
            self._validate_croisement(croisement)
            self.croisement = croisement
            
        self.comparateur = Comparateur(self.airbnb, self.rpls, self.croisement
                 , poids_sous_scores={'croisement':0.2, 'surfhab':0.3
                                      , 'etage':0.3, 'nbpiece':0.2}
                 , surfhab_tokens=None, etage_tokens=None, nbpiece_tokens=None
                 , all_scores=None)

    @staticmethod
    def _validate_airbnb(obj : pd.DataFrame):
        """ Vérifie si la DataFrame regroupe bien un ensemble d'annonces airbnb,
        utilisé au moment de "l'instanciation" du décorateur.
        
        Parameters:
            _obj (pd.DataFrame): DataFrame regroupant l'ensemble des annonces
            airbnb.
        
        Raise:
            AttributeError: si le format n'est pas respecté
        """     

        columns = {'name','summary','space','description','longitude','latitude'}
        if not columns.issubset(set(obj.columns)):
            raise AttributeError("Must have {}".format(list(columns)))

    @staticmethod
    def _validate_rpls(obj : pd.DataFrame):
        """ Vérifie si la DataFrame regroupe bien un ensemble de logements 
        sociaux. Utilisé au moment de "l'instanciation" du décorateur.
        
        Parameters:
            obj (pd.DataFrame): DataFrame regroupant l'ensemble des logements
            sociaux.
        
        Raise:
            AttributeError: si le format n'est pas respecté
        """     

        columns = {'libcom','numvoie','typvoie','nomvoie','surfhab', 'etage'
                   ,'nbpiece' ,'longitude','latitude'}
        if not columns.issubset(set(obj.columns)):
            raise AttributeError("Must have {}".format(list(columns)))

    def _validate_croisement(self, obj : pd.DataFrame):
        if not self.airbnb.index.equals(obj.index):
            raise ValueError("'croisement' ne correspond ne croise pas les annonces",
                             "airbnb contenu dans 'self.airbnb'")

    @staticmethod
    def import_data_rpls():
        
        def converter_codepostal(string):
            try:
                return int(string)
            except:
                return 0   
            
        def converter_etage(string):
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
                
        data_rpls = pd.read_csv("po_oresys/csv/paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                        header='infer', index_col=0,
                        converters={'codepostal':converter_codepostal
                                    , 'etage':converter_etage},
                        dtype={'longitude':'float', 'latitude':'float'})
        
        data_rpls.index.rename('id_rpls', inplace=True)

        return data_rpls
    
    @staticmethod
    def import_data_airbnb():
        
        data_airbnb = pd.read_csv("po_oresys/csv/airbnb.csv", sep=',', header='infer',
                              dtype={'longitude':'float', 'latitude':'float'})
        
        data_airbnb.index.rename('id_bnb', inplace=True)
    
        return data_airbnb

    @staticmethod 
    def import_croisement():
        
        keep_columns = ['id_bnb']
        for i in range(250):
            keep_columns.append('id_rpls{}'.format(i))
    #    dtype = {key:'int64' for key in keep_columns}
        
        croisement_v3 = pd.read_csv('po_oresys/csv/results_rd155_nb250.csv', header='infer'
                              , usecols=keep_columns
                              , index_col='id_bnb'
                              , dtype=pd.Int64Dtype()) 
        
        return croisement_v3