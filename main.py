#%%
import json
import pandas as pd
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns
from fuzzywuzzy import fuzz

# %%

files = [file for file in os.listdir('./data')]
files

#%%

l_df = []



for file in files:
    with open(f"./data/{file}", encoding="utf8") as f :
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
master.tail(5)

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

#%%




# %%


def replace_geography(x):
    x = str(x).lstrip().lower()
    target_score = 80
    # // A
    if fuzz.token_set_ratio(x, "Angers, 49000, Maine-et-Loire, Pays de la Loire, France") >= target_score:
        r = "Angers, 49000, Maine-et-Loire, Pays de la Loire, France"
        g = [47.47283884908798, -0.5534940664669215] 
    elif fuzz.token_set_ratio(x, 'Assé-le-Riboul, 72012, Sarthe, France') >= target_score:
        r = 'Assé-le-Riboul, 72012, Sarthe, Pays de la Loire, France'
        g = [48.19349622305956, 0.08716587461851467]
    elif fuzz.token_set_ratio(x, 'Alençon, 61000, Orne, Normandie, France') >= target_score:
        r = 'Alençon, 61000, Orne, Normandie, France'
        g = [48.43267294913876, 0.0944893266270997]
    elif fuzz.token_set_ratio(x, "Ancinnes, 72005, Sarthe, Pays de la Loire, France") >= target_score:
        r = "Ancinnes, 72005, Sarthe, Pays de la Loire, France"
        g = [48.369616962848816, 0.17619590070547042]
    elif fuzz.token_set_ratio(x, 'Appenai-sous-Bellême, 61005, Orne, Normandie, France') >= target_score:
        r = 'Appenai-sous-Bellême, 61005, Orne, Normandie, France'
        g = [48.34399343213663, 0.5586789899415898]
    elif fuzz.token_set_ratio(x, "Ancenis, 44003, Loire-Atlantique, France") >= target_score:
        r = "Ancenis, 44003, Loire-Atlantique, France"
        g = [47.36633558866474, -1.1791069891779453]
    elif fuzz.token_set_ratio(x, 'Ame-marie, 61142, Orne, France') >= target_score:
        r = 'Ame-marie, 61142, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Authon-du-perche, 28330, eure-et-loir, France') >= target_score:
        r = 'Authon-du-perche, 28330, eure-et-loir, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Argentan, 61200, Orne, France') >= target_score:
        r = 'Argentan, 61200, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Arras, 62041, pas-de-calais, France') >= target_score:
        r = 'Arras, 62041, pas-de-calais, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Asnières-sur-vègre, 72010, Sarthe, France') >= target_score:
        r = 'Asnières-sur-vègre, 72010, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Asnières-sur-vègre, 72430, Sarthe, France') >= target_score:
        r = 'Asnières-sur-vègre, 72430, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Aubevoye, 27022, eure, France') >= target_score:
        r = 'Aubevoye, 27022, eure, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Aubigné-racan, 72013, Sarthe, France') >= target_score:
        r = 'Aubigné-racan, 72013, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Aulaines, 72352, Sarthe, France') >= target_score:
        r = 'Aulaines, 72352, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Auvers-le-hamon, 72016, Sarthe, France') >= target_score:
        r = 'Auvers-le-hamon, 72016, Sarthe, France'
        g = [0., 0.]
    
    # // B
    elif fuzz.token_set_ratio(x, 'La Bazoge, 72650, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'La Bazoge, 72650, Sarthe, Pays de la Loire, France'
        g = [48.09719284999686, 0.15507781812200938]
    elif fuzz.token_set_ratio(x, "Bellou-sur-Huisne, 61042, Orne, Normandie, France") >= target_score:
        r = "Bellou-sur-Huisne, 61042, Orne, Normandie, France"
        g = [48.42557227695994, 0.7563532168839905]
    elif fuzz.token_set_ratio(x, 'Brains-sur-Gée, 72550, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Brains-sur-Gée, 72550, Sarthe, Pays de la Loire, France'
        g = [48.01487590175186, -0.026881544696310485]
    elif fuzz.token_set_ratio(x, 'Blain, 44015, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Blain, 44015, Loire Atlantique, Pays de la Loire, France'
        g = [47.47710112969596, -1.7670651628296452]
    elif fuzz.token_set_ratio(x, "Beaumont-sur-Sarthe, 72170, Sarthe, Pays de la Loire, France") >= target_score:
        r = "Beaumont-sur-Sarthe, 72170, Sarthe, Pays de la Loire, France"
        g = [48.225454229794586, 0.1292082862734064]
    elif fuzz.token_set_ratio(x, 'Bellavilliers, 61037, Orne, Normandie, France') >= target_score:
        r = 'Bellavilliers, 61037, Orne, Normandie, France'
        g = [48.423093872967534, 0.4980931791374547]
    elif fuzz.token_set_ratio(x, "Bourgneuf en Retz, 44021, Loire Atlantique, Pays de la Loire, France") >= target_score:
        r = "Bourgneuf en Retz, 44021, Loire Atlantique, Pays de la Loire, France"
        g = [47.04275289980967, -1.9496753533654674]
    elif fuzz.token_set_ratio(x, "Besle sur Vilaine 44290, Loire-Atlantique, France") >= target_score:
        r = "Besle sur Vilaine 44290, Loire-Atlantique, France"
        g = [47.69783191909151, -1.865973311662278]
    elif fuzz.token_set_ratio(x, 'Bretoncelles, 61110, Orne, France') >= target_score:
        r = 'Bretoncelles, 61110, Orne, France'
        g = [48.43111160507278, 0.887825671480107]
    elif fuzz.token_set_ratio(x, 'Brette les pins, 72250, Sarthe, France') >= target_score:
        r = 'Brette les pins, 72250, Sarthe, France'
        g = [47.91170599798948, 0.33609268697335865]
    elif fuzz.token_set_ratio(x, 'Briosne-lès-sables, 72048, Sarthe, France') >= target_score:
        r = 'Briosne-lès-sables, 72048, Sarthe, France'
        g = [48.1733634713341, 0.39527508460949756]
    elif fuzz.token_set_ratio(x, 'Brullemail, 61064, Orne, France') >= target_score:
        r = 'Brullemail, 61064, Orne, France'
        g = [48.65716413543866, 0.32788337318459143]
    elif fuzz.token_set_ratio(x, 'Bréval,78980, yvelines, France') >= target_score:
        r = 'Bréval,78980, yvelines, France'
        g = [48.94474253028737, 1.5333821259453282]
    elif fuzz.token_set_ratio(x, 'Buré, 61066, Orne, France') >= target_score:
        r = 'Buré, 61066, Orne, France'
        g = [48.50739562172698, 0.40302828583007566]
    elif fuzz.token_set_ratio(x, 'Barlin, 62083, pas-de-calais, France') >= target_score:
        r = 'Barlin, 62083, pas-de-calais, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Baugé, 49018, maine-et-loire, France') >= target_score:
        r = 'Baugé, 49018, maine-et-loire, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Beaufay, 72026, Sarthe, France') >= target_score:
        r = 'Beaufay, 72026, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Bellou-le-trichard, 61041, Orne, France') >= target_score:
        r = 'Bellou-le-trichard, 61041, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Bonnetable, 72110, Sarthe, France') >= target_score:
        r = 'Bonnetable, 72110, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Bourg-le-roi, 72043, Sarthe, France') >= target_score:
        r = 'Bourg-le-roi, 72043, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Bouvron, 54200, meurthe-et-moselle, France') >= target_score:
        r = 'Bouvron, 54200, meurthe-et-moselle, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Braye sur maulne, 37036, indre-et-loire, France') >= target_score:
        r = 'Braye sur maulne, 37036, indre-et-loire, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Brest, 29019, finistère, France') >= target_score:
        r = 'Brest, 29019, finistère, France'
        g = [0., 0.]
        
    # // C
    elif fuzz.token_set_ratio(x, "Champtocé-sur-Loire, 49068, Maine et Loire, Pays de la Loire, France") >= target_score:
        r =  "Champtocé-sur-Loire, 49068, Maine et Loire, Pays de la Loire, France"
        g = [47.412581100284065, -0.865700565104513]
    elif fuzz.token_set_ratio(x, "La Chapelle-Glain, 44670, Loire-Atlantique, Pays de la Loire, France") >= target_score:
        r = "La Chapelle-Glain, 44670, Loire-Atlantique, Pays de la Loire, France"
        g = [47.62213605793191, -1.1963718452528325]
    elif fuzz.token_set_ratio(x, 'Condé-sur-Huisne, 61116, Orne, Normandie, France') >= target_score:
        r ='Condé-sur-Huisne, 61116, Orne, Normandie, France'
        g = [48.38155023782034, 0.8492075392860832]
    elif fuzz.token_set_ratio(x, 'Chérancé, 72078, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Chérancé, 72078, Sarthe, Pays de la Loire, France'
        g = [48.28643560256843, 0.17494452618227066]
    elif fuzz.token_set_ratio(x, 'Ceton, 61260, Orne, Normandie, France') >= target_score:
        r = 'Ceton, 61260, Orne, Normandie, France'
        g = [48.224734792719715, 0.7486089053753266]
    elif fuzz.token_set_ratio(x, "Châteaubriant, 44036, Loire-Atlantique, France") >= target_score:
        r = "Châteaubriant, 44036, Loire-Atlantique, France"
        g = [47.7170669204089, -1.3805278316888892]
    elif fuzz.token_set_ratio(x, 'Caen, 14000, Calvados, France') >= target_score:
        r = 'Caen, 14000, Calvados, France'
        g = [49.18228292208149, -0.37121284996316295]
    elif fuzz.token_set_ratio(x, 'Cahan, 61069, Orne, France') >= target_score:
        r = 'Cahan, 61069, Orne, France'
        g = [48.85928126074798, -0.44358036776337406]
    elif fuzz.token_set_ratio(x, 'Chahaignes, 72340, Sarthe, France') >= target_score:
        r = 'Chahaignes, 72340, Sarthe, France'
        g = [47.74178638911168, 0.513700828878969]
    elif fuzz.token_set_ratio(x, 'Chahains, 61080, Orne, France') >= target_score:
        r = 'Chahains, 61080, Orne, France'
        g = [48.562775973131885, -0.11477571380485692]
    elif fuzz.token_set_ratio(x, 'Chailloué, 61500, Orne, France') >= target_score:
        r = 'Chailloué, 61500, Orne, France'
        g = [48.651603718819125, 0.19534903071919535]
    elif fuzz.token_set_ratio(x, 'Challes, 72053, Sarthe, France') >= target_score:
        r = 'Challes, 72053, Sarthe, France'
        g = [47.93079798799889, 0.4147622197616773]
    elif fuzz.token_set_ratio(x, 'Champ-haut, 61240, Orne, France') >= target_score:
        r = 'Champ-haut, 61240, Orne, France'
        g = [48.72662567838973, 0.324725422805561]
    elif fuzz.token_set_ratio(x, 'Champagné, 72054, Sarthe, France') >= target_score:
        r = 'Champagné, 72054, Sarthe, France'
        g = [48.022498816786076, 0.3319667141235552]
        
    # // D
    elif fuzz.token_set_ratio(x, "Derval, 44051, Loire-Atlantique, Pays de la Loire, France") >= target_score:
        r =  "Derval, 44051, Loire-Atlantique, Pays de la Loire, France"
        g = [47.664938555107376, -1.6796956248721728]
    elif fuzz.token_set_ratio(x, 'Dangeul, 72112, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Dangeul, 72112, Sarthe, Pays de la Loire, France'
        g = [48.24710884358884, 0.25755118789544845]
    elif fuzz.token_set_ratio(x, 'Dorceau, 61147, Orne, Normandie, France') >= target_score:
        r = 'Dorceau, 61147, Orne, Normandie, France'
        g = [48.423285894842756, 0.8027067882873334]

    # // E
    elif fuzz.token_set_ratio(x, "Erbray, 44110, Loire-Atlantique, Pays de la Loire, France") >= target_score: 
        r =  "Erbray, 44110, Loire-Atlantique, Pays de la Loire, France"
        g = [47.65550932252617, -1.318016468838816]
    elif fuzz.token_set_ratio(x, 'Eperrais, 61154, Orne, Normandie, France') >= target_score:
        r = 'Eperrais, 61154, Orne, Normandie, France'
        g = [48.42247238284746, 0.5494305897229315]
        
    # // F
    elif fuzz.token_set_ratio(x, 'Fay-de-Bretagne, 44056, Loire-Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Fay-de-Bretagne, 44056, Loire-Atlantique, Pays de la Loire, France'
        g = [47.41200938166818, -1.7929900540756116]
    elif fuzz.token_set_ratio(x, 'Fyé, 72139, Sarthe, Pays de la Loire, France') >= target_score:
        r ='Fyé, 72139, Sarthe, Pays de la Loire, France'
        g = [48.32442098144286, 0.08234501720679109]

    # // G
    elif fuzz.token_set_ratio(x, "Grand-Fougeray, 35124, Ille-et-Vilaine, Bretagne, France") >= target_score:
        r = "Grand-Fougeray, 35124, Ille-et-Vilaine, Bretagne, France"
        g = [47.72403298306091, -1.7313856825114087]
    elif fuzz.token_set_ratio(x, 'Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Grand-Auverné, 44065, Loire Atlantique, Pays de la Loire, France'
        g = [47.591728720003445, -1.3297962851808929]
    elif fuzz.token_set_ratio(x, 'Gémages, 61130, Orne, Normandie, France') >= target_score:
        r = 'Gémages, 61130, Orne, Normandie, France'
        g = [48.29410669580173, 0.6159544072089755]
    elif fuzz.token_set_ratio(x, 'Grand-Rullecourt, Pas-de-Calais, France') >= target_score:
        r = 'Grand-Rullecourt, Pas-de-Calais, France'
        g = [50.2561093695923, 2.47495938033202]
    elif fuzz.token_set_ratio(x, 'Guemene Penfao, 44290, Loire-Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Guemene Penfao, 44290, Loire-Atlantique, Pays de la Loire, France'
        g = [47.629877586857795, -1.8332432463456552]


    # // H

    # // I
    elif fuzz.token_set_ratio(x, "Issé, 44075, Loire-Atlantique, Pays de la Loire, France") >= target_score:
        r = "Issé, 44075, Loire-Atlantique, Pays de la Loire, France"
        g = [47.62424618630497, -1.4508212064461499]

    # // J
    elif fuzz.token_set_ratio(x, 'Juigné-des-Moutiers, 44670, Loire-Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Juigné-des-Moutiers, 44670, Loire-Atlantique, Pays de la Loire, France'
        g = [47.67886932726545, -1.1853008239988176]
    elif fuzz.token_set_ratio(x, 'Jans, 44076, Loire-Atlantique, France') >= target_score:
        r = 'Jans, 44076, Loire-Atlantique, France'
        g = [47.620828752918165, -1.6137535354831185]

    # // K

    # // L
    elif fuzz.token_set_ratio(x, 'Lusanger, 44086, Loire-Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Lusanger, 44086, Loire-Atlantique, Pays de la Loire, France'
        g = [47.68193772699341, -1.5890626460881183]
    elif fuzz.token_set_ratio(x, 'Le Mans, 72181, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Le Mans, 72181, Sarthe, Pays de la Loire, France'
        g = [48.000945666098595, 0.19741493633517118]
    elif fuzz.token_set_ratio(x, 'La-Chapelle-Souëf, 61099, Orne, Normandie, France') >= target_score:
        r = 'La-Chapelle-Souëf, 61099, Orne, Normandie, France'
        g = [48.32392834250025, 0.5957966104058483]
    elif fuzz.token_set_ratio(x, 'La Milesse, 72650, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'La Milesse, 72650, Sarthe, Pays de la Loire, France'
        g = [48.062693572698464, 0.1393453859000587]
    elif fuzz.token_set_ratio(x, 'Le-Pin-la-Garenne, 61329, Orne, Normandie, France') >= target_score:
        r = 'Le-Pin-la-Garenne, 61329, Orne, Normandie, France'
        g = [48.44174431005491, 0.5465780664088976]
    elif fuzz.token_set_ratio(x, 'Lavardin, 72240, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Lavardin, 72240, Sarthe, Pays de la Loire, France'
        g = [48.077712380571455, 0.0629775583827917]
    elif fuzz.token_set_ratio(x, 'Lalacelle, 61213, Orne, Normandie, France') >= target_score:
        r = 'Lalacelle, 61213, Orne, Normandie, France'
        g = [48.472033544435405, -0.13104258012304476]
    elif fuzz.token_set_ratio(x, 'Limerzel, 56111, Morbihan, France') >= target_score:
        r = 'Limerzel, 56111, Morbihan, France'
        g = [47.638757279317396, -2.356524208110634]
    elif fuzz.token_set_ratio(x, 'Lisieux, 14366, Calvados, France') >= target_score:
        r = 'Lisieux, 14366, Calvados, France'
        g = [49.144719108663175, 0.22623451955788693]
    elif fuzz.token_set_ratio(x, 'Livet-en-saosnois, 72610, Sarthe, France') >= target_score:
        r = 'Livet-en-saosnois, 72610, Sarthe, France'
        g = [48.35942486504485, 0.2111996844560452]
    elif fuzz.token_set_ratio(x, 'Lombron, 72165, Sarthe, France') >= target_score:
        r = 'Lombron, 72165, Sarthe, France'
        g = [48.07892260592279, 0.4163113858760074]
    elif fuzz.token_set_ratio(x, 'Luceau, 72500, Sarthe, France') >= target_score:
        r = 'Luceau, 72500, Sarthe, France'
        g = [47.712773718433496, 0.3982793298936832]
    elif fuzz.token_set_ratio(x, 'Luché-pringé, 72800, Sarthe, France') >= target_score:
        r = 'Luché-pringé, 72800, Sarthe, France'
        g = [47.70548544359025, 0.07554815644910208]
    elif fuzz.token_set_ratio(x, 'Longnes, 72166, Sarthe, France') >= target_score:
        r = 'Longnes, 72166, Sarthe, France'
        g = [48.019759465758554, -0.07948186421544014]
    elif fuzz.token_set_ratio(x, "Lonlay-l'abbaye, 61232, Orne, France") >= target_score:
        r = "Lonlay-l'abbaye, 61232, Orne, France"
        g = [48.644643315709914, -0.7087095117689625]
    elif fuzz.token_set_ratio(x, 'Louvigny, 72490, Sarthe, France') >= target_score:
        r = 'Louvigny, 72490, Sarthe, France'
        g = [48.33847245122123, 0.20254935229535748]

    # // M
    elif fuzz.token_set_ratio(x, 'Mesanger, 44522, Loire-Atlantique, Pays de Loire, France') >= target_score:
        r = 'Mesanger, 44522, Loire-Atlantique, Pays de Loire, France'
        g = [47.43256918666803, -1.2274308034360966]
    elif fuzz.token_set_ratio(x, 'Mouais, 44590, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Mouais, 44590, Loire Atlantique, Pays de la Loire, France'
        g = [47.697703969323385, -1.6454071049897794]
    elif fuzz.token_set_ratio(x, 'Moisdon-la-Rivière, 44099, Loire-Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Moisdon-la-Rivière, 44099, Loire-Atlantique, Pays de la Loire, France'
        g = [47.62261363520462, -1.3759768678012587]
    elif fuzz.token_set_ratio(x, 'Mézières-sous-Lavardin, 72197, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Mézières-sous-Lavardin, 72197, Sarthe, Pays de la Loire, France'
        g = [48.155172721331894, 0.029417144782574768]
    elif fuzz.token_set_ratio(x, 'Mont St Jean, 72211, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Mont Saint Jean, 72211, Sarthe, Pays de la Loire, France'
        g = [48.24630468649458, -0.1072229173274874]
    elif fuzz.token_set_ratio(x, 'Mauves-sur-Huisne, 61255, Orne, Normandie, France') >= target_score:
        r = 'Mauves-sur-Huisne, 61255, Orne, Normandie, France'
        g = [48.44890702792295, 0.620764350193877]
    elif fuzz.token_set_ratio(x, 'Moutiers-au-Perche, 61300, Orne, Normandie, France') >= target_score:
        r = 'Moutiers-au-Perche, 61300, Orne, Normandie, France'
        g = [48.47581578244536, 0.8479496656852]
    elif fuzz.token_set_ratio(x, 'Malicorne, 72179, Sarthe, France') >= target_score:
        r = 'Malicorne, 72179, Sarthe, France'
        g = [47.812991849445424, -0.08300230573039864]
    elif fuzz.token_set_ratio(x, 'Mamers, 72180, Sarthe, France') >= target_score:
        r = 'Mamers, 72180, Sarthe, France'
        g = [48.351003823616814, 0.3730477889591584]
    elif fuzz.token_set_ratio(x, 'Mansigné, 72510, Sarthe, France') >= target_score:
        r = 'Mansigné, 72510, Sarthe, France'
        g = [47.747562287300504, 0.13225044475477007]
    elif fuzz.token_set_ratio(x, 'Mardilly, 61230, Orne, France') >= target_score:
        r = 'Mardilly, 61230, Orne, France'
        g = [48.83133491364703, 0.27839012002987035]
    elif fuzz.token_set_ratio(x, 'Mareil-en-champagne, 72184, Sarthe, France') >= target_score:
        r = 'Mareil-en-champagne, 72184, Sarthe, France'
        g = [47.984059715926485, -0.16940256380352386]
    elif fuzz.token_set_ratio(x, 'Maresché, 72186, Sarthe, France') >= target_score:
        r = 'Maresché, 72186, Sarthe, France'
        g = [48.21162496352743, 0.15496509178400134]
    elif fuzz.token_set_ratio(x, 'Margon, 28236, Eure-et-Loir, France') >= target_score:
        r = 'Margon, 28236, Eure-et-Loir, France'
        g = [48.33588818888569, 0.8345683963293582]
    elif fuzz.token_set_ratio(x, 'Marigné-laillé, 72187, Sarthe, France') >= target_score:
        r = 'Marigné-laillé, 72187, Sarthe, France'
        g = [47.81950691936552, 0.3400284484743354]
    elif fuzz.token_set_ratio(x, 'Marolles-les-braults, 72260, Sarthe, France') >= target_score:
        r = 'Marolles-les-braults, 72260, Sarthe, France'
        g = [48.25206859511779, 0.3134831334658443]
    elif fuzz.token_set_ratio(x, 'Marçon, 72183, Sarthe, France') >= target_score:
        r = 'Marçon, 72183, Sarthe, France'
        g = [47.71135687461885, 0.5098309266201543]
    elif fuzz.token_set_ratio(x, 'Mayet, 72191, Sarthe, France') >= target_score:
        r = 'Mayet, 72191, Sarthe, France'
        g = [47.76097921970527, 0.27562546231871365]
    elif fuzz.token_set_ratio(x, 'Meaux, 77100, seine-et-Marne, France') >= target_score:
        r = 'Meaux, 77100, seine-et-Marne, France'
        g = [48.95804322634777, 2.886570135023702]
    elif fuzz.token_set_ratio(x, 'Melleray, 72320, Sarthe, France') >= target_score:
        r = 'Melleray, 72320, Sarthe, France'
        g = [48.100227424060826, 0.7984813693359138]
    elif fuzz.token_set_ratio(x, 'Mezieres-sous-ballon, 72290, Sarthe, France') >= target_score:
        r = 'Mezieres-sous-ballon, 72290, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Moncé-en-saosnois, 72260, Sarthe, France') >= target_score:
        r = 'Moncé-en-saosnois, 72260, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Monhoudou, 72202, Sarthe, France') >= target_score:
        r = 'Monhoudou, 72202, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Montabon, 72500, Sarthe, France') >= target_score:
        r = 'Montabon, 72500, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Montbizot, 72205, Sarthe, France') >= target_score:
        r = 'Montbizot, 72205, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Montfort le rotrou, 72450, Sarthe, France') >= target_score:
        r = 'Montfort le rotrou, 72450, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Montmirail, 72208, Sarthe, France') >= target_score:
        r = 'Montmirail, 72208, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Montreuil-le-henri, 72150, Sarthe, France') >= target_score:
        r = 'Montreuil-le-henri, 72150, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Ménil-hermei, 61267, Orne, France') >= target_score:
        r = 'Ménil-hermei, 61267, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Mézières-sur-ponthouin, 72196, Sarthe, France') >= target_score:
        r = 'Mézières-sur-ponthouin, 72196, Sarthe, France'
        g = [0., 0.]

    # // N
    elif fuzz.token_set_ratio(x, 'Neuvillalais, 72216, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Neuvillalais, 72216, Sarthe, Pays de la Loire, France'
        g = [48.15514260233994, -0.0002471628054206737]
    elif fuzz.token_set_ratio(x, 'Nort-sur-Erdre, 44110, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Nort-sur-Erdre, 44110, Loire Atlantique, Pays de la Loire, France'
        g = [47.43865900956249, -1.4998854281797938]
    elif fuzz.token_set_ratio(x, "Nantes, 44000, Loire Atlantique, Pays de la Loire, France") >= target_score:
        r = "Nantes, 44000, Loire Atlantique, Pays de la Loire, France"
        g = [47.22048468387292, -1.5520975173687117]

    # // O

    # // P
    elif fuzz.token_set_ratio(x, "Petit-Auverné, 44121, Loire-Atlantique, Pays de la Loire, France") >= target_score:
        r = "Petit-Auverné, 44121, Loire-Atlantique, Pays de la Loire, France"
        g = [47.60957739836478, -1.2914942961474298]
    elif fuzz.token_set_ratio(x, 'Pizieux, 72238, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Pizieux, 72238, Sarthe, Pays de la Loire, France'
        g = [48.32291678170826, 0.33173115696573524]
    elif fuzz.token_set_ratio(x, 'Le Pin, 44124, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Le Pin, 44124, Loire Atlantique, Pays de la Loire, France'
        g = [47.59097969785115, -1.1520256971382625]
    elif fuzz.token_set_ratio(x, 'Plessé, 44128, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Plessé, 44128, Loire Atlantique, Pays de la Loire, France'
        g = [47.53967748727911, -1.8865598220667976]
    elif fuzz.token_set_ratio(x, 'Panon, 72600, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Panon, 72600, Sarthe, Pays de la Loire, France'
        g = [48.3378307055659, 0.29464078758508455]
    elif fuzz.token_set_ratio(x, "Paris, 75000, Paris, Île-de-France, France") >= target_score:
        r = "Paris, 75000, Paris, Île-de-France, France"
        g = [48.85905136925032, 2.339478787408999]
    elif fuzz.token_set_ratio(x, "Pruillé l'Eguillé, 72248, Sarthe, Pays de la Loire, France") >= target_score:
        r = "Pruillé l'Eguillé, 72248, Sarthe, Pays de la Loire, France"
        g = [47.837291605005724, 0.4296225618274573]
    elif fuzz.token_set_ratio(x, 'Préaux-du-Perche, 61337, Orne, Normandie, France') >= target_score:
        r = 'Préaux-du-Perche, 61337, Orne, Normandie, France'
        g = [48.33074610126995, 0.7008977221840225]

    # // Q

    # // R
    elif fuzz.token_set_ratio(x, 'Renazé, 53188, Mayenne, Pays de la Loire, France') >= target_score:
        r = 'Renazé, 53188, Mayenne, Pays de la Loire, France'
        g = [47.79174958267767, -1.055410733623209]
    elif fuzz.token_set_ratio(x, 'René, 72260, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'René, 72260, Sarthe, Pays de la Loire, France'
        g = [48.27855872914328, 0.21820153682944038]
    elif fuzz.token_set_ratio(x, 'Rezé, 44143, Loire-Atlantique, France') >= target_score:
        r = 'Rezé, 44143, Loire-Atlantique, France'
        g = [47.19153926450472, -1.5675925627492457]
    
    elif fuzz.token_set_ratio(x, 'Ruillé-en-Champagne, 72240, Sarthe, France') >= target_score:
        r = 'Ruillé-en-Champagne, 72240, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Rouperroux-le-Coquet, 72259, Sarthe, France') >= target_score:
        r = 'Rouperroux-le-Coquet, 72259, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Rouessé-Fontaine, 72610, Sarthe, France') >= target_score:
        r = 'Rouessé-Fontaine, 72610, Sarthe, France'
        g = [0., 0.]

    # // S
    elif fuzz.token_set_ratio(x, "Sion-les-Mines, 44197, Loire-Atlantique, Pays de la Loire, France") >= target_score:
        r =  "Sion-les-Mines, 44197, Loire-Atlantique, Pays de la Loire, France"
        g = [47.735823444826636, -1.591431581738148]
    elif fuzz.token_set_ratio(x, 'Saint-Julien-de-Vouvantes, 44670, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Saint-Julien-de-Vouvantes, 44670, Loire Atlantique, Pays de la Loire, France'
        g = [47.642838220497744, -1.2402680101837842]
    elif fuzz.token_set_ratio(x, "Saint-Rémy-du-Plain, 72317, Sarthe, Pays de la Loire, France") >= target_score:
        r = "Saint-Rémy-du-Plain, 72317, Sarthe, Pays de la Loire, France"
        g = [48.34915389885259, 0.25535497185089606]
    elif fuzz.token_set_ratio(x, "Saint-Hilaire-de-Chaléons, 44164, Loire Atlantique, Pays de la Loire, France") >= target_score:
        r = "Saint-Hilaire-de-Chaléons, 44164, Loire Atlantique, Pays de la Loire, France"
        g = [47.10218003883818, -1.86779332795036]
    elif fuzz.token_set_ratio(x, 'Saint-Sulpice-des-Landes, 35316, Ille-et-Vilaine, Bretagne, France') >= target_score:
        r = 'Saint-Sulpice-des-Landes, 35316, Ille-et-Vilaine, Bretagne, France'
        g = [47.76589797803712, -1.6229813618913544]
    elif fuzz.token_set_ratio(x, 'Saint-Vincent-des-Landes, 44193, Loire-Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Saint-Vincent-des-Landes, 44193, Loire-Atlantique, Pays de la Loire, France'
        g = [47.65607499068501, -1.4950625642257795]
    elif fuzz.token_set_ratio(x, 'Saint-Longis, 72295, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Saint-Longis, 72295, Sarthe, Pays de la Loire, France'
        g = [48.355451357344705, 0.3466703711781987]
    elif fuzz.token_set_ratio(x, 'Saint-Cyr-la-Rosière, 61130, Orne, Normandie, France') >= target_score:
        r = 'Saint-Cyr-la-Rosière, 61130, Orne, Normandie, France'
        g = [48.330178810842234, 0.6398605440255456]
    elif fuzz.token_set_ratio(x, 'Saint-Étienne-de-Mer-Morte, 44157, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Saint-Étienne-de-Mer-Morte, 44157, Loire Atlantique, Pays de la Loire, France'
        g = [46.93067477737113, -1.7410734883439394]
    elif fuzz.token_set_ratio(x, 'Soudan, 44199, Loire Atlantique, Pays de la Loire, France') >= target_score:
        r = 'Soudan, 44199, Loire Atlantique, Pays de la Loire, France'
        g = [47.739098415351386, -1.3064777072752487]
    elif fuzz.token_set_ratio(x, 'Saint-Ouen-de-Mimbré, 72305, Sarthe, Pays de la Loire, France') >= target_score:
        r ='Saint-Ouen-de-Mimbré, 72305, Sarthe, Pays de la Loire, France'
        g = [48.293580515654455, 0.04751234359933429]
    elif fuzz.token_set_ratio(x, 'Sainte-Jamme-sur-Sarthe, 72380, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Sainte-Jamme-sur-Sarthe, 72380, Sarthe, Pays de la Loire, France'
        g = [48.14229208871135, 0.16647439984282472]
    elif fuzz.token_set_ratio(x, 'Saint-Germain-de-la-Coudre, 61394, Orne, Normandie, France') >= target_score:
        r ='Saint-Germain-de-la-Coudre, 61394, Orne, Normandie, France'
        g = [48.282659316152255, 0.6045594890445124]
    elif fuzz.token_set_ratio(x, 'Saint-Germain-des-Grois, 61395, Orne, Normandie, France') >= target_score:
        r = 'Saint-Germain-des-Grois, 61395, Orne, Normandie, France'
        g = [48.39886863718351, 0.8299984856841561]
    elif fuzz.token_set_ratio(x, 'Saint-Aubin-des-Grois, 61368, Orne, Normandie, France') >= target_score:
        r = 'Saint-Aubin-des-Grois, 61368, Orne, Normandie, France'
        g = [48.35494338715396, 0.643984251501759]
    elif fuzz.token_set_ratio(x, 'Saint-Nazaire, 44600, Loire-Atlantique, France') >= target_score:
        r = 'Saint-Nazaire, 44600, Loire-Atlantique, France'
        g = [47.276215970904325, -2.2123163555921064]

    elif fuzz.token_set_ratio(x, 'Sablé-sur-sarthe, 72300, Sarthe, France') >= target_score:
        r = 'Sablé-sur-sarthe, 72300, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint Martin du Vieux Bellême 61426, Orne, France') >= target_score:
        r = 'Saint Martin du Vieux Bellême 61426, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint Remy des Monts, 72600, sarthe, France') >= target_score:
        r = 'Saint Remy des Monts, 72600, sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-Calez-en-Saosnois, 72260, Sarthe, France') >= target_score:
        r = 'Saint-Calez-en-Saosnois, 72260, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint Georges le Gaultier, 72590, Sarthe, France') >= target_score:
        r = 'Saint Georges le Gaultier, 72590, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint Georges du Rosay, 72110, Sarthe, France') >= target_score:
        r = 'Saint Georges du Rosay, 72110, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-martin-des-pézerits, 61425, Orne, France') >= target_score:
        r = 'Saint-martin-des-pézerits, 61425, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-pierre-des-ormes, 72313, Sarthe, France') >= target_score:
        r = 'Saint-pierre-des-ormes, 72313, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-pierre-du-lorouër, 72314, Sarthe, France') >= target_score:
        r = 'Saint-pierre-du-lorouër, 72314, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-pierre-la-cour, 53410, mayenne, France') >= target_score:
        r = 'Saint-pierre-la-cour, 53410, mayenne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-pierre-sur-orthe, 53249, mayenne, France') >= target_score:
        r = 'Saint-pierre-sur-orthe, 53249, mayenne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-pavace, 72310, Sarthe, France') >= target_score:
        r = 'Saint-pavace, 72310, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-ulphace, 72322, Sarthe, France') >= target_score:
        r = 'Saint-ulphace, 72322, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, "Saint-pierre-d'entremont, 61800, Orne, France") >= target_score:
        r = "Saint-pierre-d'entremont, 61800, Orne, France"
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-ouen-de-sécherouvre, 61438, Orne, France') >= target_score:
        r = 'Saint-ouen-de-sécherouvre, 61438, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-sulpice-sur-risle, 61456, Orne, France') >= target_score:
        r = 'Saint-sulpice-sur-risle, 61456, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-victeur, 72323, Sarthe, France') >= target_score:
        r = 'Saint-victeur, 72323, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sainte-sabine-sur-longève, 72319, Sarthe, France') >= target_score:
        r = 'Sainte-sabine-sur-longève, 72319, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Saint-vincent-des-prés, 72324, Sarthe, France') >= target_score:
        r = 'Saint-vincent-des-prés, 72324, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sainte-honorine-la-chardonne, 61407, Orne, France') >= target_score:
        r = 'Sainte-honorine-la-chardonne, 61407, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sainte-honorine-la-guillaume, 61408, Orne, France') >= target_score:
        r = 'Sainte-honorine-la-guillaume, 61408, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sargé-lès-le-mans,72190, Sarthe, France') >= target_score:
        r = 'Sargé-lès-le-mans,72190, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sauvagère, 61463, Orne, France') >= target_score:
        r = 'Sauvagère, 61463, Orne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, "Savigné-l'evêque, 72329, Sarthe, France") >= target_score:
        r = "Savigné-l'evêque, 72329, Sarthe, France"
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Savigné-sous-le-lude, 72330, Sarthe, France') >= target_score:
        r = 'Savigné-sous-le-lude, 72330, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Segrie, 72332, Sarthe, France') >= target_score:
        r = 'Segrie, 72332, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sillé-le-guillaume, 72140, Sarthe, France') >= target_score:
        r = 'Sillé-le-guillaume, 72140, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Solesmes, 72336, Sarthe, France') >= target_score:
        r = 'Solesmes, 72336, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sommecaise, 89397, yonne, France') >= target_score:
        r = 'Sommecaise, 89397, yonne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Souain-perthes-lès-hurlus, 51553, marne, France') >= target_score:
        r = 'Souain-perthes-lès-hurlus, 51553, marne, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Souday, 41248, loir-et-cher, France') >= target_score:
        r = 'Souday, 41248, loir-et-cher, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Sougé-le-ganelon, 72337, Sarthe, France') >= target_score:
        r = 'Sougé-le-ganelon, 72337, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Souillé, 72338, Sarthe, France') >= target_score:
        r = 'Souillé, 72338, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Souligné sous ballon, 72340, Sarthe, France') >= target_score:
        r = 'Souligné sous ballon, 72340, Sarthe, France'
        g = [0., 0.]
    elif fuzz.token_set_ratio(x, 'Soulitré, 72341, Sarthe, France') >= target_score:
        r = 'Soulitré, 72341, Sarthe, France'
        g = [0., 0.]
    
    

    # // T

    # // U

    # // V
    elif fuzz.token_set_ratio(x, 'Villaines-la-Carelle, 72374, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Villaines-la-Carelle, 72374, Sarthe, Pays de la Loire, France'
        g = [48.37778841322947, 0.2985808068847063]
    elif fuzz.token_set_ratio(x, 'Verrières, 61501, Orne, Normandie, France') >= target_score:
        r = 'Verrières, 61501, Orne, Normandie, France'
        g = [48.392107622776756, 0.7623518050589735]
    elif fuzz.token_set_ratio(x, 'Vivoin, 72380, Sarthe, Pays de la Loire, France') >= target_score:
        r = 'Vivoin, 72380, Sarthe, Pays de la Loire, France'
        g = [48.234234983953016, 0.15570634024881186]

    # // W

    # // X

    # // Y
    elif fuzz.token_set_ratio(x, "Yvré-l'évêque, 72530, Sarthe, France") >= target_score:
        r = "Yvré-l'évêque, 72530, Sarthe, France"
        g = [48.01487222787023, 0.2687653123689884]
    elif fuzz.token_set_ratio(x, 'Yvré-le-pôlin, 72330, Sarthe, France') >= target_score:
        r = 'Yvré-le-pôlin, 72330, Sarthe, France'
        g = [47.82036145678282, 0.15322937839553014]

    # // Z  
        

    else:
        #r = f"[X] {x}"
        r = x
        g = [0.0, 0.0]
        pass
    return r, g




# %%

x == 'Abbaretz, 44001, Loire-Atlantique, France' or x == 'Abbaretz, 44170, Loire-Atlantique, France' or x == 'Abbaretz, Loire-Atlantique, France' or 
x == 'Arthon en retz, Loire-Atlantique, France' or x == 'Arthon, 44320, Loire-Atlantique, France' or x == 'Arthon, Loire-Atlantique, France' or x == 'Arthon-en-Retz, 44005, Loire-Atlantique, France' or x == 'Arthon-en-Retz, 44320, Loire-Atlantique, France' or x == 'Arthon-en-Retz, Loire-Atlantique, France' or 
x == 'Asserac, Loire-Atlantique, France' or x == 'Assérac (Azereg), 44410, Loire-Atlantique, France' or x == 'Assérac, 44006, Bretagne, Loire-Atlantique, France' or x == 'Assérac, 44006, Loire-Atlantique, France' or x == 'Assérac, 44410, Loire-Atlantique, France' or x == 'Assérac, Dpt, Loire-Atlantique, France' or x == 'Assérac, Loire-Atlantique, France' or x == 'Assérac, Loire-Inférieure, Loire-Atlantique, France' or x == 'Assérac,44410, Loire-Atlantique, France' or 
x == 'Avessac, 44007, Bretagne, Loire-Atlantique, France' or x == 'Avessac, 44007, Loire-Atlantique, France' or x == 'Avessac, 44460, Loire-Atlantique, France' or x == 'Avessac, Loire-Atlantique, France' or 

x == 'Bourgneuf en Retz, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, 44021, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, 44580, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, Loire-Atlantique, France' or x == 'Bourgneuf-en-Retz, Nombreuil, Bourgneuf-en-Retz, Loire-Atlantique, France' or 






#%%





#%%

master['birth_place_n'], master['birth_geoloc'] = zip(*master['birth_place'].apply(lambda x : replace_geography(x)))
master['death_place_n'], master['death_geoloc'] = zip(*master['death_place'].apply(lambda x : replace_geography(x)))

master['birth_date'] = master['birth_date'].apply(lambda x : str(x).replace('\xa0 ', ''))
master['death_date'] = master['death_date'].apply(lambda x : str(x).replace('\xa0 ', ''))
master['marriage_date'] = master['marriage_date'].apply(lambda x : str(x).replace('\xa0 ', ''))
# %%
master.head()

# %%

place = []
place.extend(master['birth_place_n'].value_counts().index)
place.extend(master['death_place_n'].value_counts().index)
#place.extend(master['marriage_place_n'].value_counts().index)
place = list(set(place))
print(f"Nb locations in dataset : {len(place)}")
t = pd.Series(place).sort_values().to_list()
t


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
event_table[['lat','long']] = pd.DataFrame(event_table.geoloc.tolist(), index= event_table.index)
event_table
# %%

x_min = -2.9 #min(df['long']) - 0.100
x_max = -0.3 #max(df['long']) + 0.100
y_min = 47.0 #min(df['lat']) - 0.100
y_max = 47.8 #max(df['lat']) + 0.100

extent = (x_min, x_max, y_min, y_max)

#plt.Figure(figsize=(679,515), dpi=50)
plt.Figure(figsize=(679,515), dpi=50)
fig = plt.gcf()
#fig.set_size_inches(9.43,7.15)
#fig.set_dpi(250)
ax = plt.gca()
ax.set_aspect('auto')
plt.title('North West France')

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
    x_max = -0.3 #max(df['long']) + 0.100
    y_min = 47.0 #min(df['lat']) - 0.100
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
