#%%
import json
import pandas as pd
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns

# %%

files = [file for file in os.listdir('./data')]
files

#%%

l_df = []



for file in files:
    with open(f"./data/{file}") as f :
        data = json.load(f)
    sex_l = []
    name_l = []
    conjoint_l = []
    owner_l = []
    period_l = []

    birth_date_l = []
    death_date_l = []
    marriage_date_l = []

    birth_place_l = []
    death_place_l = []
    marriage_place_l = []

    lieu_l = []

    for indv in data:
        print(indv)
        print(indv['indv'])
        if indv['indv'][0].startswith('H') or indv['indv'][0].startswith('F'):
            sex_l.append(indv['indv'][0].split(' : ')[0])
            name_l.append(indv['indv'][0].split(' : ')[1])
        else:
            sex_l.append(indv['indv'][0])
            name_l.append(indv['indv'][0])

        if indv['indv'][1].startswith('Arbre'):
            owner_l.append(indv['indv'][1])
        elif indv['indv'][1].startswith('Conjoint'):
            conjoint_l.append(indv['indv'][1].lstrip('Conjoint : '))
        else:
            pass

        if len(indv['indv']) == 3:
            if indv['indv'][2].startswith('Arbre'):
                owner_l.append(indv['indv'][2])
            else:
                pass
        else:
            pass

        for date in indv['period']:
            if date.startswith('Naissance'):
                birth_date_l.append(date.lstrip('Naissance'))
            elif date.startswith('Décès'):
                death_date_l.append(date.lstrip('Décès'))

        period_l.append(indv['period'])
        lieu_l.append(indv['lieu'])

        for place in indv['lieu']:
            if place[0].startswith('Naissance'):
                birth_place_l.append(place[0].lstrip('Naissance : '))
            elif place[0].startswith('Décès'):
                death_place_l.append(place[0].lstrip('Décès : '))
            elif place[0].startswith('Mariage'):
                marriage_place_l.append(place[0].lstrip('Mariage : '))
            else:
                pass
                
    df = pd.DataFrame([sex_l, name_l, conjoint_l, owner_l, period_l, lieu_l, birth_date_l, death_date_l, marriage_date_l, birth_place_l, death_place_l, marriage_place_l]).T
    df.columns = ['sex', 'name', 'conjoint', 'owner', "period", "lieu", "birth_date", 'death_date', "marriage_date",  "birth_place", "death_place", "marriage_place"]
    l_df.append(df)

master = pd.concat(l_df)    
master = master.reset_index(drop=True)
master.head()

# %%

len(master)


# %%
master.tail(500)

#%%

def get_marriage_date(x):
    if x is not None:
        if len(x) > 0:
            r = str(x).split("(")
            if len(r) > 1:
                r = r[1].replace(')', '')
            else:
                r = ''
    else:
        r = ''
    return r

master['marriage_date'] = master['conjoint'].apply(lambda x : get_marriage_date(x))

# %%


# %%

place = []
place.extend(master['birth_place'].value_counts().index)
place.extend(master['death_place'].value_counts().index)
place.extend(master['marriage_place'].value_counts().index)
place = list(set(place))
print(f"Nb locations in dataset : {len(place)}")
place

# %%
t = pd.Series(place).sort_values().to_list()
t

# %%

