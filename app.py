from calendar import c
from operator import call
from re import A
import eel
import spotipy
import json

try:
    import spotipy
except ImportError:
    print("Error: spotipy library not found")

@eel.expose
def get_image_url():
    current_track = spotify_object.current_playback()
    if current_track is not None and current_track["is_playing"]:
        current = spotify_object.currently_playing()
        if current is not None:
            artist = current["item"]["album"]["artists"][0]["name"]
            track = current["item"]["name"]
            album = current["item"]["album"]["name"]
            length = current["item"]["duration_ms"]
            progress = current["progress_ms"]
            album_art_url = current["item"]["album"]["images"][0]["url"]
            # print(album_art_url)

            # Create a dictionary with the desired values
            data = {
                "is_playing": True,
                "artist_name": artist,
                "song_title": track,
                "album_name": album,
                "length": length,
                "progress": progress,
                "album_art_url": album_art_url,
            }
        else:
            # Return a dictionary indicating that currently_playing() returned None
            data = {
                "is_playing": False,
                "error": "currently_playing() returned None"
            }
    else:
        # Return a dictionary indicating that music is not playing
        data = {
            "is_playing": False
        }

    # Return the dictionary
    return data


if __name__ == '__main__':
    SPOTIPY_CLIENT_ID = "73404788fd19469ba44c59f7130e5b28"
    SPOTIPY_CLIENT_SECRET = "0fdbfc8a347d4cc3be81f36c80fe31d2"
    SPOTIPY_REDIRECT_URI = "https://google.com"
    GENIUS_ACCESS_TOKEN = "Okbi1ioN5ofQ0P8B5XE2E9SUK7pU26cc8bvxsTIfRdlviikynk5elU_HSK4EDvCp"

    scope = "user-read-currently-playing user-read-playback-state"

    oauth_object = spotipy.SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
    )
    token_dict = oauth_object.get_access_token()
    if token_dict is not None:
        token = token_dict["access_token"]
    # Spotify Object
    spotify_object = spotipy.Spotify(auth=token)


    eel.init('web', ['.html', '.css'])
    eel.start('index.html', size=(720, 720))
