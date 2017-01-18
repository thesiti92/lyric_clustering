import numpy as np
from json import load
from scipy.spatial.distance import euclidean
lyrics = load(open('norm_vecs.json'))
# country = lyrics[8000:10000]
# rap = lyrics[-5000:-2000]
# print len(rap)
means = np.loadtxt('freq_2means_norm.dat')
# print means.shape
def genre_clusters(genre=lyrics):
    return np.bincount([np.argmin([euclidean(vec, mean) for mean in means]) for vec in genre])
print genre_clusters()
# print genre_clusters(rap)
# print [1 if euclidean(vec, means[0])<euclidean(vec, means[1]) else 0 for vec in rap]