def replace_geography(x):
    x = str(x).lstrip()
    # // A
    if x == 'Angers, 49000, FR FRANCE, Maine-et-Loire, France' or x == 'Angers, 49000, Maine-et-Loire, France' or x == 'Angers, 49007, Maine-et-Loire, France' or x == 'Angers, Maine-et-Loire, France' or x == "Angers, 49000, Maine-et-Loire, Pays de la Loire, France" or x == 'Angers 2ème,' or x == 'Angers 3ème Arr.,' or x == 'Angers,' or x == "Angers" or x == "Angers (49), Maine-et-Loire, Pays de la Loire, FRANCE":
        r = "Angers, 49000, Maine-et-Loire, Pays de la Loire, France"
        g = [47.47283884908798, -0.5534940664669215] 
    elif x == 'Assé-le-Riboul, 72012, Sarthe, Pays de la Loire, France' or x == 'Assé-le-Riboul, 72170, Sarthe, Pays de la Loire, FRANCE,' or x == 'la Barbiniere - Assé-le-Riboul, 72012, Sarthe, Pays de la Loire, France,' or x == "Bois d'Assé - Assé-le-Riboul, 72012, Sarthe, Pays de la Loire, France," or x == 'Assé-le-Riboul, 72012, Pays de la Loire, France,' or x == 'Assé-le-Riboul, 72012, Sarthe, Pays de la Loire, France,' or x == 'Assé-le-Riboul, 72012, Pays de la Loire, France' or x == 'Barbiniere - Assé-le-Riboul, 72012, Sarthe, Pays de la Loire, France,':
        r = 'Assé-le-Riboul, 72012, Sarthe, Pays de la Loire, France'
        g = [48.19349622305956, 0.08716587461851467]
    elif x == 'Alençon, 61000, Orne, Normandie, France' or x == '61 Alençon,' or x == '23 rue des Granges - Alençon, 61000, Orne, Normandie, France,':
        r = 'Alençon, 61000, Orne, Normandie, France'
        g = [48.43267294913876, 0.0944893266270997]
    elif x == "Ancinnes, 72005, Sarthe, Pays de la Loire, France" or x == 'Ancinnes (sarthe),' or x == 'Ancinnes, 72005, Sarthe, Pays de la Loire, France,':
        r = "Ancinnes, 72005, Sarthe, Pays de la Loire, France"
        g = [48.369616962848816, 0.17619590070547042]
    elif x == 'Appenai-sous-Bellême, 61005, Orne, Normandie, France' or x == 'Appenai-sous-Bellême, 61005, Orne, Normandie, France,':
        r = 'Appenai-sous-Bellême, 61005, Orne, Normandie, France'
        g = [48.34399343213663, 0.5586789899415898]
    elif x == "Ancenis, 44003, Loire-Atlantique, France":
        r = "Ancenis, 44003, Loire-Atlantique, France"
        g = [0., 0.]
    
    # // B
    elif x == 'La Bazoge, 72650, Sarthe, Pays de la Loire, France' or x == 'La Butte - La Bazoge, 72650, Sarthe, Pays de la Loire, FRANCE,' or x == 'La Bazoge, 72650, Sarthe, Pays de la Loire, FRANCE' or x == 'La Bazoge, 72650, Sarthe, Pays de la Loire, FRANCE,' or x == 'la bazoge 72' or x == 'Bouqueteaux - La Bazoge, 72650, Sarthe, Pays de la Loire, FRANCE,' or x == 'Bouqueteaux - La Bazoge, 72650, Sarthe, Pays de la Loire, FRANCE' or x == 'la bazoge 72,' or x == 'La Bazoge, 72024, Pays de la Loire, France' or x == 'la bazoge':
        r = 'La Bazoge, 72650, Sarthe, Pays de la Loire, France'
        g = [48.09719284999686, 0.15507781812200938]
    elif x == "Bellou-sur-Huisne, 61042, Orne, Normandie, France" or x == 'Bellou-sur-Huisne, 61042, Orne, Normandie, FRANCE,' or x == 'Bellou-sur-Huisne, Orne, France' or x == 'Bellou-sur-Huisne, 61042, Orne, Normandie, FRANCE' or x == 'La Butte - Bellou-sur-Huisne, 61042, Orne, Normandie, FRANCE,' or x == 'La Taupinière - Bellou-sur-Huisne, 61042, Orne, Normandie, FRANCE,' or x == 'Bellou-sur-Huisne, Orne, France,':
        r = "Bellou-sur-Huisne, 61042, Orne, Normandie, France"
        g = [48.42557227695994, 0.7563532168839905]
    elif x == 'Brains-sur-Gée, 72550, Sarthe, Pays de la Loire, France' or x == 'Brains-sur-Gée, 72550, Sarthe, Pays de la Loire, FRANCE' or x == 'Brains-sur-Gée, 72550, Sarthe, Pays de la Loire, FRANCE,':
        r = 'Brains-sur-Gée, 72550, Sarthe, Pays de la Loire, France'
        g = [48.01487590175186, -0.026881544696310485]
    elif x == 'Blain 44130, Loire-Atlantique, France' or x == 'Blain, 44015, Bretagne, Loire-Atlantique, France' or x == 'Blain, 44015, Bretagne, coyault, Loire-Atlantique, France' or x == 'Blain, 44015, Bretagne, la mercerais, Loire-Atlantique, France' or x == 'Blain, 44015, Bretagne, la pessuais, Loire-Atlantique, France' or x == 'Blain, 44015, Loire-Atlantique, France' or x == 'Blain, 44015, PBys de la Loire, Loire-Atlantique, France' or x == 'Blain, 44130, Loire-Atlantique, France' or x == 'Blain, Bretagne, Loire-Atlantique, France' or x == 'Blain, Loire-Atlantique, France' or x == 'Blain, la Bidais, Loire-Atlantique, France' or x == 'Blain, la Potironnais, Loire-Atlantique, France' or x == 'Blain,44130, Loire-Atlantique, France' or x == 'Blain, 44130, Loire-Atlantique, France' or x == 'Blain, 44015, Loire Atlantique, Pays de la Loire, France' or x == 'Blain, 44015, Loire-Atlantique, Pays de la Loire, France,' or x =='Blain, 44015, Loire-Atlantique, Pays de la Loire, France':
        r = 'Blain, 44015, Loire Atlantique, Pays de la Loire, France'
        g = [47.47710112969596, -1.7670651628296452]
    elif x == 'Beaumont-sur-Sarthe, 72029, Pays de la Loire, France' or x == 'Beaumont-sur-Sarthe, 72029, Pays de la Loire, France,' or x == 'Beaumont-sur-Sarthe, 72170, Sarthe, Pays de la Loire, FRANCE' or x == 'Beaumont,' :
        r = "Beaumont-sur-Sarthe, 72170, Sarthe, Pays de la Loire, France"
        g = [48.225454229794586, 0.1292082862734064]
    elif x == 'Bellavilliers, 61037, Orne, Normandie, France,':
        r = 'Bellavilliers, 61037, Orne, Normandie, France'
        g = [48.423093872967534, 0.4980931791374547]
    elif x == "Bourgneuf en Retz, 44021, Loire Atlantique, Pays de la Loire, France" or x == 'Nombreuil - Bourgneuf en Retz, 44' or x == 'Bourgneuf en Retz, 44,' or x == 'Bourgneuf en Retz, 44':
        r = "Bourgneuf en Retz, 44021, Loire Atlantique, Pays de la Loire, France"
        g = [47.04275289980967, -1.9496753533654674]
        
    # // C
    elif x == "Champtocé sur Loire, Maine et Loire, France" or x == 'Champtocé-sur-Loire, 49' or x == 'Champtocé-sur-Loire, 49068, Maine et Loire, Pays de la Loire, France,' or x == "Champtocé-sur-Loire, 49068, Maine et Loire, Pays de la Loire, France":
        r =  "Champtocé-sur-Loire, 49068, Maine et Loire, Pays de la Loire, France"
        g = [47.412581100284065, -0.865700565104513]
    elif x == 'La Chapelle-Glain (44), Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'La Chapelle-Glain, 44670, France' or x == 'La Chapelle-Glain, Loire Atlantique, France':
        r = "La Chapelle-Glain, 44670, Loire-Atlantique, Pays de la Loire, France"
        g = [47.62213605793191, -1.1963718452528325]
    elif x == 'Condé-sur-Huisne, 61116, Orne, Normandie, FRANCE,' or x == 'Le Brouillard - Condé-sur-Huisne, 61116, Orne, Normandie, FRANCE,' or x == 'village de Brouillard - Condé-sur-Huisne, 61116, Orne, Normandie, FRANCE,' or x == 'village de Riverai - Condé-sur-Huisne, 61116, Orne, Normandie, FRANCE,' or x == 'Condé-sur-Huisne, 61116, Orne, Normandie, FRANCE':
        r ='Condé-sur-Huisne, 61116, Orne, Normandie, France'
        g = [48.38155023782034, 0.8492075392860832]
    elif x == 'Chérancé (sarthe),' or x== 'Chérancé, 72078, Sarthe, Pays de la Loire, France,' or x == 'Chérancé (sarthe)':
        r = 'Chérancé, 72078, Sarthe, Pays de la Loire, France'
        g = [48.28643560256843, 0.17494452618227066]
    elif x == 'Basse-Normandie - Ceton, 61260, Orne, France' or x == 'Basse-Normandie - Ceton, 61260, Orne, France,':
        r = 'Ceton, 61260, Orne, Normandie, France'
        g = [48.224734792719715, 0.7486089053753266]
    elif x == 'Châteaubriant, 44036, Loire-Atlantique, France' or x == 'Châteaubriant, 44110, Loire-Atlantique, Pays de la Loire, FRANCE,':
        r = "Châteaubriant, 44036, Loire-Atlantique, France"
        g = [47.7170669204089, -1.3805278316888892]
        
    # // D
    elif x == 'Derval, 44051, Bretagne, Loire-Atlantique, France' or x == 'Derval, 44051, Loire-Atlantique, France' or x == 'Derval, 44590, Loire- Atlantique, Pays- De- La- Loire, Loire-Atlantique, France' or x == 'Derval, 44590, Loire-Atlantique, France' or x == 'Derval, Loire-Atlantique, France' or x == 'Derval,44590, Loire-Atlantique, France' or x == 'Derval, 44590, Loire- Atlantique, Pays- De- La- Loire, Loire-Atlantique, France' or x == 'Derval,44590, Loire-Atlantique, France' or x == "Derval (44), Loire-Atlantique, Pays de la Loire, FRANCE" or x == 'Derval (44),' or x == 'Derval (44)' or x == 'Derval, 44590, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'le petit plessis - Derval, 44590, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'Derval, 44590, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == "Derval, 44051, Loire-Atlantique, Pays de la Loire" or x =="Derval, Loire Atlantique, Pays de la Loire, France":
        r =  "Derval, 44051, Loire-Atlantique, Pays de la Loire, France"
        g = [47.664938555107376, -1.6796956248721728]
    elif x == 'Dangeul, Sarthe, Pays de la Loire, France' or x == 'Dangeul, 72260, Sarthe, Pays de la Loire, FRANCE':
        r = 'Dangeul, 72112, Sarthe, Pays de la Loire, France'
        g = [48.24710884358884, 0.25755118789544845]
    elif x == 'Dorceau, 61147, Orne, Normandie, France,':
        r = 'Dorceau, 61147, Orne, Normandie, France'
        g = [48.423285894842756, 0.8027067882873334]

    # // E
    elif x == 'ERBRAY, (.054), Bretagne, France., Loire-Atlantique, France' or x == 'Erbray, 44054, Loire-Atlantique, France' or x == 'Erbray, 44110, FR FRANCE, Loire-Atlantique, France' or x == 'Erbray, 44110, Loire- Atlantique, Pays- De- La- Loire, Loire-Atlantique, France' or x == 'Erbray, 44110, Loire-Atlantique, France' or x == 'Erbray, Loire-Atlantique, France' or x == 'Erbray,44054, Loire-Atlantique, France' or x == 'Erbray/, Loire-Atlantique, France' or x == 'Erbray, Loire-Atlantique, France' or x == 'Erbray, 44110, Loire- Atlantique, Pays- De- La- Loire, Loire-Atlantique, France' or x == "Erbray, 44054, Loire-Atlantique, France" or x == "Erbray, 44110, Loire-Atlantique, Pays de la Loire, France" or x == 'La Rousselière - Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'La Touche - Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'Erbray (44)' or x == 'Le Cormier-Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'La Ferronnière - Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'Erbray Loire Inférieure, , , ,' or x == 'Les Garellières-Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'Le Boulay-Erbray, 44054, Loire Atlantique, Pays de la Loire, , France,' or x == 'La Coltière - Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'Erbray, 44054, Loire Atlantique, Pays de la Loire, France,' or x == 'Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'Le Perray-Erbray, 44054, Loire Atlantique, Pays de la Loire, France,' or x == 'Erbray, 44110, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'La Ménardière - Erbray ,44054, Loire Atlantique, Pays de Loire, France' or x == 'Le Boulay-Erbray, 44054, Loire Atlantique, Pays de la Loire, , France' or x == 'Le Perray-Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'Erbray Loire Atlantique' or x == 'village de cantrais - Erbray, 44110, Loire-Atlantique, Pays de la Loire, FRANCE' or x == "Erbray, 44110, Loire-Atlantique, Pays de la Loire" or x == ' Erbray' or x == "Erbray (44), Loire-Atlantique, Pays de la Loire, FRANCE" or x =="Erbray, 44, Loire-Atlantique" or x == "Erbray, 44054, Loire Atlantique, Pays de la Loire, France" or x == 'Le Cormier, Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'Le Boulay) - Erbray, 44054, Loire Atlantique, Pays de la Loire, France' or x == 'La Ménardière - Erbray, 44054, Loire Atlantique, Pays de Loire, France' or x == 'Les Garellières, Erbray, 44054, Loire Atlantique, Pays de la Loire, France' : 
        r =  "Erbray, 44110, Loire-Atlantique, Pays de la Loire, France"
        g = [47.65550932252617, -1.318016468838816]
    elif x == 'Eperrais, 61154, Orne, Normandie, France,':
        r = 'Eperrais, 61154, Orne, Normandie, France'
        g = [48.42247238284746, 0.5494305897229315]
        
    # // F
    elif x == 'Fay de Bretagne (), Loire-Atlantique, France' or x == 'Fay de Bretagne, 44130, Loire-Atlantique, France' or x == 'Fay de Bretagne, Loire-Atlantique, France' or x == 'Fay, Loire-Atlantique, France' or x == 'Fay-de-Bretagne, 44056, Loire-Atlantique, France' or x == 'Fay-de-Bretagne, 44130, Loire-Atlantique, France' or x == 'Fay-de-Bretagne, FR-44056, Bretagne, Loire-Atlantique, France' or x == 'Fay-de-Bretagne, Loire-Atlantique, France' or x == 'Fay de Bretagne, 44130, Loire-Atlantique, France' or x == 'La Chapronais -Fay-de-Bretagne, 44056, Loire-Atlantique, Pays de la Loire, France,' or x == 'Fay-de-Bretagne, 44056, Loire-Atlantique, Pays de la Loire, France,' or x =='Meluc - Fay-de-Bretagne, 44056, Loire-Atlantique, Pays de la Loire, France' :
        r = 'Fay-de-Bretagne, 44056, Loire-Atlantique, Pays de la Loire, France'
        g = [47.41200938166818, -1.7929900540756116]
    elif x == 'La Marsollière - Fyé, 72139, Sarthe, Pays de la Loire, France,' or x == 'Fyé, 72139, Pays de la Loire, France' or x == 'Fyé, 72139, Sarthe, Pays de la Loire, France,':
        r ='Fyé, 72139, Sarthe, Pays de la Loire, France'
        g = [48.32442098144286, 0.08234501720679109]

    # // G
    elif x == 'Grand Fougeray, 35, Ille et Villaine, Bretagne, FRANCE' or x == 'la hutte à bourdin - Grand-Fougeray, 35390, Ille-et-Vilaine, Bretagne, FRANCE,' or x == 'Grand-Fougeray, 35390, Ille-et-Vilaine, Bretagne, FRANCE' or x == 'Le Grand Fougeray, Ille et Vilaine, Bretagne, France' or x == 'Grand-Fougeray, 35390, France':
        r = "Grand-Fougeray, 35124, Ille-et-Vilaine, Bretagne, France"
        g = [47.72403298306091, -1.7313856825114087]
    elif x == 'Grand-Auverné, 44520, France' or x == 'Villehoux - Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France,' or x == 'Le Bourg - Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France' or x == 'Grand-Auverné, 44065, Loire-Atlantique, Pays de la Loire, France' or x == 'Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France,' or x == 'Grand-Auverné Loire-Inférieure  La Haluchère' or x == 'Le Bourg - Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France,' or x == 'Grand Auverné Loire Inférieure, , , ,' or x == 'Villehoux - Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France':
        r = 'Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France'
        g = [47.591728720003445, -1.3297962851808929]
    elif x == 'Gémages, 61130, Orne, Basse-Normandie, France' or x == 'Gémages (61), 61130, Orne, Basse-Normandie, FRANCE' or x == 'Gémages, 61185, Orne, Normandie, FRANCE':
        r = 'Gémages, 61130, Orne, Normandie, France'
        g = [48.29410669580173, 0.6159544072089755]
    elif x == 'Grand-Rullecourt, Pas-de-Calais, France':
        r = 'Grand-Rullecourt, Pas-de-Calais, France'
        g = [0., 0.]
    elif x == 'Guemene Penfao, 44290, Loire-Atlantique, Pays de la Loire, France' or x == 'Guemene Penfao, 44290, Loire-Atlantique, France' or x == 'Guemene Penfao, Loire-Atlantique, France' or x == 'Guemene, Loire-Atlantique, France' or x == 'Guemené Penfao, Loire-Atlantique, France' or x == 'Guémené Chapelle St Georges, Loire-Atlantique, France' or x == 'Guémené Penfao Chapelle Saint Georges, Loire-Atlantique, France' or x == 'Guémené Penfao, Gascaigne, Loire-Atlantique, France' or x == 'Guémené Penfao, Loire-Atlantique, France' or x == 'Guémené, Loire-Atlantique, France' or x == 'Guémené, Penfao, Loire-Atlantique, France' or x == 'Guémené-Penfao, 44067, Bretagne, Loire-Atlantique, France' or x == 'Guémené-Penfao, 44067, Bretagne, gagnen, Loire-Atlantique, France' or x == 'Guémené-Penfao, 44067, Loire-Atlantique, France' or x == 'Guémené-Penfao, 44290, Loire-Atlantique, France' or x == 'Guémené-Penfao, Loire-Atlantique, France' or x == 'Guémené-Penfao,44290, Loire-Atlantique, France' or x == 'Guéméné Penfao, Loire-Atlantique, France' or x == 'Guéméné-Penfao, Loire-Atlantique, France' or x == 'Guéméné-Penfao,44067, Loire-Atlantique, France':
        r = 'Guemene Penfao, 44290, Loire-Atlantique, Pays de la Loire, France'
        g = [47.629877586857795, -1.8332432463456552]


    # // H

    # // I
    elif x == "Issé, 44075, Loire-Atlantique, Pays de la Loire, France" or x == 'Isse, Loire-Atlantique, France' or x == 'Issé 44520, Loire-Atlantique, France' or x == 'Issé, 44075, Loire-Atlantique, France' or x == 'Issé, 44520, Loire- Atlantique, Pays- De- La- Loire, Loire-Atlantique, France' or x == 'Issé, 44520, Loire-Atlantique, France' or x == 'Issé, Loire-Atlantique, France' or x == 'Issé,44520, Loire-Atlantique, France':
        r = "Issé, 44075, Loire-Atlantique, Pays de la Loire, France"
        g = [47.62424618630497, -1.4508212064461499]

    # // J
    elif x == 'Juigné-des-Moutiers  Loire-Atlantique, Pays de la Loire,' or x == 'Juigné-des-Moutiers, 44670, Loire-Atlantique, Pays de la Loire, FRANCE':
        r = 'Juigné-des-Moutiers, 44670, Loire-Atlantique, Pays de la Loire, France'
        g = [47.67886932726545, -1.1853008239988176]
    elif x == 'Jans, 44076, Loire-Atlantique, France' or x == 'Jans, 44170, Loire- Atlantique, Pays- De- La- Loire, Loire-Atlantique, France' or x == 'Jans, 44170, Loire-Atlantique, France' or x == 'Jans, Bretagne, Loire-Atlantique, France' or x == 'Jans, F44170, Loire-Atlantique, France' or x == 'Jans, Loire-Atlantique, France' or x == 'Jans, Ville (La Grand), Loire-Atlantique, France' or x == 'Jans,44076, Loire-Atlantique, France' or x == 'Jans,44076,Pay-de-la-Loire, Loire-Atlantique, France' or x == 'Jans,44170, Loire-Atlantique, France':
        r = 'Jans, 44076, Loire-Atlantique, France'
        g = []

    # // K

    # // L
    elif x == 'Lusanger (44)' or x == 'Lusanger, 44086, Loire-Atlantique, Pays de la Loire, France' or x == 'Lusanger, 44590, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'Lusanger, 44086, Loire Atlantique, Pays de la Loire, France' or x == 'Lusanger, 44590, France':
        r = 'Lusanger, 44086, Loire-Atlantique, Pays de la Loire, France'
        g = [47.68193772699341, -1.5890626460881183]
    elif x == '54, rue de Flore - Le Mans, 72000, Sarthe, Pays de la Loire, FRANCE,' or x == 'Rue du Grand Pont Neuf - Le Mans, 72000, Sarthe, Pays de la Loire, FRANCE' or x == 'Section de la Liberté - Le Mans, 72000, Sarthe, Pays de la Loire, FRANCE' or x == 'Le Mans, 72181, Sarthe, Pays de la Loire, FRANCE' or x == 'Le Mans, 72000, Sarthe, Pays de la Loire, FRANCE,' or x == 'Le Mans, 72000, Sarthe, Pays de la Loire, FRANCE' or x == 'Le Mans, 72181, Sarthe, Pays de la Loire, France,':
        r = 'Le Mans, 72181, Sarthe, Pays de la Loire, France'
        g = [48.000945666098595, 0.19741493633517118]
    elif x == 'La-Chapelle-Souëf, 61099, Orne, Normandie, France,':
        r = 'La-Chapelle-Souëf, 61099, Orne, Normandie, France'
        g = [48.32392834250025, 0.5957966104058483]
    elif x == 'La Milesse, 72650, Sarthe, Pays de la Loire, France,':
        r = 'La Milesse, 72650, Sarthe, Pays de la Loire, France'
        g = [48.062693572698464, 0.1393453859000587]
    elif x == 'Le-Pin-la-Garenne, 61329, Orne, Normandie, France,':
        r = 'Le-Pin-la-Garenne, 61329, Orne, Normandie, France'
        g = [48.44174431005491, 0.5465780664088976]
    elif x == 'Lavardin, 72240, Sarthe, Pays de la Loire, France,':
        r = 'Lavardin, 72240, Sarthe, Pays de la Loire, France'
        g = [48.077712380571455, 0.0629775583827917]
    elif x == 'Lalacelle, 61213, Orne, Normandie, France,' :
        r = 'Lalacelle, 61213, Orne, Normandie, France'
        g = [48.472033544435405, -0.13104258012304476]

    # // M
    elif x == 'MESANGER' or x == 'Mesanger' or x == 'Mesanger, 44, Pays de Loire':
        r = 'Mesanger, 44522, Loire-Atlantique, Pays de Loire, France'
        g = [47.43256918666803, -1.2274308034360966]
    elif x == 'Mouais, 44590, Loire Atlantique, Pays de la Loire':
        r = 'Mouais, 44590, Loire Atlantique, Pays de la Loire, France'
        g = [47.697703969323385, -1.6454071049897794]
    elif x == 'Moisdon la Rivière(44) Denazé, Mayenne, France' or x == 'Moisdon la Rivière, Loire-Atlantique, France' or x == 'Moisdon, Loire-Atlantique, France' or x == 'Moisdon-la-Rivière, 44099, Loire-Atlantique, France' or x == 'Moisdon-la-Rivière, Loire-Atlantique, France' or x == 'Moisdon Loier-Inférieure la Saudiais, , , ,' or x == "Moiddon Loire Inférieure" or  x == 'saint jouin - Moisdon-la-Rivière, 44520, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'Moisdon (Saudiais)' or x == 'Moisdon    Loire Atlantique' or x == 'village de la jannais - Moisdon-la-Rivière, 44520, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'Moisdon-la-Rivière (44)' or x == 'Moisdon  Loire Atlantique' or x == 'Moisdon (Maison Rouesné)' or x == 'village lafaudrais - Moisdon, 44, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'la Planche - Moisdon-la-Rivière, 44099, Loire-Atlantique, Pays de la Loire, France,' or x == 'Moisdon-la-Rivière, 44520, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'Moisdon la Rivière Loire Atlantique,' or x == 'La Gagnerie  Moisdon    Loire Atlantique,' or x == 'Moisdon Loire Inférieure, , , ,' or x == 'saint jouin - Moisdon, 44, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'La Pinaye Moisdon    Loire Atlantique,' or x == 'Moisdon' or x == 'Moisdon Loire Atlantique  la Saudiais' or x == 'Moisdon (La Rivière) Loire Atlantique' or x == 'Moisdon    Loire Atlantique,' or x == 'Moisdon, 44, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'la Maison Rouéné  Moisdon Loire Inférieure' or x == 'Moisdon Loire Inférieure' or x == 'Moisdon Loier-Inférieure' or x == 'Moisdon Loire Inférieure la Gagnerie, , , ,,' or x == 'la gagnerie - Moisdon, 44, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'la Rivière aux Garnier   Moisdon  Loire Atlantique,' or x == 'Moisdon Loire-Inférieure Denazé, , , ,,' or x == 'village de la vinain - Moisdon-la-Rivière, 44520, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'Moisdon Loire Atlantique' or x == 'La Planche  Moisdon la Rivière Loire Atlantique,' or x == 'Moisdon   Loire Atlantique,' or x == 'Moisdon Loire Inférieure    la Pinaye,' or x == 'Moisdon Loier-Inférieure la Saudiais, , , ,,' or x == 'Moisdon (La Rivière) Loire Atlantique,' or x == 'Moisdon la Rivière Loire Atlantique la Boulaie, , , ,,' or x == 'Moisdon la Rivière Loire-Inférieure, , , ,' or x == 'la saudraye - Moisdon-la-Rivière, 44099, Loire-Atlantique, Pays de la Loire, France' or x == 'Moisdon, 44, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'Moisdon,' :
        r = 'Moisdon-la-Rivière, 44099, Loire-Atlantique, Pays de la Loire, France'
        g = [47.62261363520462, -1.3759768678012587]
    elif x == 'Mézières-sous-Lavardin, 72197, Pays de la Loire, France,' or x == 'le Bourg - Mézières-sous-Lavardin, 72197, Pays de la Loire, France,' or x == 'Mézières-sous-Lavardin, 72197, Sarthe, Pays de la Loire, France,' or x == 'Mézières-sous-Lavardin, 72197, Pays de la Loire, France' or x == 'Chartes - Mézières-sous-Lavardin, 72197, Sarthe, Pays de la Loire, France,' or x == 'Chartes - Mézières-sous-Lavardin, 72197, Pays de la Loire, France,' or x == 'Chartes - Mézières-sous-Lavardin, 72197, Sarthe, Pays de la Loire, France' or x == 'Chartes - Mézières-sous-Lavardin, 72197, Pays de la Loire, France':
        r = 'Mézières-sous-Lavardin, 72197, Sarthe, Pays de la Loire, France'
        g = [48.155172721331894, 0.029417144782574768]
    elif x == 'Mont St Jean, 72, Sarthe, France,' or x == 'Mont St Jean, 72, Sarthe, France':
        r = 'Mont St Jean, 72211, Sarthe, Pays de la Loire, France'
        g = [48.24630468649458, -0.1072229173274874]
    elif x == 'Mauves-sur-Huisne, 61255, Orne, Normandie, France,':
        r = 'Mauves-sur-Huisne, 61255, Orne, Normandie, France'
        g = [48.44890702792295, 0.620764350193877]
    elif x == 'Moutiers-au-Perche, 61300, Orne, Normandie, France,':
        r = 'Moutiers-au-Perche, 61300, Orne, Normandie, France'
        g = [48.47581578244536, 0.8479496656852]

    # // N
    elif x == 'Neuvillalais, 72' or x == 'Neuvillalais, 72216, Sarthe, Pays de la Loire, Fra' or x == 'Neuvillalais, 72216, Pays de la Loire, France' or x == 'Neuvillalais, 72240, Sarthe, Pays de la Loire, FRANCE' or x == 'Neuvillalais, 72216, Pays de la Loire, France,':
        r = 'Neuvillalais, 72216, Sarthe, Pays de la Loire, France'
        g = [48.15514260233994, -0.0002471628054206737]
    elif x == 'Nort sur Erdre Loire-Inférieure St Georges, , , ,' or x == 'Nort-sur-Erdre, 44110, Loire Atlantique, Pays de la Loire, France,' or x == 'Faubourg St Georges  Nort sur Erdre Loire-Inférieure,' or x == 'Nort-Sur-Erdre,' or x == 'Nort-Sur-Erdre' or x == 'Nort sur Erdre Loire Atlantique la Pancarte,' or x == 'St Georges  Nort sur Erdre Loire-Inférieure' or x == 'St Georges Nort sur Erdre Loire Atlantique' or x == 'Nort sur Erdre Loire-Inférieure St Georges,' or x == 'Nort sur Erdre Loire-Inférieure St Georges, , , ,,' or x == 'Nort-Sur-Erdre (Saint-Georges)' or x == 'St Georges Nort (sur Erdre) Loire-Inférieure' or x == 'Nort-Sur-Erdre (Saint-Georges),' or x == 'St Georges Nort sur Erdre Loire Atlantique,':
        r = 'Nort-sur-Erdre, 44110, Loire Atlantique, Pays de la Loire, France'
        g = [47.43865900956249, -1.4998854281797938]
    elif x == 'Nantes 44000, Loire-Atlantique, France' or x == 'Nantes Chantenay, Loire-Atlantique, France' or x == 'Nantes, 44000, Loire-Atlantique, France' or x == 'Nantes, 44109, Loire-Atlantique, France' or x == 'Nantes, Devenu Loire Atlantique, Loire-Atlantique, France' or x == 'Nantes, Doulon, Loire-Atlantique, France' or x == 'Nantes, Loire-Atlantique, France' or x == 'Nantes, Saint Similien (Saint Sambin), Loire-Atlantique, France' or x == 'Nantes, Saint Similien, Loire-Atlantique, France' or x == 'Nantes, Saint-Donatien, Loire-Atlantique, France' or x == 'Nantes, la Perverie, Loire-Atlantique, France' or x == 'Nantes, \x86 Saint-Donatien, Loire-Atlantique, France' or x == 'Nantes,44000, Loire-Atlantique, France' or x == 'Nantes-Doulon,44000, Loire-Atlantique, France' or x == 'Nantes, 44000, Loire Atlantique, Pays de la Loire, France,' or x == "tes, 44109, Loire-Atlantique, France" or x == "Nantes, 44109, Loire-Atlantique, France" or x == 'Nantes, 44109, Loire-Atlantique, Pays de la Loire, France,' or x == 'Nantes 2ème,' or x == 'Nantes. Saint Donatien' or x == 'Nantes,  Loire Atlantique 2è canton,':
        r = "Nantes, 44000, Loire Atlantique, Pays de la Loire, France"
        g = [47.22048468387292, -1.5520975173687117]

    # // O

    # // P
    elif x == 'Petit-Auverne, 44121, Loire-Atlantique, France' or x == 'Petit-Auverné, 44121, Loire Atlantique, Pays de la Loire, France,' or x == 'Le Bourg - Petit-Auverné, 44121, Loire Atlantique, Pays de la Loire, France' or x == 'Le Bourg - Petit-Auverné, 44670, Loire Atlantique, Pays de la Loire, France' or x == 'Le Bourg - PETIT AUVERNE, F44670, PDL, FRANCE,' or x == 'Petit-Auverné, 44121, Loire Atlantique, Pays de la' or x == 'Petit-Auverné, 44121, Loire Atlantique, Pays de la Loire, France' or x == 'Petit-Auverné, 44670, Loire-Atlantique, Pays de la Loire, FRANCE':
        r = "Petit-Auverné, 44121, Loire-Atlantique, Pays de la Loire, France"
        g = [47.60957739836478, -1.2914942961474298]
    elif x == 'Pizieux, 72600, France':
        r = 'Pizieux, 72238, Sarthe, Pays de la Loire, France'
        g = [48.32291678170826, 0.33173115696573524]
    elif x == 'Le Pin, 44124, Loire Atlantique, Pays de la Loire':
        r = 'Le Pin, 44124, Loire Atlantique, Pays de la Loire, France'
        g = [47.59097969785115, -1.1520256971382625]
    elif x == 'Plessé, 44128, Loire Atlantique, Pays de la Loire':
        r = 'Plessé, 44128, Loire Atlantique, Pays de la Loire, France'
        g = [47.53967748727911, -1.8865598220667976]
    elif x == 'Panon, 72600, Sarthe'or x == 'Panon, 72227, Sarthe, Pays de la Loire, France':
        r = 'Panon, 72600, Sarthe, Pays de la Loire, France'
        g = [48.3378307055659, 0.29464078758508455]
    elif x == 'Paris, 75000, Île-de-France, FRANCE,' or x == '15e - Paris 15e  Arrondissement, 75015, Paris, Île-de-France, FRANCE,' or x == '14e - Paris 14e Arrondissement, 75014, Paris, Île-de-France, FRANCE,' or x == '5 rue Blanche - Paris 09, 75009, Seine, Île de France, FRANCE,' or x == '14e - Paris 14e Arrondissement, 75014, Paris, Île-de-France, FRANCE' or x == 'Paris, 75000, Île-de-France, FRANCE':
        r = "Paris, 75000, Paris, Île-de-France, France"
        g = [48.85905136925032, 2.339478787408999]
    elif x == "Pruillé l'Eguillé,Sarthe,France ?" or x == "janv 1777 (voir notes)) - Pruillé l'Eguillé,Sarthe,France ?" or x == "Pruillé l'Eguillé,Sarthe,France (À fils François)" or x == "Pruillé l'Eguillé,Sarthe,France" or x == "Pruillé l'Eguillé,Sarthe,France,":
        r = "Pruillé l'Eguillé, 72248, Sarthe, Pays de la Loire, France"
        g = [0.0, 0.0]
    elif x == 'Préaux-du-Perche, 61340, Orne, Basse-Normandie, France,' or x == 'Préaux-du-Perche, 61337, Orne, Normandie, FRANCE' or x == 'Préaux-du-Perche, 61337, Orne, Normandie, FRANCE,' or x == 'Préaux-du-Perche, 61340, Orne, Basse-Normandie, France' or x == 'Préaux-du-Perche (61), 61340, Orne, Basse-Normandie, FRANCE,' or x == 'Preaux, 61340, Orne, Basse-Normandie, France':
        r = 'Préaux-du-Perche, 61337, Orne, Normandie, France'
        g = [0.0, 0.0]

    # // Q

    # // R
    elif x == 'renazé, 53188, Mayenne, Pays de la Loire, France':
        r = 'Renazé, 53188, Mayenne, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'René, 72251, Sarthe, Pays de la Loire, France' or x == 'René, 72260, France':
        r = 'René, 72260, Sarthe, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Reze, Loire-Atlantique, France' or x == 'Rezé les Nantes, Loire-Atlantique, France' or x == 'Rezé les Nantes,44400, Loire-Atlantique, France' or x == 'Rezé lès Nantes, Loire-Atlantique, France' or x == 'Rezé, 44143, Loire-Atlantique, France' or x == 'Rezé, 44143, Pays de la Loire FRANCE, Loire-Atlantique, France' or x == 'Rezé, 44400, Loire-Atlantique, France' or x == 'Rezé, Loire-Atlantique, France' or x == 'Rezé, Saint-Pierre, Loire-Atlantique, France' or x == 'Rezé,44400, Loire-Atlantique, France' or x == 'Rezé, 44143, Loire-Atlantique, France':
        r = 'Rezé, 44143, Loire-Atlantique, France'
        g = [0.0, 0.0]

    # // S
    elif x == 'Sion-les-Mines, Loire-Atlantique, France' or x == 'Les Vallées - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'Le Gripay - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'La Mustais - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'La Mustais - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'Le Gripay - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'La Granville - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'La Hunaudière - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == 'Sion les Mines (44),' or x == 'La Hunaudière - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'Le Pont - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE' or x == 'La Chauvais - Sion-les-Mines, 44590, Loire-Atlantique, Pays de la Loire, FRANCE,' or x == "Sion les Mines (44)" or x == "Sion Les Mines, Loire Atlantique, France" or x =="Sion les Mines, 44590, Loire Atlantique, Pays de Loire, FRANCE":
        r =  "Sion-les-Mines, 44197, Loire-Atlantique, Pays de la Loire, France"
        g = [0.0, 0.0]
    elif x == 'Saint-Julien-De-Vouvantes, 44670, Loire-Atlantique, France' or x == 'Saint-Julien-de-Vouvantes 44170, Pays de la Loire France, Loire-Atlantique, France' or x == 'Saint-Julien-de-Vouvantes, 44170, Loire-Atlantique, France' or x == 'Saint-Julien-de-Vouvantes, 44670, Bretagne, Loire-Atlantique, France' or x == 'Saint-Julien-de-Vouvantes, 44670, Loire-Atlantique, France' or x == 'Saint-Julien-de-Vouvantes, Loire-Atlantique, France' or x == 'Saint-Julien-de-Vouvantes,44170, Loire-Atlantique, France' or x == 'Saint-Julien-de-Vouvantes, 44170, Loire Atlantique, Pays de la Loire, France' or x == 'Saint-Julien-de-Vouvantes, 44670, Loire-Atlantique, Pays de la Loire, FRANCE':
        r = 'Saint-Julien-de-Vouvantes, 44670, Loire Atlantique, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Rémy-du-Plain, 72317, Sarthe, Pays de la Loire, France,' or x == 'Saint-Rémy-du-Plain, France' or x == 'saint rémy du plain 72' or x == 'St Remy du Plain, Sarthe, France' or x == 'Saint-Rémy du Plain, Sarthe, Pays de la Loire, France,' or x == 'Saint-Rémy-du-Plain, 72317, Sarthe, Pays de la Loire, France':
        r = "Saint-Rémy-du-Plain, 72317, Sarthe, Pays de la Loire, France"
        g = [0.0, 0.0]
    elif x =='Saint-Hilaire-de-Chaleons, 44164, Loire-Atlantique, France' or x == "Saint-Hilaire-de-Chaléons, 44164, Loire Atlantique, Pays de la Loire, France" or x == 'La Richerie - St Hilaire de Chaléons, 44' or x == 'La Richerie - St Hilaire de Chaléons, 44,' or x == 'Noyeux - St Hilaire de Chaléons, 44,' or x == 'St Hilaire de Chaléons, 44,' or x == 'St Hilaire de Chaléons, 44' or x == 'Village de la Richerie, Saint-Hilaire-de-Chaléons, 44164, Loire Atlantique, Pays de la Loire, France,':
        r = "Saint-Hilaire-de-Chaléons, 44164, Loire Atlantique, Pays de la Loire, France"
        g = [47.10218003883818, -1.86779332795036]
    elif x == 'Saint-Sulpice-des-Landes, 44540, Loire Atlantique, Pays de la Loire, France':
        r = 'Saint-Sulpice-des-Landes, 35316, Ille-et-Vilaine, Bretagne, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Vincent-des-Landes, 44590, France' :
        r = 'Saint-Vincent-des-Landes, 44193, Loire-Atlantique, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Longis, 72600, France':
        r = 'Saint-Longis, 72295, Sarthe, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Cyr-la-Rosière, 61130, Orne, Basse-Normandie, France' or x == 'Saint-Cyr-la-Rosière, 61379, Orne, Normandie, FRANCE,' or x == 'Saint-Cyr-la-Rosière, 61130, Orne, Normandie, FRANCE' or x == 'Saint-Cyr-la-Rosière, 61379, Orne, Normandie, FRANCE' or x == 'Saint-Cyr-la-Rosière, 61379, Basse Normandie, France,' or x == 'Saint Cyr la Rosière 61, Orne, Basse Normandie, France' or x == 'Sainte-Gauburge-de-la-Coudre - Saint-Cyr-la-Rosière, 61379, Orne, Normandie, France' or x == 'Saint Cyr la Rosière 61, Orne, Basse Normandie, France,' or x == 'Saint-Cyr-la-Rosière, 61379, Basse Normandie, France' or x == 'Saint-Cyr-la-Rosière, 61130, Orne, Normandie, FRANCE,':
        r = 'Saint-Cyr-la-Rosière, 61130, Orne, Normandie, France'
        g = [0.0, 0.0]
    elif x == 'St Etienne de Mer Morte, 44':
        r = 'Saint-Étienne-de-Mer-Morte, 44157, Loire Atlantique, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Soudan Loire Atlantique village de Fontenay' or x == 'Soudan Loire-Inférieure Corbière, , , ,,' or x =='Soudan LoireAtlantique  le Bois Gerbaud,':
        r = 'Soudan, 44199, Loire Atlantique, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'la botterie - Saint-Ouen-de-Mimbré, 72305, Sarthe, Pays de la Loire, France'or x == 'La Hoterie - Saint-Ouen-de-Mimbré, 72305, Pays de la Loire, France,'or x == 'Saint-Ouen-de-Mimbré, 72305, Pays de la Loire, France,'or x == 'Saint-Ouen-de-Mimbré, 72305, Sarthe, Pays de la Loire, France,'or x == 'Saint-Ouen-de-Mimbré, 72305, Pays de la Loire, France':
        r ='Saint-Ouen-de-Mimbré, 72305, Sarthe, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Sainte-Jamme-sur-Sarthe, 72380, Sarthe, Pays de la Loire, FRANCE,':
        r = 'Sainte-Jamme-sur-Sarthe, 72380, Sarthe, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Germain-de-la-Coudre,Orne,Normandie,France,' or x == 'Saint-Germain-de-la-Coudre, 61394, Orne, Basse-Normandie, France':
        r ='Saint-Germain-de-la-Coudre, 61394, Orne, Normandie, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Germain-des-Grois,61110,Orne,Basse-Normandie,FRANCE,' or x == 'Saint-Germain-des-Grois,61110,Orne,Basse-Normandie,FRANCE':
        r = 'Saint-Germain-des-Grois, 61395, Orne, Normandie, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Aubin-des-Grois, 61368, Orne, Normandie, France,':
        r = 'Saint-Aubin-des-Grois, 61368, Orne, Normandie, France'
        g = [0.0, 0.0]
    elif x == 'Saint-Nazaire,44600, Loire-Atlantique, France':
        r = 'Saint-Nazaire,44600, Loire-Atlantique, France'
        g = [0., 0.]

    # // T

    # // U

    # // V
    elif x == 'Villaines-la-Carelle, 72374, Sarthe, Pays de la Loire, France,':
        r = 'Villaines-la-Carelle, 72374, Sarthe, Pays de la Loire, France'
        g = [0.0, 0.0]
    elif x == 'Verrières, 61501, Orne, Normandie, FRANCE' or x == 'Verrières, Orne, France':
        r = 'Verrières, 61501, Orne, Normandie, France'
        g = [0.0, 0.0]
    elif x == 'Congé des Guérets - Vivoin, 72380, Sarthe, Pays de la Loire, France,' or x == 'Les Bourgeons - Vivoin, 72380, Sarthe, Pays de la Loire, France' or x == 'Vivoin, 72380, Sarthe, Pays de la Loire, France' or x == 'Vivoin (sarthe)':
        r = 'Vivoin, 72380, Sarthe, Pays de la Loire, France'
        g = [0.0, 0.0]

    # // W

    # // X

    # // Y

    # // Z  
        

    else:
        #r = f"[X] {x}"
        r = x
        g = [0.0, 0.0]
        pass
    return r, g


