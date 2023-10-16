import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import os
import json
from utility import colorize

# 環境変数にClient IDとClient Secretを設定する
os.environ["SPOTIPY_CLIENT_ID"] = "295130f2a4764bc9a423387a20a3d84c"
os.environ["SPOTIPY_CLIENT_SECRET"] = "a2e47ef747e24bc68809909c2105efda"

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Beethoven Symphony No.7'

results = spotify.search(q='track:'+name, type='track')
target_dict = results["tracks"]
print(target_dict)

# print(target_dict)
# print(colorize(type(target_dict), 41))

# print(results)
# items = results['artists']['items']
# if len(items) > 0:
#     artist = items[0]
#     print(artist['name'], artist['images'][0]['url'])

# pretty_dict = json.dumps(target_dict, indent=4, sort_keys=True)
# print(pretty_dict)

url = results["tracks"]["items"][0]["external_urls"]["spotify"]
preview_url = results["tracks"]["items"][0]["preview_url"]

print("track URL: {}".format(url))
print("preview: {}".format(preview_url))