import os
import SpotifyConnect
import YoutubeConnect

if __name__ == '__main__':
    # Check for both client_id_secret.json file and quit if it doesnt exist
    if os.path.exists("spotify_client_id_secret.json") is False or os.path.exists("youtube_client_id_secret.json") is False:
        print("Please make sure you have the configuration files: ")
        print("- spotify_client_id_secret.json")
        print("- youtube_client_id_secret.json")
        quit()

    youtube = YoutubeConnect.yt_connect()
    access_token = SpotifyConnect.connect_to_spotify()

    # Get playlists from Spotify and prompt the user what playlist they want to sync to Youtube
    # spotify_user_id = SpotifyConnect.get_user(access_token)
    # spotify_playlists = SpotifyConnect.get_playlists(access_token)

    # TODO: Select a playlist
    # playlist = input('Enter Spotify playlist name you want to use or create: ')
    playlist = "2JFKf7T7Emw7XyH9GLr5PS"
    songs = SpotifyConnect.get_songs(access_token, playlist_id=playlist)

    # Get or create playlist
    playlist_name = input('Enter YT playlist name you want to use or create: ')
    playlist_id = YoutubeConnect.yt_get_playlist(youtube, playlist_name)

    if len(playlist_id) < 1:
        playlist_id = YoutubeConnect.yt_create_playlist(youtube, playlist_name)

    # Get YT URL's
    for song in songs[:10]:
        videoid = YoutubeConnect.yt_search(youtube, "{} - {}".format(song["track"], song["artist"]))
        YoutubeConnect.yt_add_song_to_playlist(youtube, playlist_id, videoid)

        print("https://www.youtube.com/watch?v={}".format(videoid))

