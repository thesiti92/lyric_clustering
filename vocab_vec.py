import json
from PyDictionary import PyDictionary

dict = PyDictionary()

def parse_words(lyric):
    if type(lyric) is list:
        string =  " ".join(lyric)
    else:
        string = lyric
    return string.replace("Chorus:", "").replace('Chorus', "").replace(" \n\n", " ").replace("\n\n", " ").replace(' \n', ' ').replace('\n', ' ').replace("(", "")\
    .replace(")", "").replace("\\", "").replace("/","").replace("?","").replace("!","").replace(",", "").replace(";", "").replace(".", "").replace(":", "")\
    .replace("\"", "").replace("\'", "").replace("*","").replace("  ", ' ').strip().lower().split()
def parse_vocab(lyrics):
    vocab = []
    words = parse_words(lyrics)
    for word in words:
        if word not in vocab:
            #parses out all non-nouns
            defn = dict.meaning(word)
            if defn is None:
                continue
            elif 'Noun' in defn.keys():
                vocab.append(word)
                print word
    return vocab
def get_vocab(lyric, total_vocab):
    lyric_words =  parse_words(lyric)
    print len(lyric_words)
    vec = []
    for word in total_vocab:
        if word not in lyric_words:
            vec.append(0)
        else:
            vec.append(1)
            print word

    return vec

clyrics = json.load(open("country_lyrics.json"))
rlyrics = json.load(open("hiphop_lyrics.json"))
lyrics = clyrics+rlyrics
vocab = parse_vocab(lyrics)
json.dump(vocab, open("join_vocab.json", "w+"))

#songs = [get_vocab(lyric, vocab) for lyric in lyrics]
#json.dump(songs, open("hiphop_vecs.json", "w+"))
