import os
import SpotifyConnect
import YoutubeConnect

if __name__ == '__main__':
    # TODO: Check for both client_id_secret.json file and quit if it doesnt exist
    if os.path.exists("spotify_client_id_secret.json") is False and os.path.exists("youtube_client_id_secret.json") is False:
        print("Please make sure the configuration files spotify_client_id_secret.json and youtube_client_id_secret.json exists and contain the correct values")
        quit()

    youtube = YoutubeConnect.yt_connect()
    access_token = SpotifyConnect.connect_to_spotify()

    # Get songs from Spotify
    songs = SpotifyConnect.get_songs(access_token, playlist_id="2JFKf7T7Emw7XyH9GLr5PS")

    # Get YT URL's
    yt_urls = []
    for song in songs[:1]:
        videoid = YoutubeConnect.yt_search(youtube, "{} - {}".format(song["track"], song["artist"]))
        yt_urls.append(videoid)
        print("https://www.youtube.com/watch?v={}".format(videoid))