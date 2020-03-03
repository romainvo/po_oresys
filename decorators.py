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
    
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
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
    
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
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
        print("\n")
        
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

    def extraire_surfhab(self, id : int):    
        """Retourne la surface habitable (en mètres carrés) indiquée dans 
        l'annonce airbnb si présente.
        
        Parameters:
            id (int): identifiant de l'annonce airbnb. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            surfhab(float): surface habitable indiquée dans l'annonce, np.nan 
            si non détectée.
        """
        
        name_airbnb = data_airbnb.loc[id, 'name']
        summary_airbnb = data_airbnb.loc[id, 'summary']
        space_airbnb = data_airbnb.loc[id, 'space']
        description_airbnb = data_airbnb.loc[id, 'description'] 
        
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
        
        surfhab_feet = []
        surfhab_meter = []
        
        if not pd.isna(description_airbnb):
            row = description_airbnb.lower()
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                surfhab_feet = list(temp_feet)
            if temp_meter:
                surfhab_meter = list(temp_meter)
        
        if not pd.isna(name_airbnb):
            row = name_airbnb.lower()
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                if len(surfhab_feet) == 0: 
                    surfhab_feet = list(temp_feet)
                else:
                    surfhab_feet += temp_feet
            if temp_meter:
                if len(surfhab_meter) == 0:
                    surfhab_meter = list(temp_feet)  
                else:
                    surfhab_meter += temp_meter
        
        if not pd.isna(summary_airbnb):
            row = summary_airbnb.lower()
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                if len(surfhab_feet) == 0: 
                    surfhab_feet = list(temp_feet)
                else:
                    surfhab_feet += temp_feet 
            if temp_meter:
                if len(surfhab_meter) == 0:
                    surfhab_meter = list(temp_feet)  
                else:
                    surfhab_meter += temp_meter
        
        if not pd.isna(space_airbnb):
            row = space_airbnb.lower()
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                if len(surfhab_feet) == 0: 
                    surfhab_feet = list(temp_feet)
                else:
                    surfhab_feet += temp_feet        
            if temp_meter:
                if len(surfhab_meter) == 0:
                    surfhab_meter = list(temp_feet)  
                else:
                    surfhab_meter += temp_meter
        
        if (len(surfhab_feet) != 0) and (len(surfhab_meter) == 0):
            surfhab_feet = list(map(lambda x: x.replace(',','.')
                        , surfhab_feet))
            surfhab_feet = list(map(float, surfhab_feet))
            surfhab_feet = max(surfhab_feet)
            surfhab_feet = surfhab_feet / 10.764 #1m² = 10.764 feet²
            
            return surfhab_feet
        elif (len(surfhab_feet) == 0) and (len(surfhab_meter) != 0):
            surfhab_meter = list(map(lambda x: x.replace(',','.')
                                    , surfhab_meter))
            surfhab_meter = list(map(float, surfhab_meter))
            surfhab_meter = max(surfhab_meter)
            
            return surfhab_meter
        elif (len(surfhab_feet) != 0) and (len(surfhab_meter) != 0):
            surfhab_feet = list(map(lambda x: x.replace(',','.')
                        , surfhab_feet))
            surfhab_feet = list(map(float, surfhab_feet))
            surfhab_feet = max(surfhab_feet)
            surfhab_feet = surfhab_feet / 10.764 #1m² = 10.764 feet²

            surfhab_meter = list(map(lambda x: x.replace(',','.')
                                    , surfhab_meter))
            surfhab_meter = list(map(float, surfhab_meter))
            surfhab_meter = max(surfhab_meter)
            
            return max(surfhab_feet, surfhab_meter)
        else:
            return np.nan
        
    def extraire_etage(self, id : int):
        """Retourne le numéro de l'étage (en mètres carrés) indiquée dans 
        l'annonce airbnb si présente.
        
        Parameters:
            id (int): identifiant de l'annonce airbnb. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            etage (int): numéro de l'étage indiqué dans l'annonce, np.nan si
            non-détecté.
        """
        
        name_airbnb = data_airbnb.loc[id, 'name']
        summary_airbnb = data_airbnb.loc[id, 'summary']
        space_airbnb = data_airbnb.loc[id, 'space']
        description_airbnb = data_airbnb.loc[id, 'description'] 
        
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

        etage_number = []
        etage_letter = []
    
        if not pd.isna(description_airbnb):
            row = description_airbnb.lower()
            temp_number = re.findall(pattern_etage_number, row) 
            temp_letter = re.findall(pattern_etage_letter, row)
                
            if temp_number:
                etage_number = list(temp_number)
            if temp_letter:
                etage_letter = list(temp_letter)
        
        if not pd.isna(name_airbnb):
            row = name_airbnb.lower()
            temp_number = re.findall(pattern_etage_number, row) 
            temp_letter = re.findall(pattern_etage_letter, row)
                
            if temp_number:
                if len(etage_number) == 0: 
                    etage_number = list(temp_number)
                else:
                    etage_number += temp_number
            if temp_letter:
                if len(etage_letter) == 0:
                    etage_letter = list(temp_letter)  
                else:
                    etage_letter += temp_letter
        
        if not pd.isna(summary_airbnb):
            row = summary_airbnb.lower()
            temp_number = re.findall(pattern_etage_number, row) 
            temp_letter = re.findall(pattern_etage_letter, row)
                
            if temp_number:
                if len(etage_number) == 0: 
                    etage_number = list(temp_number)
                else:
                    etage_number += temp_number
            if temp_letter:
                if len(etage_letter) == 0:
                    etage_letter = list(temp_letter)  
                else:
                    etage_letter += temp_letter
        
        if not pd.isna(space_airbnb):
            row = space_airbnb.lower()
            temp_number = re.findall(pattern_etage_number, row) 
            temp_letter = re.findall(pattern_etage_letter, row)
                
            if temp_number:
                if len(etage_number) == 0: 
                    etage_number = list(temp_number)
                else:
                    etage_number += temp_number
            if temp_letter:
                if len(etage_letter) == 0:
                    etage_letter = list(temp_letter)  
                else:
                    etage_letter += temp_letter
        
        if (len(etage_number) != 0) and (len(etage_letter) == 0):
            etage_number = list(map(float, etage_number))
            etage_number = min(etage_number)
            
            return etage_number
        elif (len(etage_number) == 0) and (len(etage_letter) != 0):
            etage_letter = list(map(lambda x: letter_to_number[x], etage_letter))
            etage_letter = min(etage_letter)
            
            return etage_letter
        elif (len(etage_number) != 0) and (len(etage_letter) != 0):
            etage_number = list(map(float, etage_number))
            etage_number = min(etage_number) 
            
            etage_letter = list(map(lambda x: letter_to_number[x], etage_letter))
            etage_letter = min(etage_letter)
            
            return min(etage_number, etage_letter)
        else:
            return np.nan
          
#    #extraction de l'étage dans la description du airbnb id
#    def extraire_nb_piece(id): 
        
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