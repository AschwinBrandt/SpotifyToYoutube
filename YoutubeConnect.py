import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class YoutubeConnect:

    __scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    __youtube = None

    def __init__(self):
        self.__yt_connect()

    def __yt_connect(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "youtube_client_id_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, self.__scopes)
        credentials = flow.run_console()

        __youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    def yt_download(self, url):
        # return "{}".format(url)
        pass

    # Return URI for YT search for video
    def yt_search(self, query):
        request = self.__youtube.search().list(
            part="snippet",
            maxResults=1,
            q=query,
            type="video"
        )

        response = request.execute()
        videoid = response["items"][0]["id"]["videoId"]
        return videoid

    def yt_get_playlist_id(self, playlist_name):

        playlist_id = ""

        # TODO: Add pagination in case people have more then 50 playlists
        request = self.__youtube.playlists().list(
            part="snippet",
            mine="true",
            maxResults=50
        )
        response = request.execute()

        for item in response["items"]:
            if item["snippet"]["title"] == playlist_name:
                playlist_id = item["id"]

        return playlist_id

    def yt_create_playlist(self, playlist_name):
        request = self.__youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": playlist_name
                }
            }
        )
        response = request.execute()
        playlist_id = response["id"]
        return playlist_id

    def yt_add_song_to_playlist(self, playlist_id, resource_id):

        request = self.__youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": resource_id
                }
              }
            }
        )
        response = request.execute()
        print(response)




