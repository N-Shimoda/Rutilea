import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

def image_to_text(image):
    pass


def search_spotify(name: str) -> tuple:
    # 環境変数にClient IDとClient Secretを設定する
    os.environ["SPOTIPY_CLIENT_ID"] = "295130f2a4764bc9a423387a20a3d84c"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "a2e47ef747e24bc68809909c2105efda"

    # Acquire matching tracks in Spotify
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    results = spotify.search(q='track:'+name, type='track')

    # Artwork, name of track, name of artist
    artwork_url = results["tracks"]["items"][0]["album"]["images"][0]

    track_name = results["tracks"]["items"][0]["album"]["name"]
    track_URL = results["tracks"]["items"][0]["album"]["external_urls"]["spotify"]

    artist_name = results["tracks"]["items"][0]["album"]["artists"][0]["name"]
    artist_URL = results["tracks"]["items"][0]["album"]["artists"][0]["external_urls"]["spotify"]

    return artwork_url, track_name, track_URL, artist_name, artist_URL