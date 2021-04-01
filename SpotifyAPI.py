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


def get_sha(user, repo, filepos):
    """Permet de générer le token 'sha' d'un fichier, prend en entrée le nom du compte github, le nom du repo et le nom du fichier, 
    renvoie une str comprenant le 'sha'."""
    login2 = requests.get('https://api.github.com/repos/' + user + '/' + repo + '/contents/' + filepos)
    return login2.json()["sha"]

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
                            "sha": get_sha(user, repo, filepos)
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
                time.sleep(10)
                r = requests.get(endpoint, headers=headers) 
            if str(r) == '<Response [401]>' :
                access_token = spoti.get_access_token()
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
            time.sleep(10)
            r = requests.get(endpoint, headers=headers) 
        if str(r) == '<Response [401]>' :
                print("access_token")
                access_token = spoti.get_access_token() 
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
    headers = {
      "Authorization": f"Bearer {access_token}"}
    for i in data_tracks["track_id"]:
        dict_verif["verif"].append(i)
        endpoint = "https://api.spotify.com/v1/audio-features/" + str(i) 
        try:
            r = requests.get(endpoint, headers=headers) 
        except ConnectionError:
            time.sleep(10)
            r = requests.get(endpoint, headers=headers) 
        nb_track += 1
        if str(r) == '<Response [401]>' :
                print("access_token")
                access_token = spoti.get_access_token() 
                headers = {
                  "Authorization": f"Bearer {access_token}"}
                r = requests.get(endpoint, headers=headers)
        try:
            response_dict = json.loads(r.text)
            df_analyse = df_analyse.append(response_dict, ignore_index=True)
            df_analyse.to_csv("data_analyse.csv")
        except:
            pass
        
    return df_analyse



def access_token_build(client_id, client_secret):
    """Génère le token d'accès"""
    spoti = SpotifyAPI(client_id, client_secret)
    return spoti.get_access_token()
    
      

client_id_spoti = str(os.environ.get("ACCOUNT_API_REPO_KEY"))   
client_secret_spoti = str(os.environ.get("ACCOUNT_API_REPO_SECRET"))  




USER = "GrAMATO"
REPO = "Spotify_final"
TOKEN = str(os.environ.get("TOKEN_REPO_ACCESS"))



#### Récupération des playlists

playlists_df = pd.DataFrame(get_playlists(client_id_spoti, client_secret_spoti))

#### Déplacement du fichier précédent dans une archive

url = "https://raw.githubusercontent.com/GrAMATO/Spotify_final/main/data_playlists.csv" 
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))

filepos = "Archives_data/data_playlists_old.csv"
sha = get_sha(USER, REPO, filepos)
encodedfile = encode_file(df)


update_file(USER, REPO, filepos, TOKEN, sha, encodedfile)

#### Remplacement des nouvelles données (Remplace dans un autre dossier pour le moment)

data_playlists_new = pd.DataFrame(get_playlists(client_id_spoti, client_secret_spoti))

filepos = "Testfolder/data_playlists.csv"
sha = get_sha(USER, REPO, filepos)
encodedfile_playlists = encode_file(playlists_df)


update_file(USER, REPO, filepos, TOKEN, sha, encodedfile_playlists)
