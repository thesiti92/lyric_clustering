import json
# import pandas as pd
# stopwords = json.load(open('stopwords.json'))
# words_we_want = {"n-word": ["nigga", "niggas"], "baby": ["baby", "babe"]}
words_we_want = {"n-word": ["nigga", "niggas"], "yall": ["yall"]}

def parse_words(lyric):
    if type(lyric) is list:
        string =  " ".join(lyric)
    else:
        string = lyric
    return string.replace("Chorus:", "").replace('Chorus', "").replace(" \n\n", " ").replace("\n\n", " ").replace(' \n', ' ').replace('\n', ' ').replace("(", "")\
    .replace(")", "").replace("\\", "").replace("/","").replace("?","").replace("!","").replace(",", "").replace(";", "").replace(".", "").replace(":", "")\
    .replace("\"", "").replace("\'", "").replace("*","").replace("  ", ' ').strip().lower().split()
# def parse_vocab(lyrics):
#     vocab = {}
#     words = parse_words(lyrics)
#     print len(words)
#     for word in words:
#         if word not in stopwords:
#             if word not in vocab:
#                 vocab[word] = 1
#             else:
#                 vocab[word] += 1
#                     # print word
#     return vocab
def get_vocab(lyric):
    lyric_words = parse_words(lyric)
    # print len(lyric_words)
    feats = {"n-word": 0, "yall": 0}
    for word in words_we_want['n-word']:
        feats['n-word'] += lyric_words.count(word)
    for word in words_we_want['yall']:
        feats['yall'] += lyric_words.count(word)
    return feats

clyrics = json.load(open("country_lyrics.json"))
rlyrics = json.load(open("hiphop_lyrics.json"))

# vocab = parse_vocab(lyrics)
# df = pd.Series(vocab, name='frequency').order().to_frame().reset_index()
# adjust1 = int(len(vocab)*.90)
# adjust2 = int(len(vocab)*.0005)

# df2 = df[adjust1:]
# df2.to_csv("top10percent_words.csv")
# print df2
# json.dump(vocab, open("join_freq_vocab-trimmed.json", "w+"))
songs = {}
songs["country_songs"] = [get_vocab(lyric) for lyric in clyrics]
songs["rap_songs"] = [get_vocab(lyric) for lyric in rlyrics]

json.dump(songs, open("2_features_yall.json", "w+"))
