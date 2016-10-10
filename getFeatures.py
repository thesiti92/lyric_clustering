import csv,base64
from requests import get, post
import json

SEARCH_URL = "https://api.spotify.com/v1/search"
TRACK_URL = "https://api.spotify.com/v1/tracks/"
FEATURES_URL = "https://api.spotify.com/v1/audio-features/"
ALBUM_URL = "https://api.spotify.com/v1/albums/"
AUTH_URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = "8402752d0a084c2395d3c611ca96eb2e"
CLIENT_SECRET = "a42d5cdab34e4734b5e21a6669bdd401"

header = {'Authorization' : "Basic %s" % base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)}
r = post(AUTH_URL, data={'grant_type' : 'client_credentials'}, headers=header)
response = r.json()
print(response)
auth_token = response['access_token']

songs=[]
failed_searches = []
full_list = []
with open('songs.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        songs.append(row)
with open('more_songs.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        songs.append(row)

for song in songs:
    song_info = []
    name = song['song']
    artist = song['artist']
    search_request = get(SEARCH_URL, params={'q': "track:%s artist:%s" % (name, artist), 'type':'track', 'limit':'1'}, headers={"Authorization" : "Bearer %s" % auth_token})
    try:
        search_resp = search_request.json()
        result = search_resp['tracks']['items'][0]
        id = result['id']
        # song_info['popularity'] = result['popularity']
        # song_info['name'] = name
    except:
        print("oh no")
    #     song_info['song_name'] = name
    #     song_info['song_artist'] = artist
    #     print("failed to find %s by %s" % (name, artist))

    features_request = get(FEATURES_URL + id, headers={"Authorization" : "Bearer %s" % auth_token})
    features = features_request.json()
    result['features']=features
    full_list.append(result)


    # try:
    #
    # #     wanted_features = []
    # #     wanted_features.append(features['danceability'])
    # #     wanted_features.append(features['energy'])
    # #     wanted_features.append( features['key'])
    # #     wanted_features.append(features['loudness'])
    # #     wanted_features.append(  features['mode'])
    # #     wanted_features.append(features['speechiness'])
    # #     wanted_features.append(features['acousticness'])
    # #     wanted_features.append( features['instrumentalness'])
    # #     wanted_features.append(features['valence'])
    # #     wanted_features.append(features['tempo'])
    # except:
    #     print("failed to get features for %s by %s" % (song, artist))
    # song_info['features'] = wanted_features
    # full_list.append(song_info)
with open('spotify_dump.json', mode='w') as outfile:
    json.dump(full_list, outfile)
