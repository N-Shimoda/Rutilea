import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import json

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'

results = spotify.search(q='track:'+name, type='track')
target_dict = results["tracks"]

# print(target_dict)
print(type(target_dict))

# print(results)
# items = results['artists']['items']
# if len(items) > 0:
#     artist = items[0]
#     print(artist['name'], artist['images'][0]['url'])

pretty_dict = json.dumps(target_dict, indent=4, sort_keys=True)
print(pretty_dict)