import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


def search_spotify(text: str, i=0, verbose=False) -> dict:
    """
    Function to search spotify.

    Parameters
    ----------
    text: str
    i: int
        ヒットしたトラックのうち、何番目のものを出力するか。
    verbose: bool

    Returns
    -------
    result: dict
    """

    # 環境変数にClient IDとClient Secretを設定する
    # os.environ["SPOTIPY_CLIENT_ID"] = "enter client id here"
    # os.environ["SPOTIPY_CLIENT_SECRET"] = "enter client secret here"

    keywords = text_to_keywords(text)
    name = " ".join(keywords)

    # Acquire matching tracks in Spotify
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    results = spotify.search(q='track:'+name, type='track')

    # Define return value
    if len(results["tracks"]["items"]) == 0:
        if verbose:
            print("No tracks found.")
        return None
    
    else:
        # Report number of tracks
        if verbose:
            print("{} tracks found in Spotify!".format(results["tracks"]["total"]))

        # Artwork, name of track, name of artist
        artwork_url = results["tracks"]["items"][i]["album"]["images"][0]["url"]    # Usually, 'images' have more than 1 artwork.

        # track_name = results["tracks"]["items"][i]["album"]["name"]
        track_name = results["tracks"]["items"][i]["name"]
        track_URL = results["tracks"]["items"][i]["external_urls"]["spotify"]
        album_URL = results["tracks"]["items"][i]["album"]["external_urls"]["spotify"]

        artist_name = results["tracks"]["items"][i]["album"]["artists"][0]["name"]
        artist_URL = results["tracks"]["items"][i]["album"]["artists"][0]["external_urls"]["spotify"]

        result = {
            "track_name": track_name,
            "artist_name": artist_name,
            "track_url": track_URL,
            "album_url": album_URL,
            "artwork_url": artwork_url,
            "artist_url": artist_URL
        }

        return result
    

def text_to_keywords(text: str) -> list:
    """
    Function to convert text about music into keywords.
    For example, if "'Moon River' by Audrey Hepburn" were given as input, the output will be a list ["Moon River", "Audrey Hepburn"].

    Parameters
    ----------
    text: str

    Returns
    -------
    keywords: list
        A list of keywords. Each keywords are str type.
    """

    # replace " and '
    cleaned_text = text.replace('"', '').replace("'", "")
    
    # split text with word "by"
    keywords = cleaned_text.split("by")

    return keywords


if __name__ == "__main__":

    text = "'Moon River' by Audrey Hepburn"
    for i in range(5):
        info = search_spotify(text, i=i, verbose=True)
        print("\n{}th result:\n{}".format(i, info))