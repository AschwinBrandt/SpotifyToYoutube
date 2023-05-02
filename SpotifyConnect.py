import requests
import json

def connect_to_spotify():
    # http://localhost:8888/redirect

    access_token = ""

    # Read clientid and secret from file
    f = open('spotify_client_id_secret.json')
    f_client_id_secret = json.load(f)
    client_id = f_client_id_secret["client_id"]
    client_secret = f_client_id_secret["client_secret"]

    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        json_response = json.loads(response.content)
        access_token = json_response["access_token"]
    else:
        print("Something went wrong getting the access_token!")

    return access_token




def get_songs(access_token, playlist_id):
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    header = {"Authorization": "Bearer " + access_token}

    songs = []
    while url:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            json_response = json.loads(response.content)
            tracks = json_response["items"]
            url = json_response["next"]

            for track in tracks:
                track_name = track["track"]["name"]
                artist = track["track"]["artists"][0]["name"]
                songs.append({'artist': artist, 'track': track_name})
        else:
            print("Something went wrong getting the songs_iteratie_1.json!")

    return songs

