# https://zenn.dev/d0ne1s/scraps/1c2d7d021c05e2 より

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 環境変数にClient IDとClient Secretを設定する
os.environ["SPOTIPY_CLIENT_ID"] = "295130f2a4764bc9a423387a20a3d84c"
os.environ["SPOTIPY_CLIENT_SECRET"] = "a2e47ef747e24bc68809909c2105efda"

# 認証情報を使用してSpotify APIクライアントを作成する
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_drake_tracks():
    # DrakeのSpotifyアーティストID
    drake_id = "3TVXtAsR1Inumwj472S9r4"

    # Drakeのアルバムを取得する
    albums = sp.artist_albums(drake_id, album_type='album')

    # 各アルバムのトラックを取得する
    tracks = []
    for album in albums['items']:
        album_tracks = sp.album_tracks(album['id'])
        for track in album_tracks['items']:
            tracks.append(track['name'])

    return tracks

if __name__ == "__main__":
    drake_tracks = get_drake_tracks()
    for idx, track in enumerate(drake_tracks):
        print(f"{idx + 1}. {track}")