import numpy as np
import json
def round(arr, min=.5, max=1):
    return [1 if x>min and x<max else 0 for x in arr]
means = np.apply_along_axis(round, 0, np.loadtxt('mean_6vecs.dat'))
# diff = np.setdiff1d(zero, one)
print means.shape
# print [np.nonzero(mean) for mean in means]
vocab = json.load(open("country_vocab.json"))
mean_vocab = np.array([[vocab[i] for i in np.nonzero(mean)[0]] for mean in means])

print mean_vocab
print len(mean_vocab)
