import sklearn.cluster as clu
import json
def parse_words(lyric, array=True):
    if array:
        string =  " ".join(lyric)

    else:
        string = lyric
    return string.replace("Chorus:", "").replace('Chorus', "").replace(" \n\n", " ").replace("\n\n", " ").replace(' \n', ' ').replace('\n', ' ').replace("(", "")\
    .replace(")", "").replace("\\", "").replace("/","").replace("?","").replace("!","").replace(",", "").replace(";", "").replace(".", "").replace(":", "")\
    .replace("\"", "").replace("\'", "").replace("*","").replace("  ", ' ').strip().lower().split()
def parse_vocab(lyrics):
    vocab = []
    words = parse_words(lyrics)
    print len(words)
    for word in words:
        if word not in vocab:
            vocab.append(word)
    return vocab
def get_vocab(lyric, total_vocab):
    lyric_words =  parse_words(lyric)
    print len(lyric_words)
    vocab_ = []
    for word in total_vocab:
        if word in lyric_words:
            vocab_.append(1)
            print word
        else:
            vocab_.append(0)
    return vocab_

lyrics = json.load(open("country_lyrics.json"))
vocab = parse_vocab(lyrics)
print len(vocab)
song_vocab = get_vocab(lyrics[0], vocab)
print(song_vocab)
