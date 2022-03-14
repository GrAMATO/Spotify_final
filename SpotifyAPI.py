import requests
import json
import pandas as pd
import base64
import datetime
from urllib.parse import urlencode
import time
import base64
import io
import os
from boto.s3.connection import S3Connection


def get_all_sha(user, repo, filepos):
    """Permet de générer le token 'sha' de tous les fichiers d'un dossier, prend en entrée le nom du compte github, le nom du repo et le nom du fichier, 
    renvoie une liste comprenant les 'sha'."""
    login2 = requests.get('https://api.github.com/repos/' + user + '/' + repo + '/contents/' + filepos)
    return login2.json()

def encode_file(file_to_encode):
    """Prend en entrée le fichier à encoder, le convertit en csv et renvoie le fichier crypté."""
    file_to_encode_csv = file_to_encode.to_csv(index = False)
    file_change64 = base64.b64encode(file_to_encode_csv.encode("utf-8"))
    return str(file_change64, "utf-8")

def update_file(user, repo, filepos, token, sha, encodedfile):
    """Permet la mise à jour d'un fichier, nécessite un token de connexion avec autorisation de modification des repos. Le fichier doit être
    encodé en base64."""
    message = json.dumps({"message":"update",
                            "content": encodedfile ,
                            "sha": sha
                            })
    headers = {'Authorization': 'token ' + token}
    login2 = requests.put('https://api.github.com/repos/' + user + '/' + repo + '/contents/' + filepos , headers=headers, data=message)
    return login2.json()

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret


    def get_client_credentials(self):

        #Returns a base64 encoded string

        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
        "Authorization": f"Basic {client_creds_b64}" 
        }

    def get_token_data(self):
        return {
        "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299): 
            raise Exception("Could not authenticate client")
          #return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires 
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
   
  

    
def get_playlists(client_id_spoti, client_secret_spoti): 
    """Récupère les playlists"""
    access_token = access_token_build(client_id_spoti, client_secret_spoti)
    dict_playlists = {"names":[], "description":[], "url":[], "id":[], "image":[], "public":[]} 
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    url = 'https://api.spotify.com/v1/users/spotify/playlists'
    j = 0
    params_number = {'limit': 1}
    r = requests.get(url, headers=headers, params=params_number)
    number_dict = json.loads(r.text)
    
    for i in range(0, round(number_dict["total"], -1)+50, 50):
        try:
            params = {'limit': 50, 'offset': i}
            try:
                r = requests.get(url, headers=headers, params=params) 
            except:
                while True:
                    try:
                        time.sleep(10)
                        access_token = access_token_build(client_id_spoti, client_secret_spoti)
                        headers = {
                          "Authorization": f"Bearer {access_token}"}
                        r = requests.get(endpoint, headers=headers) 
                        break
                    except:
                        print("error")
            if str(r) == '<Response [401]>' :
                access_token = access_token_build(client_id_spoti, client_secret_spoti)
                headers = {
                  "Authorization": f"Bearer {access_token}"}
                r = requests.get(endpoint, headers=headers)
            else:
                response_dict = json.loads(r.text)
                for j in range(50):
                    try:
                        dict_playlists["names"].append(response_dict["items"][j]["name"])
                        dict_playlists["description"].append(response_dict["items"][j]["description"])
                        dict_playlists["url"].append(response_dict["items"][j]["external_urls"]["spotify"])
                        dict_playlists["id"].append(response_dict["items"][j]["id"])
                        try:
                            dict_playlists["image"].append(response_dict["items"][j]["images"][0]["url"])
                        except:
                            dict_playlists["image"].append("")
                        try:
                            dict_playlists["public"].append(response_dict["items"][j]["public"])
                        except:
                            dict_playlists["public"].append("")
                        j+=1
                    except:
                        break
        except:
            return dict_playlists
    return dict_playlists

def get_moyennes_playlists(data_playlists, tracks_playlist, data_analyse):
    dict_playlists = {"names":[], "id":[], "url":[]} 
    dict_playlists_test = {}
    dict_playlists["names"].append(data_playlists["names"])
    dict_playlists["id"].append(data_playlists["id"])
    dict_playlists["url"].append(data_playlists["url"])
    for i in ["valence", "danceability", "energy", "acousticness", "speechiness", "instrumentalness"]:
        dict_playlists_test["mean_"+i] = []
        dict_playlists_test["med_"+i] = []
        dict_playlists_test["sd_"+i] = []
        dict_playlists_test["quant1_"+i] = []
        dict_playlists_test["quant3_"+i] = []
    for playlist_id, playlist_name, playlist_url in zip(data_playlists["id"], data_playlists["names"], data_playlists["url"]):
        tracks_playlist_clean = tracks_playlist[tracks_playlist["playlist_id"] == playlist_id]
        track_playlist_detail = pd.merge(tracks_playlist_clean, data_analyse, left_on="track_id", right_on="id")
        data_tracks_playlist_cleaned = track_playlist_detail[["playlist_id", "popularity", "valence", "danceability", "energy", "acousticness", "speechiness", "instrumentalness"]]
        #["valence", "danceability", "energy", "acousticness", "speechiness", "instrumentalness"] #"names_playlist", "id_playlist", "url_playlist",
        described_data = data_tracks_playlist_cleaned.describe()
        for i in ["valence", "danceability", "energy", "acousticness", "speechiness", "instrumentalness"]:
            dict_playlists_test["mean_"+i].append(described_data.loc["mean", i])
            dict_playlists_test["med_"+i].append(described_data.loc["50%", i])
            dict_playlists_test["sd_"+i].append(described_data.loc["std", i])
            dict_playlists_test["quant1_"+i].append(described_data.loc["25%", i])
            dict_playlists_test["quant3_"+i].append(described_data.loc["75%", i])
    
           
    dict_final = {**dict_playlists, **dict_playlists_test}
    for i in dict_playlists.keys():
        dict_final[i] = dict_final[i][0]
    return dict_final
    
def get_tracks(client_id_spoti, client_secret_spoti, data_playlists):
    access_token = access_token_build(client_id_spoti, client_secret_spoti)
    dict_tracks = {"playlist_id":[], "track_id":[], "popularity":[], "track_url":[], "artist":[]} 
    headers = {
      "Authorization": f"Bearer {access_token}"}
    for i in data_playlists["id"]:
        time.sleep(0.5)
        endpoint = "https://api.spotify.com/v1/playlists/" + str(i) + "/tracks"
        params = {'market':'FR'}
        try:
            r = requests.get(endpoint, headers=headers, params=params) 
        except ConnectionError:
            while True:
                try:
                    time.sleep(10)
                    access_token = access_token_build(client_id_spoti, client_secret_spoti)
                    headers = {
                      "Authorization": f"Bearer {access_token}"}
                    r = requests.get(endpoint, headers=headers) 
                    break
                except:
                    print("error")
        if str(r) == '<Response [401]>' :
                print("access_token")
                access_token = access_token_build(client_id_spoti, client_secret_spoti)
                headers = {
                  "Authorization": f"Bearer {access_token}"}
                r = requests.get(endpoint, headers=headers)
        try:
            response_dict = json.loads(r.text)
            for j in range(int(response_dict["total"])):
                try:
                    dict_tracks["playlist_id"].append(str(i))
                    try:
                        dict_tracks["track_id"].append(response_dict["items"][j]["track"]["id"])
                    except:
                        dict_tracks["track_id"].append("")
                    try:
                        dict_tracks["popularity"].append(response_dict["items"][j]["track"]["popularity"])
                    except:
                        dict_tracks["popularity"].append("")
                    try:
                        dict_tracks["track_url"].append(response_dict["items"][j]["track"]["external_urls"]["spotify"])
                    except:
                        dict_tracks["track_url"].append("")
                    try:
                        dict_tracks["artist"].append([test["items"][j]["track"]["artists"][i]["name"] for i in range(0, len(test["items"][j]["track"]["artists"]))])
                    except:
                        dict_tracks["artist"].append("")
                        
                except:
                    break
        except:
            pass
    return dict_tracks

def analyse_tracks(client_id_spoti, client_secret_spoti, data_tracks):
    access_token = access_token_build(client_id_spoti, client_secret_spoti)
    df_analyse = pd.DataFrame()
    #dict_verif = {}
    headers = {
      "Authorization": f"Bearer {access_token}"}
    for i in data_tracks["track_id"]:
        #dict_verif["verif"].append(i)
        endpoint = "https://api.spotify.com/v1/audio-features/" + str(i) 
        try:
            r = requests.get(endpoint, headers=headers) 
        except ConnectionError:
            while True:
                try:
                    time.sleep(10)
                    access_token = access_token_build(client_id_spoti, client_secret_spoti)
                    headers = {
                      "Authorization": f"Bearer {access_token}"}
                    r = requests.get(endpoint, headers=headers) 
                    break
                except:
                    print("error")
        #nb_track += 1
        if str(r) == '<Response [401]>' :
                print("access_token")
                access_token = access_token_build(client_id_spoti, client_secret_spoti)
                headers = {
                  "Authorization": f"Bearer {access_token}"}
                r = requests.get(endpoint, headers=headers)
        try:
            response_dict = json.loads(r.text)
            df_analyse = df_analyse.append(response_dict, ignore_index=True)
            #print(df_analyse)
            #df_analyse.to_csv("data_analyse.csv")
        except:
            pass
        
    return df_analyse



def access_token_build(client_id, client_secret):
    """Génère le token d'accès"""
    spoti = SpotifyAPI(client_id, client_secret)
    return spoti.get_access_token()
    
def main_transfert(filenames, dict_sha, USER, REPO, TOKEN):
    for filename in filenames:
        url = "https://raw.githubusercontent.com/GregoireAMATO/Spotify_final/main/data/{}.csv".format(filename)
        filepos = "Archives_data/{}_old.csv".format(filename)
        download = requests.get(url).content
        df = pd.read_csv(io.StringIO(download.decode('utf-8')))
        encodedfile = encode_file(df)
        print(update_file(USER, REPO, filepos, TOKEN, dict_sha[filename], encodedfile))
        print(filename + " archived!")

def main_transfert2(filenames, dict_sha, USER, REPO, TOKEN):
    for filename in filenames:
        url = "https://raw.githubusercontent.com/GregoireAMATO/Spotify_final/main/data/{}.csv".format(filename)
        filepos = "Testfolder/{}.csv".format(filename)
        download = requests.get(url).content
        df = pd.read_csv(io.StringIO(download.decode('utf-8')))
        encodedfile = encode_file(df)
        print(update_file(USER, REPO, filepos, TOKEN, dict_sha[filename], encodedfile))
        print(filename + " archived!")


def main():
    client_id_spoti = str(os.environ.get("ACCOUNT_API_REPO_KEY"))  
    client_secret_spoti = str(os.environ.get("ACCOUNT_API_REPO_SECRET"))  
    USER = "GregoireAMATO"
    REPO = "Spotify_final"
    TOKEN = str(os.environ.get("TOKEN_REPO_ACCESS"))

    #### Déplacement du fichier précédent dans une archive
 
    filepos = "data"#/{}_old.csv".format(filename)
    sha = get_all_sha(USER, REPO, filepos)
    dict_sha = {i["name"].replace(".csv", ""):i["sha"] for i in sha}
    
    filenames = ["data_playlists", "data_tracks_final", "data_analyse", "moyennes_playlists"]
    main_transfert(filenames, dict_sha, USER, REPO, TOKEN )

    print("OK")
    #### Remplacement des nouvelles données (Remplace dans un autre dossier pour le moment)

    data_playlists_new = pd.DataFrame(get_playlists(client_id_spoti, client_secret_spoti))
    data_data_tracks_final_new = pd.DataFrame(get_tracks(client_id_spoti, client_secret_spoti, data_playlists_new))
    #data_moyennes_playlists_new = pd.DataFrame(get_playlists(client_id_spoti, client_secret_spoti))
    data_data_analyse_new = pd.DataFrame(analyse_tracks(client_id_spoti, client_secret_spoti, data_data_tracks_final_new))
    data_moyennes_playlists_new = get_moyennes_playlists(data_playlists_new, data_data_tracks_final_new, data_data_analyse_new)

    dict_new_data = {"data_playlists":data_playlists_new, "data_tracks_final":data_data_tracks_final_new, "data_analyse":data_data_analyse_new, "moyennes_playlists":data_moyennes_playlists_new}
    
    #### Validé, tout a fonctionné jusqu'ici
    print("I have all data")
    filenames = ["data_analyse", "data_playlists", "data_tracks_final", "moyennes_playlists"]
    filepos2 = "Testfolder"
    sha2 = sp.get_all_sha(USER, REPO, filepos2)
    dict_sha2 = {i["name"].replace(".csv", ""):i["sha"] for i in sha2}
    for filename in filenames: 
        print(filename)
        file_to_encode = pd.DataFrame(dict_new_data[filename])
        encodedfile_playlists = sp.encode_file(file_to_encode)
        print(filename + " updated!")
    sp.main_transfert2(filenames, dict_sha2, USER, REPO, TOKEN )
    print("OK2")

    # On peut potentiellement ajouter les nouveaux fichiers un par un plutôt que de faire une grosse boucle à la fin pour éviter les erreurs
    
main()
