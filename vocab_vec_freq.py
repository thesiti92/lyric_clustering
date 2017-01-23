import json
import pandas as pd
stopwords = json.load(open('stopwords.json'))
def parse_words(lyric):
    if type(lyric) is list:
        string =  " ".join(lyric)
    else:
        string = lyric
    return string.replace("Chorus:", "").replace('Chorus', "").replace(" \n\n", " ").replace("\n\n", " ").replace(' \n', ' ').replace('\n', ' ').replace("(", "")\
    .replace(")", "").replace("\\", "").replace("/","").replace("?","").replace("!","").replace(",", "").replace(";", "").replace(".", "").replace(":", "")\
    .replace("\"", "").replace("\'", "").replace("*","").replace("  ", ' ').strip().lower().split()
def parse_vocab(lyrics):
    vocab = {}
    words = parse_words(lyrics)
    print len(words)
    for word in words:
        if word not in stopwords:
            if word not in vocab:
                vocab[word] = 1
            else:
                vocab[word] += 1
                    # print word
    return vocab
def get_vocab(lyric, total_vocab):
    lyric_words =  parse_words(lyric)
    # print len(lyric_words)
    vec = []
    for word in total_vocab:
        if word not in lyric_words:
            vec.append(0)
        else:
            vec.append(lyric_words.count(word))
            # print word

    return vec

clyrics = json.load(open("country_lyrics.json"))
rlyrics = json.load(open("hiphop_lyrics.json"))
lyrics = clyrics+rlyrics

vocab = parse_vocab(lyrics)
df = pd.Series(vocab, name='frequency').order().to_frame().reset_index()
df['country'] = df['index'].map(parse_vocab(clyrics))
df['rap'] = df['index'].map(parse_vocab(rlyrics))

adjust1 = int(len(vocab)*.90)
# adjust2 = int(len(vocab)*.0005)

df2 = df[adjust1:]
df2.to_csv("top10percent_words.csv")
print df
# json.dump(vocab, open("join_freq_vocab-trimmed.json", "w+"))
# songs = [get_vocab(lyric, df2["index"].tolist()) for lyric in lyrics]
# json.dump(songs, open("join_freq2_vecs.json", "w+"))
