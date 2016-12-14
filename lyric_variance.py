import numpy as np
from json import load
from scipy.spatial.distance import euclidean
lyrics = load(open('join_vecs.json'))
country = lyrics[8000:10000]
rap = lyrics[-5000:-2000]
print len(rap)
means = np.loadtxt('mean_join_2vecs.dat')
def genre_clusters(genre):
    return np.bincount([1 if euclidean(vec, means[0])<euclidean(vec, means[1]) else 0 for vec in genre])
print genre_clusters(country)
print genre_clusters(rap)
print [1 if euclidean(vec, means[0])<euclidean(vec, means[1]) else 0 for vec in rap]
