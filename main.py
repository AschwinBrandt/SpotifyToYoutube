import os
import pickle
import SpotifyConnect
import YoutubeConnect

def get_playlist_and_songs(access_token):

    # TODO: Select a playlist
    # Get playlists from Spotify and prompt the user what playlist they want to sync to Youtube
    # spotify_user_id = SpotifyConnect.get_user(access_token)
    # spotify_playlists = SpotifyConnect.get_playlists(access_token)
    # playlist = input('Enter Spotify playlist name you want to use or create: ')
    spotify_playlist = "2JFKf7T7Emw7XyH9GLr5PS"
    spotify_songs = SpotifyConnect.get_songs(access_token, playlist_id=spotify_playlist)

    # Get or create playlist
    youtube_playlist = input('Enter YT playlist name you want to use or create: ')
    yt_playlist_id = YoutubeConnect.yt_get_playlist(youtube, youtube_playlist)

    if len(yt_playlist_id) < 1:
        yt_playlist_id = YoutubeConnect.yt_create_playlist(youtube, youtube_playlist)

    return spotify_playlist, yt_playlist_id, spotify_songs

if __name__ == '__main__':
    # Check for both client_id_secret.json file and quit if it doesnt exist
    if os.path.exists("spotify_client_id_secret.json") is False or os.path.exists("youtube_client_id_secret.json") is False:
        print("Please make sure you have the configuration files: ")
        print("- spotify_client_id_secret.json")
        print("- youtube_client_id_secret.json")
        quit()

    # Connect to API's
    youtube = YoutubeConnect.yt_connect()
    access_token = SpotifyConnect.connect_to_spotify()

    # Load previous data if exists
    spotify_playlist = ""
    yt_playlist_id = ""
    spotify_songs = {}
    song_offset = 0

    if (os.path.exists("pickle_data.p")):
        previous_data = pickle.load(open("pickle_data.p", "rb"))

        print("Do you want to continue importing songs from Spotify playlist {} to Youtube playlist {} continue at song {}".format(
            previous_data["spotify_playlist"],
            previous_data["youtube_playlist"],
            previous_data["offset"]
        ))

        if input("y/n:") == "y":
            spotify_playlist = previous_data["spotify_playlist"]
            yt_playlist_id = previous_data["youtube_playlist"]
            spotify_songs = previous_data["spotify_songs"]
            song_offset = int(previous_data["offset"])
        else:
            os.remove("pickle_data.p")
            spotify_playlist, yt_playlist_id, songs = get_playlist_and_songs(access_token)
    else:
        spotify_playlist, yt_playlist_id, songs = get_playlist_and_songs(access_token)



    # Get YT URL's
    counter = song_offset
    for song in songs[song_offset:song_offset+100]:
        try:
            videoid = YoutubeConnect.yt_search(youtube, "{} - {}".format(song["track"], song["artist"]))
            YoutubeConnect.yt_add_song_to_playlist(youtube, yt_playlist_id, videoid) #TODO: Fetch errors when quota is reached
            counter += 1
        except:
            print("Error, probably reached YT quota. Please run the script again tomorrow.")
            break


    # Pickle data if not all songs are iterated
    if counter < len(songs) - 1:
        persistant_data = {"spotify_playlist" : spotify_playlist, "youtube_playlist" : yt_playlist_id, "spotify_songs" : songs, "offset" : counter}
        pickle.dump(persistant_data, open("pickle_data.p", "wb"))






