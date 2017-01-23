# import json
# words = json.load(open("2_features.json"))
# rap = words['rap_songs']
# rlyrics = json.load(open("hiphop_lyrics.json"))
# print rlyrics[rap.index({"baby":0, "n-word": 92})]

import json
words = json.load(open("2_features.json"))
country = words['country_songs']
clyrics = json.load(open("country_lyrics.json"))
print clyrics[country.index({"baby":0, "n-word": 9})]