# %%

'(14ème arrondissement), Paris, Paris, France',
'(Barel), Blain, Loire-Atlantique, France',
'(Beslé) Guémené-Penfao, Loire-Atlantique, France',
'(Bretagne), Lusanger, Loire-Atlantique, France',
'(Cuneix) Saint-Nazaire, 44600, Loire-Atlantique, France',
'(Cuneix) Saint-Nazaire,44600, Loire-Atlantique, France',
'(Les Fréteauderies), Savenay, Loire-Atlantique, France',
'(Sainte-Anne) Saint-Dolay,56130, Morbihan, France',
'(Trelu) Missillac,44780, Loire-Atlantique, France',
'(Village de Kernevy) Saint-Dolay,56130, Morbihan, France',
'(Village de Sautron) Saint-Nazaire,44600, Loire-Atlantique, France',
'(Village du Cressin) Nivillac,56130, Morbihan, France',
'3e Canton, Loire-Atlantique, France',
'44170 Jans, Loire-Atlantique, France',
'44170 Treffieux, Loire-Atlantique, France',
'44290,, Guémené-Penfao, Loire-Atlantique, France',
'44520, Loire-Atlantique, France',
'44590 Saint Vincent des Landes, Loire-Atlantique, France',
'44670, Saint Julien de Vouvantes, Loire-Atlantique, France',

