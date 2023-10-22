import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


def search_spotify(name: str) -> tuple:
    # 環境変数にClient IDとClient Secretを設定する
    os.environ["SPOTIPY_CLIENT_ID"] = "295130f2a4764bc9a423387a20a3d84c"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "a2e47ef747e24bc68809909c2105efda"

    # Acquire matching tracks in Spotify
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    results = spotify.search(q='track:'+name, type='track')

    if len(results["tracks"]["items"]) == 0:
        print("No tracks found.")
        return None
    
    else:
        # Artwork, name of track, name of artist
        artwork_url = results["tracks"]["items"][0]["album"]["images"][0]["url"]    # Usually, 'images' have more than 1 artwork.

        track_name = results["tracks"]["items"][0]["album"]["name"]
        track_URL = results["tracks"]["items"][0]["album"]["external_urls"]["spotify"]

        artist_name = results["tracks"]["items"][0]["album"]["artists"][0]["name"]
        artist_URL = results["tracks"]["items"][0]["album"]["artists"][0]["external_urls"]["spotify"]

        result = {
            "artwork_url": artwork_url,
            "track_name": track_name,
            "track_url": track_URL,
            "artist_name": artist_name,
            "artist_url": artist_URL
            }
        
        print(result)

        return result


if __name__ == "__main__":

    info = search_spotify("Romantic Dinner")
    print(info)