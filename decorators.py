import pandas as pd
import re
import numpy as np

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
        
#    #renvoie les coordonnées du rpls
#    def coordonnee(id):
#    
#    #renvoie la surface indiquée dans les données si présente.
#    def surfhab(id):
#    
#    #renvoie le nombre de piece du logement social concerné
#    def nbpiece(id):
#    
#    #renvoie l'arrondissement du logement social concerné
#    def arrondissement(id):
#
#    #renvoie l'étage du logement social concerné
#    def etage(id):
#    
#    #renvoie l'adresse du logement social concerné
#    def adresse(id):


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
            
    @property
    def center(self):
        # return the geographic center point of this DataFrame
        lat = self._obj.latitude
        lon = self._obj.longitude
        return (float(lon.mean()), float(lat.mean()))
   
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
        
        if not hasattr(id, '__iter__'):
            indexes = [id]
        else :
            indexes = id
            
        name_airbnb = self._obj.loc[indexes, 'name']
        summary_airbnb = self._obj.loc[indexes, 'summary']
        space_airbnb = self._obj.loc[indexes, 'space']
        description_airbnb = self._obj.loc[indexes, 'description'] 
    
        pattern_surfhab_meter = r"""(?x)
            (\d+\.?,?\d*)
            (?:
             \s+m.tre.\s+carr.*
            |\s?m2
            |\s?sqm
            |(?:m\s|\sm|m)²
            |\s?square.?\s?met...?
            |\s?sq\.?\s?(?:\.mts|meter.?|\.\s?m)
            |\s?sq\sm
            )
            """
        pattern_surfhab_feet = r"""(?x)
            (\d+\.?,?\d*)
            (?:
             \s?square.?\s?(?:feet|ft|foot)
            |\s?feet²
            |\s?sq\.?\s?(?:f.{0,2}t|\.\s?ft|f|/ft)
            )
            """
        
        surfhab_tokens_feet = dict()
        surfhab_tokens_meter = dict()
        surfhab_tokens = dict()
        
        for idx, row in zip(indexes, description_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    surfhab_tokens_feet[idx] = temp_feet
                    
                if temp_meter:
                    surfhab_tokens_meter[idx] = temp_meter
        
        for idx, row in zip(indexes, name_airbnb):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    if idx not in surfhab_tokens_feet:
                        surfhab_tokens_feet[idx] = list(temp_feet)
                    else:
                        surfhab_tokens_feet[idx] += temp_feet
                    
                if temp_meter:
                    if idx not in surfhab_tokens_meter:
                        surfhab_tokens_meter[idx] = temp_meter  
                    else:
                        surfhab_tokens_meter[idx] += temp_meter
        
        for idx, row in zip(indexes, summary_airbnb):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    if idx not in surfhab_tokens_feet:
                        surfhab_tokens_feet[idx] = list(temp_feet)
                    else:
                        surfhab_tokens_feet[idx] += temp_feet
                    
                if temp_meter:
                    if idx not in surfhab_tokens_meter:
                        surfhab_tokens_meter[idx] = temp_meter  
                    else:
                        surfhab_tokens_meter[idx] += temp_meter
        
        for idx, row in zip(indexes, space_airbnb):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    if idx not in surfhab_tokens_feet:
                        surfhab_tokens_feet[idx] = temp_feet
                    else:
                        surfhab_tokens_feet[idx] += temp_feet
                    
                if temp_meter:
                    if idx not in surfhab_tokens_meter:
                        surfhab_tokens_meter[idx] = temp_meter  
                    else:
                        surfhab_tokens_meter[idx] += temp_meter
        
        for key, element in surfhab_tokens_meter.items():
            surfhab_tokens_meter[key] = list(map(lambda x: x.replace(',','.'), element))
            surfhab_tokens_meter[key] = list(map(float, surfhab_tokens_meter[key]))
            surfhab_tokens_meter[key] = max(surfhab_tokens_meter[key])
        
        for key, element in surfhab_tokens_feet.items():
            surfhab_tokens_feet[key] = list(map(lambda x: x.replace(',','.'), element))
            surfhab_tokens_feet[key] = list(map(float, surfhab_tokens_feet[key]))
            surfhab_tokens_feet[key] = max(surfhab_tokens_feet[key])
            surfhab_tokens_feet[key] = surfhab_tokens_feet[key] / 10.764 #1m² = 10.764 feet²
            
        for key in set(list(surfhab_tokens_meter.keys())+list(surfhab_tokens_feet.keys())):
            if (key not in surfhab_tokens_meter) and (key in surfhab_tokens_feet):
                surfhab_tokens[key] = surfhab_tokens_feet[key]
            elif (key in surfhab_tokens_meter) and (key not in surfhab_tokens_feet):
                surfhab_tokens[key] = surfhab_tokens_meter[key]
            elif (key in surfhab_tokens_meter) and (key in surfhab_tokens_feet):
                surfhab_tokens[key] \
                = max(surfhab_tokens_feet[key], surfhab_tokens_meter[key])
        
        if type(id) is int:
            if id in surfhab_tokens:
                return surfhab_tokens[id]
            else:
                return np.nan
        else:
            return surfhab_tokens
        
    def extraire_etage(self, id : int):
        """Retourne le numéro de l'étage (en mètres carrés) indiquée dans 
        l'annonce airbnb si présente.
        
        Parameters:
            id (int or [int]): identifiant de l'annonce airbnb ou liste
            d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            etage (int): numéro de l'étage indiqué dans l'annonce, np.nan si
            non-détecté.
        """
        
        if not hasattr(id, '__iter__'):
            indexes = [id]
        else :
            indexes = id
            
        name_airbnb = self._obj.loc[indexes, 'name']
        summary_airbnb = self._obj.loc[indexes, 'summary']
        space_airbnb = self._obj.loc[indexes, 'space']
        description_airbnb = self._obj.loc[indexes, 'description'] 
        
        pattern_etage_number = r"""(?x)
            (\d+(?:\.\d+)?)
            (?:
             \s*(?:th|d|nd|rd|st|e|.me|°)\s*(?:floor|.tage)
            |\s*(?:th|d|nd|rd|st|e|.me|°)[a-z\s]{0,20}(?:floor|.tage)
            |\s*(?:floor|.tage)
            )
            """
        pattern_etage_letter = r"""(?x)
            (first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|nineth|tenth
            |eleventh|twelveth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth
            |eighteenth|nineteenth|twentieth|ground|rez.de.chauss[a-z]{1,2}
            |premier|deuxi.me|troisi.me[a-z]?|quatri.me[a-z]?|cinqui.me[a-z]?
            |sixi.me[a-z]?|septi.me[a-z]?|huiti.me[a-z]?|neuvi.me[a-z]?|dizi.me[a-z]?
            |onzi.me[a-z]?|douzi.me[a-z]?|treizi.me[a-z]?|quatorzi.me[a-z]?|quinzi.me[a-z]?
            |seizi.me[a-z]?|dix.?septi.me[a-z]?|dix.huiti.me[a-z]?|dix.neuvi.me[a-z]?
            |vingti.me[a-z]?)
            (?:
             \s*(?:floor|.tage)
            |[a-z\s]{0,20}(?:floor|.tage)
            )
            """
        
        letter_to_number \
        = {'first':1,'second':2,'third':3,'fourth':4,'fifth':5
            ,'sixth':6,'seventh':7,'eighth':8,'ninth':9,'nineth':9
            ,'tenth':10,'eleventh':11,'twelveth':12,'thirteenth':13
            ,'fourteenth':14,'fifteenth':15,'sixteenth':16
            ,'seventeenth':17,'eighteenth':18,'nineteenth':19
            ,'twentieth':20,'ground':0,'premier':1,'deuxieme':2
            ,'deuxième':2,'troisieme':3,'troisième':3,'quatrieme':4
            ,'quatrième':4,'cinquieme':5,'cinquième':5,'sixieme':6
            ,'sixième':6,'septieme':7,'septième':7,'huitieme':8
            ,'huitième':8,'neuvieme':9,'neuvième':9,'dixieme':10
            ,'dixième':10,'onzieme':11,'onzième':11,'douzieme':12
            ,'douzième':12,'treizieme':13,'treizième':13,'quatorzieme':14
            ,'quatorzième':14,'quinzieme':15,'quinzième':15
            ,'seizieme':16,'seizième':16,'dix-septieme':17
            ,'dix-septième':17,'dix-huitieme':18,'dix-huitième':18
            ,'dix-neuvieme':19,'dix-neuvième':19,'vingtieme':20
            ,'vingtième':20,'rez-de-chaussée':0,'rez-de-chausee':0
            ,'rez-de-chaussé':0,'rez-de-chausse':0,'rez de chaussée':0
            ,'rez de chaussé':0, 'rez de chaussez':0} 
           
        etage_tokens_number = dict()
        etage_tokens_letter = dict()
        etage_tokens = dict()
        
        for idx, row in zip(indexes, description_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    etage_tokens_number[idx] = temp_number
                    
                if temp_letter:
                    etage_tokens_letter[idx] = temp_letter
                    
        for idx, row in zip(indexes, name_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    if idx not in etage_tokens_number:
                        etage_tokens_number[idx] = list(temp_number)
                    else:
                        etage_tokens_number[idx] += temp_number
        
                if temp_letter:
                    if idx not in etage_tokens_letter:
                        etage_tokens_letter[idx] = list(temp_letter)
                    else:
                        etage_tokens_letter[idx] += temp_letter
                        
        for idx, row in zip(indexes, summary_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    if idx not in etage_tokens_number:
                        etage_tokens_number[idx] = list(temp_number)
                    else:
                        etage_tokens_number[idx] += temp_number
        
                if temp_letter:
                    if idx not in etage_tokens_letter:
                        etage_tokens_letter[idx] = list(temp_letter)
                    else:
                        etage_tokens_letter[idx] += temp_letter
        
        for idx, row in zip(indexes, space_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    if idx not in etage_tokens_number:
                        etage_tokens_number[idx] = list(temp_number)
                    else:
                        etage_tokens_number[idx] += temp_number
        
                if temp_letter:
                    if idx not in etage_tokens_letter:
                        etage_tokens_letter[idx] = list(temp_letter)
                    else:
                        etage_tokens_letter[idx] += temp_letter
                              
        for key, element in etage_tokens_number.items():
            etage_tokens_number[key] = list(map(float, element))
            etage_tokens_number[key] = min(etage_tokens_number[key])
        
        for key, element in etage_tokens_letter.items():
            etage_tokens_letter[key] \
            = list(map(lambda x: letter_to_number[x], element))
            etage_tokens_letter[key] = min(etage_tokens_letter[key])
            
        for key in set(list(etage_tokens_number.keys())+list(etage_tokens_letter.keys())):
            if (key not in etage_tokens_number) and (key in etage_tokens_letter):
                etage_tokens[key] = etage_tokens_letter[key]
            elif (key not in etage_tokens_letter) and (key in etage_tokens_number):
                etage_tokens[key] = etage_tokens_number[key]
            elif (key in etage_tokens_number) and (key in etage_tokens_letter):
                etage_tokens[key] \
                = min(etage_tokens_number[key], etage_tokens_letter[key])
                
        if type(id) is int:
            if id in etage_tokens:
                return etage_tokens[id]
            else:
                return np.nan
        else:
            return etage_tokens
          
    #extraction de l'étage dans la description du airbnb id
    def extraire_nbpiece(self, id : int):
        
        return np.nan
        
if __name__ == '__main__':

    data_airbnb = pd.read_csv("csv/airbnb.csv", sep=',', header='infer',
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
            
    data_rpls = pd.read_csv("csv/paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                    header='infer', index_col=0,
                    converters={'codepostal':converter_codepostal
                                , 'etage':converter_etage},
                    dtype={'longitude':'float', 'latitude':'float'})
    
    data_rpls.index.rename('id_rpls', inplace=True)