'A Guemene Penfao 44290, Loire-Atlantique, France',



'Albert-la-Boisselle, Somme, France',
'Ancenis, 44003, Loire-Atlantique, France',
'Augrain, Saffre 44390, Loire-Atlantique, France',
'Avant, France',




x == 'Abbaretz, 44001, Loire-Atlantique, France' or x == 'Abbaretz, 44170, Loire-Atlantique, France' or x == 'Abbaretz, Loire-Atlantique, France' or 
x == 'Arthon en retz, Loire-Atlantique, France' or x == 'Arthon, 44320, Loire-Atlantique, France' or x == 'Arthon, Loire-Atlantique, France' or x == 'Arthon-en-Retz, 44005, Loire-Atlantique, France' or x == 'Arthon-en-Retz, 44320, Loire-Atlantique, France' or x == 'Arthon-en-Retz, Loire-Atlantique, France' or 
x == 'Asserac, Loire-Atlantique, France' or x == 'Assérac (Azereg), 44410, Loire-Atlantique, France' or x == 'Assérac, 44006, Bretagne, Loire-Atlantique, France' or x == 'Assérac, 44006, Loire-Atlantique, France' or x == 'Assérac, 44410, Loire-Atlantique, France' or x == 'Assérac, Dpt, Loire-Atlantique, France' or x == 'Assérac, Loire-Atlantique, France' or x == 'Assérac, Loire-Inférieure, Loire-Atlantique, France' or x == 'Assérac,44410, Loire-Atlantique, France' or 
x == 'Avessac, 44007, Bretagne, Loire-Atlantique, France' or x == 'Avessac, 44007, Loire-Atlantique, France' or x == 'Avessac, 44460, Loire-Atlantique, France' or x == 'Avessac, Loire-Atlantique, France' or 
x == 'BESLÉ sur VILAINE, 44290, Loire-Atlantique, France' or x == 'Besle sur Vilaine 44290, Loire-Atlantique, France' or x == 'Besle sur Vilaine, 44294, Loire Inférieur, Saint Nazaire, Loire-Atlantique, France' or x == 'Besle sur Vilaine, Loire-Atlantique, France' or x == 'Beslé' or x == 'Beslé (-sur-Vilaine), 44067, Bretagne, Loire-Atlantique, France' or x == 'Beslé (-sur-Vilaine), 44067, Bretagne, la fillette, Loire-Atlantique, France' or x == 'Beslé sur Vilaine, 44291, Loire-Atlantique, France' or x == 'Beslé sur Vilaine, Loire-Atlantique, France' or x == 'Beslé sur Vilaines, Loire-Atlantique, France' or x == 'Beslé, Guémené-Penfao, 44067, Bretagne, Loire-Atlantique, France' or x == 'Beslé-sur-Vilaine, Loire-Atlantique, France' or 
x == 'Bourgneuf en Retz, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, 44021, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, 44580, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, Nombreuil, Bourgneuf-en-Retz, Loire-Atlantique, France' or 






