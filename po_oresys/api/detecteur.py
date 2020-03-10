import pandas as pd
from po_oresys.api.comparateur import Comparateur
import po_oresys.api.decorators
import po_oresys.api.data_loader as data_loader

class Detecteur:
    
    def __init__(self , airbnb_path=None, rpls_path=None, croisement_path=None
                 , scores_path=None):
        
        self.airbnb = data_loader.import_data_airbnb(airbnb_path)
        self._validate_airbnb(self.airbnb)
    
        self.rpls = data_loader.import_data_rpls(rpls_path)
        self._validate_rpls(self.rpls)
            
        self.croisement = data_loader.import_croisement(croisement_path)
        self._validate_croisement(self.croisement)
        
        self.all_scores = data_loader.import_scores(scores_path)
        self._validate_all_scores(self.all_scores)
            
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
            
    def _validate_all_scores(self, obj : pd.DataFrame):
        if not self.airbnb.index.equals(obj.index):
            raise ValueError("'all_scores' ne correspond ne calcule pas les scores",
                             "des pairs 'AirBnB/logement social' résultat du produit",
                             "cartésien de self.airbnb.index par self.rpls.index")

