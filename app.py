# import lyricsgenius as lg
import spotipy
import time
import json
import os
from flask import Flask, jsonify, render_template

SPOTIPY_CLIENT_ID = "8a2908991bf3476193849ec660a18e22"
SPOTIPY_CLIENT_SECRET = "95aa3215633241e2b729868ff0b4961f"
SPOTIPY_REDIRECT_URI = "https://google.com"
GENIUS_ACCESS_TOKEN = "Okbi1ioN5ofQ0P8B5XE2E9SUK7pU26cc8bvxsTIfRdlviikynk5elU_HSK4EDvCp"

scope = "user-read-currently-playing user-read-playback-state"

oauth_object = spotipy.SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
)
token = None  # Define a default value
token_dict = oauth_object.get_access_token()
if token_dict is not None:
    token = token_dict["access_token"]
    # Use the token to make API requests
else:
    # Handle the case where get_access_token() returned None
    print("Error: get_access_token() returned None")

# Spotify Object
spotify_object = spotipy.Spotify(auth=token)

# Genius Object
# genius = lg.Genius(GENIUS_ACCESS_TOKEN)

current = spotify_object.currently_playing()
# print(json.dumps(playing, sort_keys=False, indent=4))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/currently_playing_info")
def get_image_url():
    current_track = spotify_object.current_playback()
    if current_track is not None and current_track["is_playing"]:
        current = spotify_object.currently_playing()
        print(current)
        if current is not None:
            artist = current["item"]["album"]["artists"][0]["name"]
            track = current["item"]["name"]
            album = current["item"]["album"]["name"]
            length = current["item"]["duration_ms"]
            progress = current["progress_ms"]
            album_art_url = current["item"]["album"]["images"][0]["url"]

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

    # Return the dictionary as JSON
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5000)

# while True:
#     current = spotify_object.currently_playing()
#     status = current['currently_playing_type']

#     if status == "track":
#         artist_name = current['item']['album']['artists'][0]['name']
#         song_title = current['item']['name']
#         length = current['item']['duration_ms']
#         progress = current['progress_ms']
#         time_left = int(((length-progress)/1000))
#         album_art_url = current['item']['album']['images'][0]['url']

#         # Download the image and open it with PIL
#         response = requests.get(album_art_url)
#         image = Image.open(BytesIO(response.content))
#         # Get the current time as a timestamp string
#         timestamp = str(int(time.time()))

#         # Construct the new file name with the timestamp
#         new_file_name = 'img_' + timestamp + '.jpg'
#         # Save the image to a file
#         image.save(new_file_name)

#         # song = genius.search_song(title=song_title, artist=artist_name)
#         # lyrics = song.lyrics
#        # print(lyrics)
#         time.sleep(time_left)

#     elif status == "ad":
#         time.sleep(30)