'Batz-sur-Mer, 44010, Loire-Atlantique, France',
'Batz-sur-Mer, 44740, Loire-Atlantique, France',


'Belligné, 44011, Loire-Atlantique, France',



'Bouguenais, 44020, Loire-Atlantique, France',
'Bouguenais, 44340, Loire-Atlantique, France',



'Boussay, 44022, Loire-Atlantique, France',
'Boussay, 44190, Loire-Atlantique, France',


'Bouvron, 44023, Loire-Atlantique, France',
'Bouvron, 44130, Loire-Atlantique, France',
'Bouvron, 54200, Meurthe-et-Moselle, France',
'Bouvron, Loire-Atlantique, France',


'Bouée, 44019, Loire-Atlantique, France',
'Bouée, Bretagne, Loire-Atlantique, France',


'Brest, 29019, Finistère, France',
'Brest, 29200, Finistère, France',


'Camoel, Morbihan, France',

'Campbon, 44750, Loire-Atlantique, France',
'Case-Pilote, 97222, Martinique, Martinique',

'Champtocé-sur-Loire, 49068, Maine-et-Loire, France',
'Champtocé-sur-Loire, Maine-et-Loire, France',

'Chantenay nantes, Loire-Atlantique, France',
'Chantenay sur Loire',
'Chantenay, Loire-Atlantique, France',
'Chantenay, Nantes, 44109, Loire-Atlantique, France',
'Chantenay, Pays de la Loire, France',

'Chateau-Gontier, 53062, Mayenne, France',
'Chateaubriant, Loire-Atlantique, France',
'Chatelais, 49081, Maine-et-Loire, France',
'Chatelet Maine et Loire, France',
'Chauche, 85064, Vendée, France',
'Chauvé, 44320, Loire-Atlantique, France',
'Chauvé, Loire-Atlantique, France',
'Chizé, Deux-Sèvres, France',
'Cholet, 49099, Maine-et-Loire, France',
'Châteaubriant, 44036, Loire-Atlantique, France',
'Châteaubriant, 44110, Loire-Atlantique, France',
'Châtelais, 49081, Maine-et-Loire, France',
'Chéméré, 44040, Loire-Atlantique, France',
'Chéméré, 44680, Loire-Atlantique, France',
'Chéméré, Loire-Atlantique, France',
'Clion sur mer,44042, Loire-Atlantique, France',
'Coisfoux,Guéméné-Penfao, Loire-Atlantique, France',
'Concarneau, 29039, Finistère, France',
'Concarneau, 29900, Finistère, France',
'Conquereuil, 44044, Loire-Atlantique, France',
'Conquereuil, Loire-Atlantique, France',
'Cordemais, 44045, Loire-Atlantique, France',
'Cordemais, 44360, Loire-Atlantique, France',
'Corsept, Loire-Atlantique, France',
'Coueron, Loire-Atlantique, France',
'Couëron, 440047, Loire-Atlantique, France',
'Couëron, 44047, Loire-Atlantique, France',
'Couëron, 44220, Loire-Atlantique, France',
'Couëron, Loire-Atlantique, France',
'Coësmes, 35000, Ille-et-Vilaine, France',
'Crossac, 44050, Loire-Atlantique, France',
'Crossac, 44160, Loire-Atlantique, France',
'Crossac, Loire-Atlantique, France',
'Céret, 66049, Pyrénées-Orientales, France',
'DOULON, Diocèse de Nantes, Loire-Atlantique, France',





'Donges, 44480, Loire-Atlantique, France',
'Donges, Loire-Atlantique, France',

'Doulon (Saint Médard), 44109, Loire-Atlantique, France',
'Doulon, Diocèse de Nantes, Bretagne, Loire-Atlantique, France',
'Doulon, Loire-Atlantique, France',

'Dreffeac, Loire-Atlantique, France',
'Dréfféac, Loire-Atlantique, France',





'FROSSAY, Diocèse de Nantes, Loire-Atlantique, France',
'Fabrègues, 34690, Hérault, France',





'Fercé, 44660, Loire-Atlantique, France',
'Fleche (La)',
'Fresnay-en-Retz, 44059, Loire-Atlantique, France',
'Frossay,44320, Loire-Atlantique, France',
'Fégréac, 44057, Loire-Atlantique, France',
'Fégréac, 44460, Loire-Atlantique, France',
'Fégréac, Henrieux, Fégréac, Loire-Atlantique, France',
'Fégréac, Loire-Atlantique, France',
'Fégréac,44460, Loire-Atlantique, France',
'Gaubretiere, 85097, Vendée, France',


'Grand Auverné, Loire-Atlantique, France',
'Grand-Auverné, 44520, Loire-Atlantique, France',
'Grand-Auverné, Loire-Atlantique, France',



'Grand Fougeray, Ille-et-Vilaine, France',
'Grand-Fougeray, 35124, Ille-et-Vilaine, France',
'Grand-Fougeray, 35390, Ille-et-Vilaine, France',



'Grand-Rullecourt, 62385, Pas-de-Calais, France',
'Grand-Rullecourt, 62810, Pas-de-Calais, France',
'Grand-Rullecourt, Pas-de-Calais, France',







'Guenrouet, 44068, Loire-Atlantique, France',
'Guenrouet, 44530, Loire-Atlantique, France',
'Guenrouët, 44068, Bretagne, Loire-Atlantique, France',
'Guenrouët, 44530, Loire-Atlantique, France',
'Guenrouët, Loire-Atlantique, France',

'Guerande, Loire-Atlantique, France',
'Guidel, 56078, Morbihan, France',
'Guiscard, 60291, Oise, France',

'Guénouvry,44914, Loire-Atlantique, France',
'Guérande, 44069, Loire-Atlantique, France',
'Guérande, 44350, Loire-Atlantique, France',
'Guérande, Loire-Atlantique, France',
'Guérande,44350, Loire-Atlantique, France',
'Hanvec, 29460, Finistère, France',

