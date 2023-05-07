import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def yt_connect():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "youtube_client_id_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    return youtube


def yt_download(url):
    # return "{}".format(url)
    pass


# Return URI for YT search for video
def yt_search(youtube, query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )

    response = request.execute()
    videoid = response["items"][0]["id"]["videoId"]
    return videoid


def yt_create_playlist(youtube, playlist_name):
    request = youtube.playlists().insert(
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

def yt_add_song_to_playlist(youtube, playlist_id, resource_id):

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": resource_id
            }
          }
        }
    )
    response = request.execute()
    print(response)




