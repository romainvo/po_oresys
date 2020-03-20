import pandas as pd
import re
import numpy as np
import po_oresys.api.text_miner as text_miner

@pd.api.extensions.register_dataframe_accessor("rpls")
class RPLSAccessor:
    """ Instancie un décorateur python permettant de manipuler les dataframe
    instanciant des rpls (répertoire des logements sociaux) plus facilement.
    
    Parameters:
        _obj (pd.DataFrame): DataFrame regroupant l'ensemble des logements
        sociaux.
    """
    
    def __init__(self, pandas_obj : pd.DataFrame):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj : pd.DataFrame):
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

    def coordonnees(self, id : int):
        return (self._obj.loc[id,'latitude'], self._obj.loc[id,'longitude'])

    def complete_description(self, id : int, pprint=True, rreturn=False):
        """Print l'ensemble des champs textuels pertinents pour le logement
        social d'iditifiant 'id'
        
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
            
        Keyword arguments:
            pprint (boolean): True si on affiche la description complète

            rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        
        Returns:
            (pd.Series): en index les noms des champs textuels retournés, en 
            élements les string des champs textuels pertinents.
        """
        
        columns = ['libcom','numvoie','typvoie','nomvoie','surfhab', 'etage'
                   ,'nbpiece']
        print("Champs affichés : {}".format(columns[0]), end=" ")
        for elt in columns[1:]:
            print(",",elt, end="")
        print(" - coordonnées gps = {}".format(self.coordonnees(id), "\n"))
        print()
        
        if pprint:
            for elt in columns :
                print("{} :".format(elt), end=" ")
                print(self._obj.loc[id, elt])
            print()
        
        if rreturn:
            return self._obj.loc[id, columns]  
        
    """ renvoie la surface habitable du rpls caractérisé par l'id id
    Parameters:
        id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
    Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
    Return:
        valeur de la surface habitable du rpls id dans le dataframe.(float)
    """
    def surface_habitable(self,id,pprint = True,rreturn = False):
        if(pprint):
            print(self._obj.loc[id,'surfhab'])
        
        if(rreturn):
            return self._obj.loc[id,'surfhab']
 
    
    def nombre_piece(self,id,pprint = True,rreturn = False):
        """ renvoie le nombre de piece du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        valeur du nombre de piece du rpls id dans le dataframe.(float)
        """
        if(pprint):
            print(self._obj.loc[id,'nbpiece'])
        
        if(rreturn):
            return self._obj.loc[id,'nbpiece']
 

    def arrondissement(self,id,pprint = True,rreturn = False):
        """ renvoie l'arrondissement' du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        arrondissement du rpls id dans le dataframe (string).
        """
        if(pprint):
            print(self._obj.loc[id,'libcom'])
        
        if(rreturn):
            return self._obj.loc[id,'libcom']

    def etage(self,id,pprint = True,rreturn = False):
        """ renvoie l'etage' du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        etage du rpls id dans le dataframe (float).
        """
        if(pprint):
            print(self._obj.loc[id,'etage'])
        
        if(rreturn):
            return self._obj.loc[id,'etage']

    def adresse(self,id,pprint = True,rreturn = False):
        """ renvoie l'adresse du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        adresse du rpls id dans le dataframe (string).
        """
        S = self._obj.loc[id,'numvoie']+" "
        if(self._obj.loc[id,'indrep']!=np.nan):
            S=S+self._obj.loc[id,'indrep']
        S=S+self._obj.loc[id,'typvoie']+" "+self._obj.loc[id,'nomvoie']
        if(self._obj.loc[id,'bat']!=np.nan):
            S=S+", batiment "+self.batiment(id,pprint=False,rreturn=True)
        if(self._obj.loc[id,'numappt']!=np.nan):
            S=S+", appartement "+self.numero_appartement(id,pprint=False,rreturn=True)
        if(pprint):
            print(S)
        if(rreturn):
            return S
    
    def batiment(self,id,pprint = True,rreturn = False):
        """ renvoie le batiment du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        batiment du rpls id dans le dataframe (float).
        """

        if(pprint):
            print(self._obj.loc[id,'bat'])
        
        if(rreturn):
            return self._obj.loc[id,'bat']
    
    def numero_appartement(self,id,pprint = True,rreturn = False):
        """ renvoie le numero d'appartement du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        numero d'appartement du rpls id dans le dataframe (float).
        """
        if(pprint):
            print(self._obj.loc[id,'numappt'])
        if(rreturn):
            return self._obj.loc[id,'numappt']