'Herbignac, 44072, Loire-Atlantique, France',
'Herbignac, 44410, Loire-Atlantique, France',
'Herbignac, Bretagne, Loire-Atlantique, France',
'Herbignac, Dpt, Loire-Atlantique, France',
'Herbignac, Loire-Atlantique, France',
'Herbignac,44410, Loire-Atlantique, France',

'Hospice Saint-Julien-de-Vouvantes, 44170, Loire-Atlantique, France',

'Heric, Loire-Atlantique, France',
'Héric, 44073, Loire-Atlantique, France',
'Héric, 44810, Loire-Atlantique, France',
'Héric, Loire-Atlantique, France',






'Joué sur Erdre, 44440, Loire-Atlantique, France',
'Joué, Loire-Atlantique, France',
'Joué-sur-Erdre, 44440, Loire-Atlantique, France',
'Joué-sur-Erdre, Loire-Atlantique, France',
'Joué-sur-Erdre,44077, Loire-Atlantique, France',
'Joué/Erdre, 44077, Bretagne, Loire-Atlantique, France',

'Kerhoux, Nivillac, Morbihan, France',
"L'Auvière, Le Clion sur Mer, 44210, 440042, Loire-Atlantique, France",
'La Baule-Escoublac, 44055, Loire-Atlantique, France',
'La Bernerie-En-Retz, Loire-Atlantique, France',
'La Bernerie-en-Retz, 44012, Loire-Atlantique, France',
'La Bernerie-en-Retz, 44760, Loire-Atlantique, France',
'La Bernerie-en-Retz, Loire-Atlantique, France',
'La Beusse, Sainte-Pazanne, 44680, Loire-Atlantique, France',
'La Binguenais, Issé, 44075, Loire-Atlantique, France',
'La Binquenais, Issé, 44075, Loire-Atlantique, France',
'La Boisselle, 80300, Somme, France',
'La Boisselle, Somme, France',
'La Bourrelière Vertou, 44215, Loire-Atlantique, France',
'La Bruffière, 85039, Vendée, France',
'La Chapelle Launay, 44260, Loire-Atlantique, France',
'La Chapelle-Basse-Mer, 44450, Loire-Atlantique, France',
'La Chapelle-Glain, 44031, Loire-Atlantique, France',
'La Chapelle-Heulin, Loire-Atlantique, France',
'La Chapelle-Launay, 44260, Loire-Atlantique, France',
'La Chapelle-Launay, Loire-Atlantique, France',
'La Chapelle-Saint-Sauveur, 44370, Loire-Atlantique, France',
'La Chapelle-sur-Erdre, 44035, Loire-Atlantique, France',
'La Chevrolière, Loire-Atlantique, France',
'La Devairie, Le Clion-sur-Mer, Pornic, 44131, Loire-Atlantique, France',
'La Dominelais, 35098, Ille-et-Vilaine, France',
'La Dominelais, 35390, Ille-et-Vilaine, France',
'La Dréallière, Arthon-en-Retz, 44005, Loire-Atlantique, France',
'La Garnache, Vendée, France',
'La Gaubretiere, 85097, Vendée, France',
'La Gommerais, Treffieux, 44208, Loire-Atlantique, France',
'La Hunaudière, Sion-les-Mines, 44197, Loire-Atlantique, France',
'La Limouzinière, 44310, Loire-Atlantique, France',
'La Magdeleine, Saint-Vincent-des-Landes, 44193, Loire-Atlantique, France',
'La Marzelle, Saint-Mars-de-Coutais, 44680, Loire-Atlantique, France',
'La Meilleraye de Bretagne, Loire-Atlantique, France',
'La Meilleraye, Loire-Atlantique, France',
'La Meilleraye-de-Bretagne, 44095, Loire-Atlantique, France',
'La Meilleraye-de-Bretagne, Loire-Atlantique, France',
'La Mulçonnais, Saint-Vincent-des-Landes, 44193, Loire-Atlantique, France',
'La Roche-André, Soudan, 44199, Loire-Atlantique, France',
'La Roche-Bernard, 56130, Morbihan, France',
'La Roche-Bernard, 56195, Morbihan, France',
'La Rouxière, 44147 / 44370, Loire-Atlantique, France',
'La Rouxière, 44147, Loire-Atlantique, France',
'La Rouxière, 44370, Loire-Atlantique, France',
'La Rouxière, Loire-Atlantique, France',
'La Selle-Craonaise, Mayenne, France',
'La Selle-Craonnaise, Mayenne, France',
'La Selle-Craonnaise,53258, Mayenne, France',
'La Ville-ès-Nonais, 35358, Ille-et-Vilaine, France',
'La-Chapelle-sur-Erdre, Loire-Atlantique, France',
'Laval, Mayenne, France',
'Laval,53130, Mayenne, France',
'Le Bois-Gerbaud, Soudan, 44199, Loire-Atlantique, France',
'Le Bourg, Port-Saint-Père, 44710, Loire-Atlantique, France',
'Le Chêne, Vertou, 44215, Loire-Atlantique, France',


'Le Clion Sur Mer 44042, Loire-Atlantique, France',
'Le Clion sur Mer, 44210, 440042, Loire-Atlantique, France',
'Le Clion sur Mer, 44210, Loire-Atlantique, France',
'Le Clion sur Mer, Loire-Atlantique, France',
'Le Clion sur mer, Loire-Atlantique, France',
'Le Clion-sur-Mer, 44210, Loire-Atlantique, France',
'Le Clion-sur-Mer, Pornic, 44131, Loire-Atlantique, France',
'Le Clion-sur-mer,44210, Loire-Atlantique, France',


'Le Croisic, 44049, Loire-Atlantique, France',
'Le Croisic, Loire-Atlantique, France',
'Le Fresne-sur-Loire, Loire-Atlantique, France',
'Le Haut Trémorel, Herbignac, 44410, Loire-Atlantique, France',
'Le Mans, 72181, Sarthe, France',
'Le Mans,72000, Pays de le Loire, Sarthe, France',
'Le Pouliguen, 44135, Loire-Atlantique, France',
'Le Temple-de-Bretagne, 44360, Loire-Atlantique, France',
'Les Essarts 85140, Vendée, France',
'Les Essarts, 85084, Vendée, France',
'Les Glands, Blain, 44015, Loire-Atlantique, France',
'Les Magnils-Reigniers, 85400, Vendée, France',
'Les Moutiers-en-Retz, Loire-Atlantique, France',
'Ligné, 44001, Loire-Atlantique, France',
'Ligné, 44082, Loire-Atlantique, France',
'Ligné, 44850, Loire-Atlantique, France',
'Ligné, Loire-Atlantique, France',
'Limeil-Brévannes, 94044, Val-de-Marne, France',
'Limerzel, 56111, Morbihan, France',
'Limerzel, Morbihan, France',
'Lorient, 56100, Morbihan, France',
'Lorient, 56121, Morbihan, France',
'Lusanger, 44086, Loire-Atlantique, France',
'Lusanger, 44590, Loire-Atlantique, France',
'Lusanger, Loire-Atlantique, France',
'Lusanger,44590, Loire-Atlantique, France',
'Marsac sur Don, Saint Martin, Loire-Atlantique, France',
'Marsac, 44170, Loire-Atlantique, France',
'Marsac-sur-Don, 44091, France le Verger, Loire-Atlantique, France',
'Marsac-sur-Don, 44091, Loire-Atlantique, France',
'Marsac-sur-Don, 44091, Pays de l Loire, Loire-Atlantique, France',
'Marsac-sur-Don, 44170, Loire-Atlantique, France',
'Marsac-sur-Don, Loire-Atlantique, France',
'Marsac/don, Loire-Atlantique, France',
"Maël-Carhaix, 22137, Côtes-d'Armor, France",
'Meaux, 77100, Seine-et-Marne, France',
'Meaux, 77284, Seine-et-Marne, France',
'Mesquer, 44097, Loire-Atlantique, France',
'Messac, 35480, Ille-et-Vilaine, France',
'Mirebeau, 86160, Vienne, France',
'Missillac (Saint Paul), 44780, Loire-Atlantique, France',
'Missillac, 44098, Bretagne, Leandeuc, Loire-Atlantique, France',
'Missillac, 44098, Loire-Atlantique, France',
'Missillac, 44780, Loire-Atlantique, France',
'Missillac, Les Handeux 44098, Loire-Atlantique, France',
'Missillac, Loire-Atlantique, France',
'Missillac,44098, Loire-Atlantique, France',
'Misssillac, Loire-Atlantique, France',








'Montbert, 44140, Loire-Atlantique, France',
'Montbert, Loire-Atlantique, France',
'Montfaucon-Montigné, 49230, Maine-et-Loire, France',
'Montoir de Bretagne, Loire-Atlantique, France',
'Montrelais, 44104, Loire-Atlantique, France',
'Mouais, 44105, Loire-Atlantique, France',
'Mouais, Loire-Atlantique, France',
'Mouzeil, 44107, Loire-Atlantique, France',
'Mouzeil, 44850, Loire-Atlantique, France',
'Mouzeil, Loire-Atlantique, France',
'NOGENT Sur MARNE, Val-de-Marne, France',
'Nancy, 54000, Meurthe-et-Moselle, France',
'Nancy, 54395, Meurthe-et-Moselle, France',
'Nantes St Similien BMS page,/184, Lot-et-Garonne, France',





