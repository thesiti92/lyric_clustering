import numpy as np
import json
from nltk.corpus import stopwords
import re


def loadData(fn):
    return np.load(fn)

def filter_word(w):
    return re.sub('[().,!@#$?:;]', '', w).lower()

def filter_song(song):
    pass

def get_dictionary(songs):
    #load stop words
    stop_words = set(stopwords.words('english'))

    all_words = [Counter(song.split()) for song in songs]
    words = [filter_word(key) for sublist in all_words for key in sublist.keys()]
    words = set(words)
    return set([w for w in words if w not in stop_words])

def get_songs(song_fn):
    with open(song_fn,  mode='r') as infile:
        songs = json.load(infile)
    return songs

def convert_to_bow(song, word_dict):
    bow = np.zeros(len(word_dict))
    v_idx = [word_dict.index(filter_word(word)) for word in song if filter_word(word) in word_dict]
    bow[v_idx] = 1
    return bow

def create_bow_vectors(songs, word_dict):
    all_songs = [Counter(song.split()) for song in songs]
    bows = [convert_to_bow(song, word_dict) for song in all_songs]
    return bows 


