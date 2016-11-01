import base64
from requests import get, post
import json
import argparse

parser = argparse.ArgumentParser()

FEATURES_URL = "https://api.spotify.com/v1/audio-features/"
AUTH_URL = "https://accounts.spotify.com/api/token"
PLAYLIST_URL = "https://api.spotify.com/v1/users/%s/playlists/%s/tracks"
CATAGORIES_URL = "https://api.spotify.com/v1/browse/categories"
CLIENT_ID = "8402752d0a084c2395d3c611ca96eb2e"
CLIENT_SECRET = "a42d5cdab34e4734b5e21a6669bdd401"
CAT_PLIST_URL = "https://api.spotify.com/v1/browse/categories/%s/playlists"
REC_URL = "https://api.spotify.com/v1/recommendations"
auth_header = {'Authorization' : "Basic %s" % base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)}
plist_params = {'fields': 'items(track(name,popularity,id,artists(name,id)))', 'limit': "100"}

parser.add_argument("-c", default="country")

def get_songs_from_genre(genre):
    r = post(AUTH_URL, data={'grant_type' : 'client_credentials'}, headers=auth_header)
    response = r.json()
    authed_header={"Authorization" : "Bearer %s" % response['access_token']}

    lists_request = get(CAT_PLIST_URL % genre, headers=authed_header, params={'limit': 50})
    try:
        playlists = lists_request.json()['playlists']['items']
    except:
        print lists_request.json()
        return
    songs = []
    for playlist in playlists:
        id = playlist['id']
        owner = playlist['owner']['id']
        plist_request = get(PLAYLIST_URL % (owner, id), headers=authed_header, params=plist_params)
        tracks = plist_request.json()['items']
        for track in tracks:
            try:
                data = track['track']
                t_id = data['id']
                to_add = {'name' : data['name'], 'artist': data['artists'][0]['name'],"popularity": data['popularity'], 'id' : t_id}
                if to_add not in songs:
                    songs.append(to_add)
                    len(songs)
            except:
                print "Failed to parse track from %s, %s, %s" % (playlist['name'], owner, id)
                continue
            rec_request = get(REC_URL, params={'seed_tracks': t_id, 'seed_genres' : 'genre', 'limit':100}, headers=authed_header)
            rec_tracks = rec_request.json()['tracks']
            for rec_track in rec_tracks:
                try:
                    to_add = {'name' : rec_track['name'], 'artist': rec_track['artists'][0]['name'],"popularity": rec_track['popularity'], 'id' : rec_track['id']}
                except:
                    print "Failed to parse track"
                    continue
                if to_add not in songs:
                    songs.append(to_add)
                    print len(songs)
    with open('%s_songs.json' % genre, mode='w+') as out:
        json.dump(songs, out, indent=2)

args = parser.parse_args()
if args.c == 'all':
    with open('catagories.json', mode='r') as cats:
        catagories = json.load(cats)
    for catagory in catagories:
        print catagory
        get_songs_from_genre(catagory)
else:
    get_songs_from_genre(args.c)
