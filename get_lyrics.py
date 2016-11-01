import json
from PyLyrics import *


with open("country_songs.json", mode='r') as infile:
    songs = json.load(infile)

lyrics = []
for song in songs:
    try:
        lyrics.append(PyLyrics.getLyrics(song['artist'],song['name']))
        print len(lyrics)
    except:
        try:
            print "Failed to get lyrics for %s by %s" % (song['name'], song['artist'])
        except:
            print "Failed to get lyrics for %s" % (song['id'])
with open("country_lyrics.json", mode='w+') as out:
    json.dump(lyrics, out)