'Neuilly-sur-Seine, 92200, Hauts-de-Seine, France',
'Niort, Deux-Sèvres, France',
'Nivillac, 56130, Morbihan, France',
'Nivillac, 56147, Morbihan, France',
'Nivillac,56130, Morbihan, France',
'Nivillac,56147, Morbihan, France',
'Nogent-Sur-Marne, Val-de-Marne, France',
'Notre-Dame-de-Bon-Port, Bourgneuf, 44021, Loire-Atlantique, France',
'Ovillers-la-Boisselle, 80615, Somme, France',
'Ovillers-la-Boisselle, Somme, France',
'Ovillers-la-Boisselle,80615, Somme, France',
'PARIS 18ème, Paris, France',
'Paimboeuf, Loire-Atlantique, France',
'Pannecé, 44118, Loire-Atlantique, France',
'Paris 14 ème, Paris, France',
'Paris 14e Arrondissement, 75114, Paris, France',
'Paris 14e, Paris, France',
'Paris 14ème, 75114, Paris, France',
'Paris 18, 75118, Paris, France',
'Paris 4e, Paris, France',
'Paris 7ème, 75107, Paris, France',
'Paris, 75000, Paris, France',
'Paulx, 44119, Loire-Atlantique, France',
'Paulx, 44270, Loire-Atlantique, France',
'Paulx, La Galaisière, Paulx, Loire-Atlantique, France',
'Paulx, Loire-Atlantique, France',
'Penestin, Morbihan, France',
'Petit-Auverne, 44121, Loire-Atlantique, France',
'Petit-Mars, Loire-Atlantique, France',
'Pierric, 44123, Loire-Atlantique, France',
'Pierric, 44290, Loire-Atlantique, France',
'Pierric, Loire-Atlantique, France',
'Piriac-sur-Mer, 44420, Loire-Atlantique, France',
'Plescop, 56890, Morbihan, France',
'Plessé 44630, Loire-Atlantique, France',
'Plessé le Coudray, France',
'Plessé, 44128, Bretagne, Loire-Atlantique, France',
'Plessé, 44128, Loire-Atlantique, France',
'Plessé, 44630, Loire-Atlantique, France',
'Plessé, Loire-Atlantique, France',
'Plessé,44128, Loire-Atlantique, France',
'Plessé,44630, Loire-Atlantique, France',
'Ploemeur, 56162, Morbihan, France',
'Plomodiern, Finistère, France',
'Plouray, 56770, Morbihan, France',
'Pléssé, Loire-Atlantique, France',
'Pont-Chateau, Loire-Atlantique, France',
'Pont-Château, Loire-Atlantique, France',
'Pont-Scorff, Morbihan, France',
'Pontcarneau, Loire-Atlantique, France',
'Pontchateau, 44129, Loire-Atlantique, France',
'Pontchateau, 44160, Loire-Atlantique, France',
'Pontchateau, Loire-Atlantique, France',
'Pontchateau,44160, Loire-Atlantique, France',
'Pontchâteau (Saint Martin), 44160, Loire-Atlantique, France',
'Pontchâteau, 440129, Loire-Atlantique, France',
'Pontchâteau, 44129, France 1512, Loire-Atlantique, France',
'Pontchâteau, 44129, Loire-Atlantique, France',
'Pontchâteau, 44129, Loirpoe Atlantique, Loire-Atlantique, France',
'Pontchâteau, 44160, Loire-Atlantique, France',
'Pontchâteau, Loire-Atlantique, France',
'Pontchâteau,44129, Loire-Atlantique, France',
'Pontchâteau,44160, Loire-Atlantique, France',
"Pontlieue, Aujourd'Hui le Mans, Sarthe, France",
'Pornic, 44131, Loire-Atlantique, France',
'Pornic, 44210, Loire-Atlantique, France',
'Pornic, Loire-Atlantique, France',
'Port Louis, 56290, Morbihan, France',
'Port-Saint-Père, 44133, Loire-Atlantique, France',
'Port-Saint-Père, 44710, Loire-Atlantique, France',
'Pouillé les Côteaux, 44522, Loire-Atlantique, France',
'Pouillé-les-Côteaux, 44134, Loire-Atlantique, France',
'Pouillé-les-Côteaux, 44522, Loire-Atlantique, France',
'Pouillé-les-Côteaux, Loire-Atlantique, France',
'Puceul, 44138, Loire-Atlantique, France',
'Puceul, 44390, Loire-Atlantique, France',
'Puceul, Saffre 44390, Loire-Atlantique, France',
'Puceul,44390, Loire-Atlantique, France',
'Pénestin, 56155, Morbihan, France',
'Pénestin, 56760, Morbihan, France',
'Pénestin, Morbihan, France',
'Questembert, Morbihan, France',
'Quilly, 44139, Loire-Atlantique, France',
'Quimper, 29232, Finistère, France',
'ROUGÉ, (.146), Bretagne, France., Loire-Atlantique, France',
'Rennes, 35238, Ille-et-Vilaine, France',
'Restigné, 37193, Indre-et-Loire, France',
'Restigné, Indre-et-Loire, France',






'Riaillé, 44440, Loire-Atlantique, France',
'Riaillé, Loire-Atlantique, France',
'Rouans, Loire-Inférieure, Loire-Atlantique, France',
'Rouge, Loire-Atlantique, France',
'Rougé, 44146, Loire-Atlantique, France',
'Rougé, 44660, Loire-Atlantique, France',
'Rougé, Loire-Atlantique, France',
'Roussay, 49263, Maine-et-Loire, France',
'Roussay, 49450, Maine-et-Loire, France',
'Ruffigné, 44148, Loire-Atlantique, France',
'Ruffigné, 44660, Loire-Atlantique, France',
'SAINT MÊME le TENU les BASSES ERMITIÈRES, Diocèse de Nantes, Loire-Atlantique, France',
'Saffré, 44149, Loire-Atlantique, France',
'Saffré, 44390, Loire-Atlantique, France',
'Saffré,44390, Loire-Atlantique, France',
'Saint André des Eaux, 44117, Loire-Atlantique, France',
'Saint André des Eaux, 44151, Bretagne, Loire-Atlantique, France',
'Saint Dolay, Morbihan, France',
'Saint Herblon, Loire-Atlantique, France',
'Saint Hilaire-de-Chaléons, Loire-Atlantique, France',
'Saint Julien de Mouvantes, Loire-Atlantique, France',
'Saint Julien de Vouvantes, Loire-Atlantique, France',
'Saint Lyphard, Loire-Atlantique, France',
'Saint Meme le Tenu, Loire-Atlantique, France',
'Saint Molf, Loire-Atlantique, France',
'Saint Même le Tenu, Pays-de-la-Loire, Loire-Atlantique, France',
'Saint Nazaire, 44184, Loire-Atlantique, France',
'Saint Nazaire, 44600, Loire-Atlantique, France',
'Saint Nazaire, Loire-Atlantique, France',
'Saint Patern, Vannes, 56000, Morbihan, France',
'Saint Sulpice des Landes, Loire-Atlantique, France',
'Saint Vincent des Landes, Loire-Atlantique, France',
'Saint-André des Eaux, Loire-Atlantique, France',
'Saint-André-des-Eaux 44117, Loire-Atlantique, France',
'Saint-André-des-Eaux, 44117, Loire-Atlantique, France',
'Saint-André-des-Eaux, 44151, Loire-Atlantique, France',
'Saint-André-des-Eaux,44117, Loire-Atlantique, France',
'Saint-Aubin-des-Châteaux, 44110, Loire-Atlantique, France',
'Saint-Aubin-des-Châteaux, 44153, Loire-Atlantique, France',
'Saint-Avaugourd-des-Landes, 85540, Vendée, France',
'Saint-Benoît-la-Forêt, 37210, Indre-et-Loire, France',
'Saint-Brevin-les-Pins, 44154, Loire-Atlantique, France',
'Saint-Brévin, Loire-Atlantique, France',
'Saint-Christophe-du-Bois, 49269, Maine-et-Loire, France',
'Saint-Dolay, 56130, Morbihan, France',
'Saint-Dolay, 56212, Morbihan, France',
'Saint-Dolay,56130, Morbihan, France',
'Saint-Etienne-de-Mer-Morte, 44157, Loire-Atlantique, France',
'Saint-Etienne-de-Mer-Morte, 44270, Loire-Atlantique, France',
'Saint-Etienne-de-Montluc, 44158, Loire-Atlantique, France',
'Saint-Fulgent, 85215, Vendée, France',
'Saint-Georges-sur-Loire, Maine-et-Loire, France',
'Saint-Gildas-des-Bois, 44161, Loire-Atlantique, France',
'Saint-Herblain, 44162, Loire-Atlantique, France',
'Saint-Herblain, 44800, Loire-Atlantique, France',


x == 'Saint-Hilaire-de-Chaleons, 44164, Loire-Atlantique, France' or x == 'Saint-Hilaire-de-Chaléons, 44164, Loire-Atlantique, France' or x == 'Saint-Hilaire-de-Chaléons, 44680, Loire-Atlantique, France' or x == 'Saint-Hilaire-de-Chaléons, La Richerie, Saint-Hilaire-de-Cha, Loire-Atlantique, France' or x == 'Saint-Hilaire-de-Chaléons, Loire-Atlantique, France' or 