@pd.api.extensions.register_dataframe_accessor("bnb")
class AirbnbAccessor:
    """ Instancie un décorateur python permettant de manipuler les dataframe
    regroupant des annonces airbnb plus facilement.
    
    Parameters:
        _obj (pd.DataFrame): DataFrame regroupant l'ensemble des annonces
        airbnb.
    """
    
    def __init__(self, pandas_obj : pd.DataFrame):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj : pd.DataFrame):
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
   
    def complete_description(self, id : int, pprint=True, rreturn=False):
        """Print l'ensemble des champs textuels pertinents pour l'annonce 
        airbnb d'iditifiant 'id'
        
        Parameters:
            id (int): identifiant de l'annonce airbnb. Index de la ligne dans 
            la DataFrame.
            
        Keyword arguments:
            pprint (boolean): True si on affiche la description complète

            rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        
        Returns:
            (pd.Series): en index les noms des champs textuels retournés, en 
            élements les string des champs textuels pertinents.
        """
        
        columns = ['name', 'summary', 'space', 'description']
        print("Champs affichés : {}".format(columns[0]), end=" ")
        for elt in columns[1:]:
            print(",",elt, end="")
        print(" - coordonnées gps = {}".format(self.coordonnees(id), "\n"))
        print()
        
        if pprint:
            for elt in columns :
                print("{} :".format(elt))
                print(self._obj.loc[id, elt], "\n")
        
        if rreturn:
            return self._obj.loc[id, columns]  
  
    def coordonnees(self, id : int):
        return (self._obj.loc[id,'latitude'], self._obj.loc[id,'longitude'])
    
    def name(self, id : int):
        return self._obj.loc[id, 'name']
    
    def summary(self, id : int):
        return self._obj.loc[id, 'summary']
    
    def description(self, id : int):
        return self._obj.loc[id, 'description']
    
    def all_extractions(self, id : int, pprint=False, rreturn=True):
        extractions = dict()
        extractions['surfhab'] = self.extraire_surfhab(id)
        extractions['etage'] = self.extraire_etage(id)
        extractions['nbpiece'] = self.extraire_nbpiece(id)
        
        if pprint:
            print("Ensemble des champs textuels extraits :")
            print(extractions)
            
        if rreturn:
            return extractions

    def extraire_surfhab(self, id):    
        """Retourne la surface habitable (en mètres carrés) indiquée dans 
        l'annonce airbnb si présente.
        
        Parameters:
            id (int or [int]): identifiant de l'annonce airbnb ou liste
            d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            surfhab (float or {id:surfhab}): surface habitable indiquée dans 
            l'annonce, np.nan si non détectée.
        """
        
        return text_miner.extraire_surfhab(self._obj, id)
        
    def extraire_etage(self, id : int):
        """Retourne le numéro de l'étage indiqué dans l'annonce airbnb si présente.
        
        Parameters:
            id (int or [int]): identifiant de l'annonce airbnb ou liste
            d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            etage (int): numéro de l'étage indiqué dans l'annonce, np.nan si
            non-détecté.
        """
        
        return text_miner.extraire_etage(self._obj, id)
          
    def extraire_nbpiece(self, id : int):
        """Retourne le nombre de pièces indiqué dans l'annonce airbnb si présente.
        
        Parameters:
            id (int or [int]): identifiant de l'annonce airbnb ou liste
            d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            etage (int): nombre de pièce indiqué dans l'annonce, np.nan si
            non-détecté.
        """
        
        return text_miner.extraire_nbpiece(self._obj, id)
        
if __name__ == '__main__':

    data_airbnb = pd.read_csv("po_oresys/csv/airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
    
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

