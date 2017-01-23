import json
from collections import Counter
from nltk.corpus import stopwords
import re
import numpy as np
from util import *

#load stop words
stop_words = set(stopwords.words('english'))

print "Loading country songs lyrics...."
country_songs = get_songs("../data/country_lyrics.json")
print "DONE"
print "Generating country dictionary."
country_dictionary = get_dictionary(country_songs)
print "DONE"

print "Loading hiphop song lyrics...."
hiphop_songs = get_songs("../data/hiphop_lyrics.json")
print "DONE"
print "Generating hiphop dictionary"
hiphop_dictionary = get_dictionary(hiphop_songs)
print "DONE"

print "Creating complete dictionary for both"
overlap_dict = list(country_dictionary.intersection(hiphop_dictionary))
print "DONE"

print "Building Country BoWs..."
country_bows = np.array(create_bow_vectors(country_songs, overlap_dict))
print "Saving....."
np.save('../data/country_bows', country_bows)
print "DONE"

print "Building Hiphop BoWs..."
hiphop_bows = np.array(create_bow_vectors(hiphop_songs, overlap_dict))
print "Saving....."
np.save('../data/hiphop_bows', hiphop_bows)
print "DONE"




