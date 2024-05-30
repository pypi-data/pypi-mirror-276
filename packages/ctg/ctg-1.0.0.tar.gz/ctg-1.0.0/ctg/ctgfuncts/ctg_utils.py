__all__ = ['built_lat_long',
           'day_of_the_date',
           'get_cout_total',
           'get_sejour_info',
           'parse_date',
          ]

# Standard library imports
import itertools
import os
import re
from calendar import monthrange
from collections import Counter
from collections import namedtuple
from datetime import datetime
from pathlib import Path

# 3rd party imports
import pandas as pd

def parse_date(label:str,year:str)->datetime:
    '''
    Convert the label with the form yyy_mm_dd or mm_dd or yyyy-mm-dd or mm-dd to a datetime formatted date
    '''

    convert_to_date = lambda s: datetime.strptime(s,"%Y_%m_%d")
    label = re.sub(r"-","_",label)

    try:
        pattern = re.compile(r"(?P<year>\b\d{4}_)(?P<month>\d{1,2}_)(?P<day>\d{1,2})")
        match = pattern.search(label)
        date = convert_to_date(match.group("year")+match.group("month")+match.group("day"))
    except:
        pattern = re.compile(r"(?P<month>\d{1,2}_)(?P<day>\d{1,2})")
        match = pattern.search(label)
        date = convert_to_date(year+'_'+match.group("month")+match.group("day"))

    return date

def day_of_the_date(day,month,year):

    # Compute the day of the week of the date after "Elementary Number Theory David M. Burton Chap 6.4" [1]
    days_dict = {0: 'dimanche',
                 1: 'Lundi',
                 2: 'mardi',
                 3: 'mercredi',
                 4: 'jeudi',
                 5: 'vendredi',
                 6: 'samedi'}

    #month_dict = dict(zip(itertools.islice(itertools.cycle(l:=range(1,13)),2,2+len(l)),l))
    month_dict = {3: 1, 4: 2, 5: 3, 6: 4, 7: 5,
                  8: 6, 9: 7, 10: 8, 11: 9, 12:
                  10, 1: 11, 2: 12} # [1] p. 125

    y = year%100
    c = int(year/100)
    m = month_dict[month]
    if m>10 : y = y-1

    return days_dict[(day + int(2.6*m - 0.2) - 2*c + y + int(c/4) + int(y/4))%7] # [1] thm 6.12

def _yamlinfo_randos2df(ctg_path,year):

    # Reads the yaml file
    info_path = ctg_path / Path(str(year)) / Path('DATA') / Path('info_randos.xlsx')


    df = pd.read_excel(info_path)

    return df

def get_sejour_info(ctg_path,year):


    sejour_info = namedtuple('sejour_info', 'nbr_jours nbr_sejours histo')
    df =  _yamlinfo_randos2df(ctg_path,year)
    info_sejour = df.query('type=="sejour"')['nbr_jours'].tolist()

    c = Counter()
    c = Counter(info_sejour)


    sejour_info_tup = sejour_info( sum(info_sejour),len(info_sejour),c)

    return sejour_info_tup

def get_cout_total(year,type_sejour,dg,ctg_path):
    ''' Calcul du coût total des randonnées (type='randonnee") ou des séjours (type="sejour") pour l'année year
    '''

    file_info = Path(ctg_path) / Path(str(year)) / Path('DATA') / Path('info_randos.xlsx')
    df_indo = pd.read_excel(file_info)
    cout_total = 0
    for evenement in dg.index:
        date_rando = f"{str(year)[2:4]}-{evenement[0:5].replace('_','-')}"
        cout_rando = df_indo.query('date==@date_rando and type==@type_sejour')['Cout'].tolist()[0]
        nbr_participants = dg[evenement]
        cout_total += cout_rando * nbr_participants

    return cout_total

def built_lat_long(df):

    path_villes_de_france = Path(__file__).parent.parent / Path('ctgfuncts/CTG_RefFiles/villes_france_premium.csv')

    def normalize_ville(x):
        dic_ville = {'SAINT-HILAIRE-DU-TOUVET':"SAINT-HILAIRE-38",
                     'SAINT-HILAIRE':"SAINT-HILAIRE-38",
                     'LAVAL-EN-BELLEDONNE':'LAVAL-38',
                     'LAVAL':"LAVAL-38",
                     'CRETS-EN-BELLEDONNE':"SAINT-PIERRE-D'ALLEVARD"}
        if x in dic_ville.keys():
            return dic_ville[x]
        else:
            return x

    df_villes = pd.read_csv(path_villes_de_france,header=None,usecols=[3,19,20])
    dic_long = dict(zip(df_villes[3] , df_villes[19]))
    dic_lat = dict(zip(df_villes[3] , df_villes[20]))

    df['Ville'] = df['Ville'].str.replace(' ','-')
    df['Ville'] = df['Ville'].str.replace('ST-','SAINT-')
    df['Ville'] = df['Ville'].str.replace('\-D\-+',"-D'",regex=True)
    df['Ville'] = df['Ville'].str.replace('^LA-',"LA ",regex=True)
    df['Ville'] = df['Ville'].str.replace('^LE-',"LE ",regex=True)

    df['Ville'] = df['Ville'].apply(normalize_ville)


    df['long'] = df['Ville'].map(dic_long)
    df['lat'] = df['Ville'].map(dic_lat)
    list_villes = df['Ville'].tolist()
    Counter(list_villes)
    dg = df.groupby(['Ville']).count()['N° Licencié']

    dh = pd.DataFrame.from_dict({'Ville':dg.index,
                                'long':dg.index.map(dic_long),
                                'lat':dg.index.map(dic_lat),
                                'number':dg.tolist()})
    return df,dh