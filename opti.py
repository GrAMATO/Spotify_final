import pandas as pd

playlists = pd.read_csv("moyennes_playlists.csv")

def _obj(med_valence, med_danceability, med_energy, med_acousticness, med_liveness,med_speechiness, med_instrumentalness):
    """
    Fixe les contraintes dans une liste"""
    objectif=[med_valence, med_danceability, med_energy, med_acousticness, med_liveness, med_speechiness, med_instrumentalness]
    return objectif


def _opti(objectif_min, objectif_max, playlists, dict_output):
    """Sélectionne dans un premier temps les playlists qui correspondent aux critères puis trie la liste obtenue en fonction de la popularité."""
    playlists_no_na = playlists.dropna()
    playlists_med = playlists_no_na.iloc[:, 10:16]
    for i, j, k in zip(list(playlists_med.columns), objectif_min, objectif_max):
        playlists_med[str(i) + "_filtre"] = playlists_med[(playlists_med[i]>=j) & (playlists_med[i]<=k)][i]
    return playlists_med.join(playlists_no_na[["med_popularity", "url","id","names"]]).dropna().sort_values("med_popularity", ascending = False).reset_index(drop=True)


def _fill_dict(valence, dansability, energy, acousti, speechness, instrumentalness, dict_output):
    """prend en entrée les valeurs des inputs, renvoie deux listes comprenant les bornes des inputs."""
    list_type = ["mood", "danser", "energie", "type_instruments", "type_paroles", "paroles"]
    list_inputs = [valence, dansability, energy, acousti, speechness, instrumentalness]
    objectif_min = []
    objectif_max = []
    for i, j in zip(list_type, list_inputs):
        min_value, max_value = dict_output[i][j]
        objectif_min.append(min_value)
        objectif_max.append(max_value)
    return objectif_min, objectif_max   


def final_opti(valence, dansability, energy, acousti, speechness, instrumentalness):
    
    playlists = pd.read_csv("moyennes_playlists.csv")

    dict_output = {"mood":{"joyeuse":[0.6, 1], "peu_importe":[0, 1], "neutre":[0.35, 0.60], "triste":[0, 0.35]},
"danser":{"oui":[0.6, 1],  "peu_importe":[0, 1], "neutre":[0.3, 0.6], "pas_du_tout":[0, 0.3]},
"energie":{"tres_oui":[0.8,1],"oui":[0.6, 85], "peu_importe":[0, 1], "neutre":[0.4, 0.65], "non":[0.2, 0.45],"tres_non":[0,0.25]},
"type_instruments":{"acoustiques":[0.75, 1], "majorite_acoustiques":[0.6, 0.8], "peu_importe":[0, 1], "melange":[0, 0.6]},
"paroles":{"sans_paroles":[0.65, 1],"majorite_sans_paroles":[0.4,0.7],"peu_importe":[0, 1], "avec_paroles":[0, 0.5]},
"type_paroles":{"majorite_chantees":[0.5, 1], "peu_importe":[0, 0.5], "majorite_parlees":[0, 0.50]}}
    
    
    objectif_min, objectif_max = _fill_dict(valence, dansability, energy, acousti, speechness, instrumentalness, dict_output)
    res_opti=_opti(objectif_min, objectif_max, playlists, dict_output).iloc[:, [i for i in range(-4,6)]]
    return res_opti








