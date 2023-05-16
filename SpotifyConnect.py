import requests
import json

class SpotifyConnect:

    __access_token = None

    def __init__(self):
        self.__connect_to_spotify()

    def __connect_to_spotify(self):
        # http://localhost:8888/redirect

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
            self.__access_token = json_response["access_token"]
        else:
            print("Something went wrong getting the access_token!")


    # def get_user(access_token):
        # # https://api.spotify.com/v1/me
        # url = "https://api.spotify.com/v1/me"
        # header = {"Authorization": "Bearer " + access_token}
        #
        # user_id = None
        # response = requests.get(url, headers=header)
        # if response.status_code == 200:
        #     json_response = json.loads(response.content)
        #     user_id = json_response["id"]
        # else:
        #     print("Request failed with error code {}".format(response.status_code))

    # def get_playlists(access_token, user_id):
    #     url = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
    #     header = {"Authorization": "Bearer " + access_token}
    #
    #     playlists = []
    #     while url:
    #         response = requests.get(url, headers=header)
    #         if response.status_code == 200:
    #             json_response = json.loads(response.content)
    #             url = json_response["next"]
    #             print(url)

    def get_songs(self, playlist_id):
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        header = {"Authorization": "Bearer " + self.__access_token}

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
                print("Something went wrong getting the songs_iteratie_1.json!") #TODO

        return songs

