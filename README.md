# Lyric Clustering with Multiple Genres
## Essentially this project is me messing around before moving to the text generation

The main bulk of this repo is dedicated to clustering songs into genres based on their lyrics. Although I could collect a dataset of lyrics from all Spotify genres, I focused mainly on clustering hip-hop and country songs because they seem to be different enough genres. At first, I generated the bag of words vectors using simply word occurance in a song after filtering out stop words, creating a long binary vector. Ultimately, the results were alright. The model was really good at seporating out a chunk of rap lyrics, but about half of the rap lyrics were sorted with the country.

[3D graph of clusters after doing PCA on the song vectors](https://plot.ly/~thesiti92/16)

To improve the results, I tried to generate the BOW vectors using normalized frequency counts as opposed to simply word occurance in a song.In preprocessing, I chopped the bottom 25% and top 5% least/most frequent words off of the BOW vocab vector to produce better results, but in the end this method didn't work as well as the previous one. I did, however, dump out these frequency counts to an Excel file and got some cool graphs.

* Vocab_vec.py/vocab_vec_freq.py for creating the vectors 
* norm.py for normalizing/scaling the data when using the frequency counts
* clusters_last_stand.py for clustering the BOW vectors
* lyric_variance.py for analyzing the error of the clusters
