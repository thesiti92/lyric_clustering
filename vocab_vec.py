import json
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
            vocab.append(word)
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

lyrics = json.load(open("country_lyrics.json"))
vocab = parse_vocab(lyrics)
json.dump(vocab, open("country_vocab.json", "w+"))
songs = [get_vocab(lyric, vocab) for lyric in lyrics]
np.dump(songs, open("song_vecs.json", "w+"))
