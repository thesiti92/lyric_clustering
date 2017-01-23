
import json
import numpy as np

words = json.load(open("2_features.json"))
join = words['country_songs'] + words['rap_songs']
song_distro = {'country':0,'rap':0}
for song in join:
    if song['n-word'] > 1:
        song_distro['rap'] += 1
    else:
        song_distro['country'] += 1
print song_distro
print len(words['country_songs']), len(words['rap_songs'])