'Saint-Laurent, Blain, 44015, Loire-Atlantique, France',
'Saint-Lyphard, 44410, Loire-Atlantique, France',
'Saint-Léger-les-Vignes, 44710, Loire-Atlantique, France',
'Saint-Mars-de-Coutais, 44178, Loire-Atlantique, France',
'Saint-Mars-de-Coutais, 44680, Loire-Atlantique, France',
'Saint-Mars-de-Coutais, Loire-Atlantique, France',
'Saint-Martin-des-Noyers, 85140, Vendée, France',
'Saint-Meme-le-Tenu, Loire-Atlantique, France',
'Saint-Molf, 44350, Loire-Atlantique, France',
'Saint-Molf, Loire-Atlantique, France',
'Saint-Même-le-Tenu, 44181, Loire-Atlantique, France',
'Saint-Même-le-Tenu, 44270, Loire-Atlantique, France',
'Saint-Même-le-Tenu,44270, Loire-Atlantique, France',
'Saint-Nazaire, ( Grand Marsac), Loire-Atlantique, France',
'Saint-Nazaire, 44184, Loire-Atlantique, France',
'Saint-Nazaire, 44600, Loire-Atlantique, France',
'Saint-Nazaire, Loire-Atlantique, France',
'Saint-Nazaire,44600, Loire-Atlantique, France',
'Saint-Nazaire,Cuneix, Loire-Atlantique, France',
"Saint-Nazaire,L'Angle, Loire-Atlantique, France",
'Saint-Nazaire,Le Bas Cuneix, Loire-Atlantique, France',
'Saint-Nazaire,Marsac, Loire-Atlantique, France',
'Saint-Nazaire,Passouer, Loire-Atlantique, France',
'Saint-Père-en-Retz, 44187, Loire-Atlantique, France',
'Saint-Saint-André-des-Eayx, Loire-Atlantique, France',
'Saint-Servant, 56236, Morbihan, France',
'Saint-Sulpice-des-Landes, 35316, Ille-et-Vilaine, France',
'Saint-Sulpice-des-Landes, 44191, Loire-Atlantique, France',
'Saint-Sébastien-sur-Loire, 44190, Loire-Atlantique, France',
'Saint-Sébastien-sur-Loire, 44230, Loire-Atlantique, France',
'Saint-Sébastien-sur-Loire, Loire-Atlantique, France',
'Saint-Vincent-des-Landes, 44193, Loire-Atlantique, France',
'Saint-Vincent-des-Landes, 44590, Loire-Atlantique, France',
'Saint-Vincent-des-Landes, Loire-Atlantique, France',
'Saint-Vincent-des-Landes,44590, Loire-Atlantique, France',
'Saint-Étienne-de-Mer-Morte, 44157, Loire-Atlantique, France',
'Saint-Étienne-de-Mer-Morte, 44270, Loire-Atlantique, France',
'Saint-Étienne-de-Mer-Morte, Loire-Atlantique, France',
'Saint-Étienne-de-Montluc, 44360, Loire-Atlantique, France',
'Sainte Reine de Bretagne, Loire-Atlantique, France',
'Sainte-Marie-sur-Mer, 44210, Loire-Atlantique, France',
'Sainte-Opportune, Sainte-Opportune-en-Retz, 44000, Loire-Atlantique, France',
'Sainte-Opportune-en-Retz, 44000, Loire-Atlantique, France',
'Sainte-Pazanne, 44680, Loire-Atlantique, France',
'Sainte-Pazanne, La Beusse, Sainte-Pazanne, Loire-Atlantique, France',
'Sainte-Reine-de-Bretagne, 44160, Loire-Atlantique, France',
'Sainte-Reine-de-Bretagne, 44189, Loire-Atlantique, France',
'Sainte-Reine-de-Bretagne, Loire-Atlantique, France',
'Sautron, 44194, Loire-Atlantique, France',
'Sautron, 44880, Loire-Atlantique, France',
'Sautron, Loire-Atlantique, France',
'Savenay, 44195, Loire-Atlantique, France',
'Savenay, 44260, Loire-Atlantique, France',
'Savenay, Loire-Atlantique, France',
'Sion Les Mines, Loire-Atlantique, France',
'Sion les Mines, Loire-Atlantique, France',
'Sion-Les-Mines, 44197, Loire-Atlantique, France',
'Sion-Les-Mines, 44590, Loire-Atlantique, France',
'Sion-les-Mines, 44197, Loire-Atlantique, France',
'Sion-les-Mines, 44590, Loire-Atlantique, France',
'Sion-les-Mines, France',
'Sion-les-Mines, Loire-Atlantique, France',
'Sommecaise, 89110, Yonne, France',
'Sommecaise, 89397, Yonne, France',
'Soudan, Loire-Atlantique, France',
'Soulvache, Loire-Atlantique, France',
'St André des Eaux, Loire-Atlantique, France',
'St André des Eaux,44600, Loire-Atlantique, France',
'St Etienne de Mer Morte, Loire-Atlantique, France',
'St Fulgent, Vendée, France',
'St Gildas des Bois, Loire-Atlantique, France',
'St Hilaire de Chaléons, Loire-Atlantique, France',
'St Julien de Vouvantes, Loire-Atlantique, France',
'St Lumine de Coutais, Loire-Atlantique, France',
'St Lyphard, Loire-Atlantique, France',
'St Mars de Coutais, Loire-Atlantique, France',
'St Martin, Rouans, 44145, Loire-Atlantique, France',
'St Même le Tenu, Loire-Atlantique, France',
'St Vincent des L, Loire-Atlantique, France',
'St Vincent des Landes, Loire-Atlantique, France',
'St Étienne de Montluc, 44360, Loire-Atlantique, France',
'St-André-des-Eaux, FR-44151, Bretagne, Loire-Atlantique, France',
'St-Hilaire-de-Chaléons, 44680, Loire-Atlantique, France',
'St-Jean-Baptiste, Lusanger,44590, Loire-Atlantique, France',
'St-Julien-de-Vouvantes, Loire-Atlantique, France',
'St-Même-le-Tenu, 44181, Loire-Atlantique, France',
'St-Vincent-des-Landes, 44193, Loire-Atlantique, France',
'Ste Pazanne, 44680, Loire-Atlantique, France',
'Ste Pazanne, Loire-Atlantique, France',
'Ste Reine de Bretagne, Loire-Atlantique, France',
'Ste-Pazanne, 44680, Loire-Atlantique, France',
'Sucé-Sur-Erdre, 44240, Loire-Atlantique, France',
'Teillay, 35332, Ille-et-Vilaine, France',
'Trans, Loire-Atlantique, France',
'Trans-sur-Erdre, 44440, Loire-Atlantique, France',
'Treffieux, 44170, Loire-Atlantique, France',
'Treffieux, 44208, Loire-Atlantique, France',
"Treffieux, Côtes-d'Armor, France",
'Treffieux, Loire-Atlantique, France',
'Treffieux,44170, Loire-Atlantique, France',
'Treffieux,44208, Loire-Atlantique, France',
'Trelaze, 49800, FR FRANCE, Maine-et-Loire, France',
"Trébrivan, 22344, Côtes-d'Armor, France",
'Tréffieux, Loire-Atlantique, France',
'Trélazé, 49353, Maine-et-Loire, France',
'Trélazé, Maine-et-Loire, France',
'Vai, France',
'Vains, 50300, Manche, France',
'Vains, 50612, Manche, France',
'Vannes, 56000, Morbihan, France',
'Vay, Loire-Atlantique, France',
'Vertou, 44120, Bretagne, Loire-Atlantique, France',
'Vertou, 44120, Loire-Atlantique, France',
'Vertou, 44215, Loire-Atlantique, France',
'Vertou, Loire-Atlantique, France',
'Vieillevigne, 44116, Loire-Atlantique, France',
'Vieillevigne, Loire-Atlantique, France',
'Vienne, 38544, Isère, France',
'Vigneux-de-Bretagne, Loire-Atlantique, France',
'Village de la Richerie, Saint-Hilaire-de-Chaléons, 44164, Loire-Atlantique, France',
'Viroflay, 78686, Yvelines, France',
'Warloy Baillon, Somme, France',
'Warloy-Baillon, Somme, France',
'X Guemene Penfao, 44x291, Saint Nazaire, Loire-Atlantique, France',
'[La Doubleraie]-Issé, 44075, Loire-Atlantique, France',
'[La Feuvrais]-Issé, 44075, Loire-Atlantique, France',
'[Le Boulay]-Erbray, 44054, Loire-Atlantique, France',
'[Le Cormier]-Erbray, 44054, Loire-Atlantique, France',
'[Les Garellières]-Erbray, 44054, Loire-Atlantique, France',
'checoul Sainte Croix, Loire-Atlantique, France',
'checoul, 44087, Loire-Atlantique, France',
'checoul, 44270, Loire-Atlantique, France',
'checoul, Loire-Atlantique, France',
'checoul, Ste-Croix, Loire-Atlantique, France',
'erval, Loire-Atlantique, France',
'inéault, Finistère, France',
'la Chapelle-Glain, 44031, Loire-Atlantique, France',
'le Haut Morvel, Marsac, Loire-Atlantique, France',
'le Haut Morvel, Marsac-sur-Don, Loire-Atlantique, France',
'lville, 44089, Loire-Atlantique, France',
'oirbreuil, Bourgneuf-en-Retz, 44021, Loire-Atlantique, France',
'oisdon La Riviere, Loire-Atlantique, France',
'oisdon la Rivière, Loire-Atlantique, France',
'oisdon, Loire-Atlantique, France',
'oisdon-la-Rivière, 44099, Loire-Atlantique, France',
'oisdon-la-Rivière, 44520, Loire-Atlantique, France',
'oisdon-la-Rivière, Loire-Atlantique, France',
'ontoir de Bretagne, Loire-Atlantique, France',
'ontoir-de-Bretagne, 44550, Loire-Atlantique, France',
'ontoir-de-Bretagne, Loire-Atlantique, France',
'ouais, 44105, Loire-Atlantique, France',
'ouais, Loire-Atlantique, France',
'ouzeil, 44107, Loire-Atlantique, France',
'ouzeil, Loire-Atlantique, France',
'reffeac, Loire-Atlantique, France',
'sac sur Don, Loire-Atlantique, France',
'sac-sur-Don, 44091, France le Verger, Loire-Atlantique, France',
'sac-sur-Don, 44091, Loire-Atlantique, France',
'sac-sur-Don, 44170, Loire-Atlantique, France',
'sac-sur-Don, Loire-Atlantique, France',
'squer, 44097, Loire-Atlantique, France',
'squer, Loire-Atlantique, France',
'ssillac, 440098, Loire-Atlantique, France',
'ssillac, 44098, Loire-Atlantique, France',
'ssillac, 44780, Loire-Atlantique, France',
'ssillac, Loire-Atlantique, France',
'ssillac,44098, Loire-Atlantique, France',
'ssillac,44780, Loire-Atlantique, France',
'ssérac, 44092, Loire-Atlantique, France',
't Nazaire, Loire-Atlantique, France',
'tes (Saint Clément), 44000, Loire-Atlantique, France',
'tes Chantenay, Loire-Atlantique, France',
'tes St clément, Loire-Atlantique, France',
'tes probable, Loire-Atlantique, France',
'tes, 44000, Loire-Atlantique, France',
'tes, 44109, Loire-Atlantique, France',
'tes, Loire-Atlantique, France',
'tes, \x86 Saint-Donatien, Loire-Atlantique, France',
'uvy-en-Champagne, 72219, Sarthe, France',
'villac, 56130, Morbihan, France',
'villac, 56147, Morbihan, France',
'villac, Morbihan, France',
'villac,56130, Morbihan, France',
'yet, 72191, Sarthe, France Page, Loire-Atlantique, France',
'ésanger, Loire-Atlantique, France'


#%%

event_table['place'].value_counts()[0:40]



#%%

master['birth_place_n'], master['birth_geoloc'] = zip(*master['birth_place'].apply(lambda x : replace_geography(x)))
master['death_place_n'], master['death_geoloc'] = zip(*master['death_place'].apply(lambda x : replace_geography(x)))

master['birth_date'] = master['birth_date'].apply(lambda x : str(x).replace('\xa0 ', ''))
master['death_date'] = master['death_date'].apply(lambda x : str(x).replace('\xa0 ', ''))
master['marriage_date'] = master['marriage_date'].apply(lambda x : str(x).replace('\xa0 ', ''))
# %%
master.head()

# %%

# %%

def f_memoize_dt(s):
    """
    Memoization technique
    """
    dates = {date:datetime.strptime(date,'%Y').strftime('%Y') for date in s.unique()}
    return s.map(dates)


t1 = master[['birth_geoloc', 'birth_date', 'birth_place_n']].rename(columns={'birth_geoloc' : 'geoloc', 'birth_date' : 'date', 'birth_place_n' : "place"})
t1['event_type'] = 'birth'
t2 = master[['death_geoloc', 'death_date', 'death_place_n']].rename(columns={'death_geoloc' : 'geoloc', 'death_date' : 'date', "death_place_n" : "place"})
t2['event_type'] = 'death'


event_table = pd.concat([t1, t2], axis=0, ignore_index=True)
event_table = event_table[event_table['date'] != ""].reset_index(drop=True)
event_table['date'] = event_table['date'].apply(lambda x : None if len(x) != 4 else x)
event_table = event_table.replace(to_replace='None', value=np.nan).dropna()
event_table['date'] = f_memoize_dt(event_table['date'])
#event_table['date'] = event_table['date'].year
event_table = event_table.sort_values(by="date")
event_table

# %%

event_table[['lat','long']] = pd.DataFrame(event_table.geoloc.tolist(), index= event_table.index)
event_table
# %%

x_min = -1.9 #min(df['long']) - 0.100
x_max = -1.3 #max(df['long']) + 0.100
y_min = 47.05 #min(df['lat']) - 0.100
y_max = 47.8 #max(df['lat']) + 0.100

extent = (x_min, x_max, y_min, y_max)

#plt.Figure(figsize=(679,515), dpi=50)
plt.Figure(figsize=(679,515), dpi=50)
fig = plt.gcf()
#fig.set_size_inches(9.43,7.15)
#fig.set_dpi(250)
ax = plt.gca()
ax.set_aspect('auto')
plt.title('Courbevoie')

plt.scatter(event_table['long'], event_table['lat'], s=5)

plt.xlim((x_min,x_max))
plt.ylim((y_min,y_max))
plt.xticks(size=5)
plt.yticks(size=5)


plt.show()

# %%

date_dict = {}
i = 0
for day in event_table['date'].sort_values(ascending=True).unique():
    date_dict[i] = day
    i += 1

def animate_plot(x):
    x_min = -1.9 #min(df['long']) - 0.100
    x_max = -1.3 #max(df['long']) + 0.100
    y_min = 47.05 #min(df['lat']) - 0.100
    y_max = 47.8 #max(df['lat']) + 0.100
    #colors = {1.:'red', 2.:'green'}

    date = date_dict[x]
    print(date)
    dt = event_table.loc[event_table['date'] == date, :]
    ax.scatter(dt['long'], dt['lat'], marker='o', s=5) # c=dt['transaction_type'].map(colors)

    extent = (x_min, x_max, y_min, y_max)

    #plt.imshow(img, aspect='auto', extent = extent, cmap='gray')

    ax.set_xlim((x_min,x_max))
    ax.set_ylim((y_min,y_max))

    ax.set_title('Hauts-de-Seine \nPublication Date = ' + str(date)[:10])


# Test animation
fig = plt.figure()
ax = plt.axes()
anim = animation.FuncAnimation(fig, animate_plot, interval = 1000, frames = len(event_table['date'].sort_values(ascending=True).unique()),
repeat=False)

# Saving the Animation
f = r"animate_func1.gif"
writergif = animation.PillowWriter(fps=len(event_table['date'].sort_values(ascending=True).unique())/6)
anim.save(f, writer=writergif)

#%%