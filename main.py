import os
import pickle

from SpotifyConnect import SpotifyConnect
from YoutubeConnect import YoutubeConnect


def get_playlist_and_songs(youtubeConnect, spotifyConnect):

    # TODO: Select a playlist
    # Get playlists from Spotify and prompt the user what playlist they want to sync to Youtube
    # spotify_user_id = SpotifyConnect.get_user(access_token)
    # spotify_playlists = SpotifyConnect.get_playlists(access_token)
    # playlist = input('Enter Spotify playlist name you want to use or create: ')
    sf_playlist_id = input('Enter the Spotify playlist ID of the playlist you want to convert: ') #"2JFKf7T7Emw7XyH9GLr5PS" or 1qvjFvI0qCVgtfF67i8OC6
    spotify_songs = spotifyConnect.get_songs(playlist_id=sf_playlist_id)

    # Get or create playlist
    yt_playlist_name = input('Enter YT playlist name you want to use or create: ')
    yt_playlist_id = youtubeConnect.yt_get_playlist_id(yt_playlist_name)

    if len(yt_playlist_id) < 1:
        yt_playlist_id = youtubeConnect.yt_create_playlist(yt_playlist_name)

    return sf_playlist_id, yt_playlist_id, spotify_songs


def check_configuration():
    # Check for both client_id_secret.json file and quit if it doesnt exist
    if os.path.exists("spotify_client_id_secret.json") is False or os.path.exists("youtube_client_id_secret.json") is False:
        print("Please make sure you have the configuration files: ")
        print("- spotify_client_id_secret.json")
        print("- youtube_client_id_secret.json")
        quit()


def get_previous_data():
    # Load previous data if exists
    __sf_playlist_id = None
    __yt_playlist_id = None
    __spotify_songs = None
    __song_offset = None

    if (os.path.exists("pickle_data.p")):
        previous_data = pickle.load(open("pickle_data.p", "rb"))

        print(
            "Do you want to continue importing songs from Spotify playlist {} to Youtube playlist {} continue at song {}".format(
                previous_data["spotify_playlist"],
                previous_data["youtube_playlist"],
                previous_data["offset"]
            ))

        if input("y/n:") == "y":
            __sf_playlist_id = previous_data["spotify_playlist"]
            __yt_playlist_id = previous_data["youtube_playlist"]
            __spotify_songs = previous_data["spotify_songs"]
            __song_offset = int(previous_data["offset"])
        else:
            os.remove("pickle_data.p")

    return (
        __sf_playlist_id,
        __yt_playlist_id,
        __spotify_songs,
        __song_offset
    )


if __name__ == '__main__':
    # Check if config files are available and connect to API's
    check_configuration()

    youtubeConnect = YoutubeConnect()
    spotifyConnect = SpotifyConnect()

    # Load previous data if exists, otherwise get the data
    sf_playlist_id, yt_playlist_id, spotify_songs, song_offset = get_previous_data()
    if sf_playlist_id is None:
        sf_playlist_id, yt_playlist_id, spotify_songs = get_playlist_and_songs(youtubeConnect, spotifyConnect)
        song_offset = 0

    # Get YT URL's
    counter = song_offset
    for song in spotify_songs[song_offset:song_offset+100]:
        try:
            videoid = youtubeConnect.yt_search("{} - {}".format(song["track"], song["artist"]))
            youtubeConnect.yt_add_song_to_playlist(yt_playlist_id, videoid)
            counter += 1
        except:
            print("Error, probably reached YT quota. Please run the script again tomorrow.")
            break

    # Pickle data if not all songs are iterated
    if counter < len(spotify_songs) - 1:
        persistant_data = {"spotify_playlist" : sf_playlist_id, "youtube_playlist" : yt_playlist_id, "spotify_songs" : spotify_songs, "offset" : counter}
        pickle.dump(persistant_data, open("pickle_data.p", "wb"))
    else:
        if (os.path.exists("pickle_data.p")):
            os.remove("pickle_data.p")






