import numpy as np
import json
def round(arr, min=.5, max=1):
    return [1 if x>min and x<=max else 0 for x in arr]
vecs = np.loadtxt('swears_2means.dat')
rmeans = np.apply_along_axis(round, 0, vecs, min=.3, max= .5)
print rmeans.shape
diff = np.subtract(rmeans[1], rmeans[0])
mean_d = np.apply_along_axis(round, 0, diff)

# print [np.nonzero(mean) for mean in means]
vocab = np.array(json.load(open("join_swear_vocab.json")))
# mean_vocab = np.array([[vocab[i] for i in np.nonzero(mean)[0]] for mean in means])
print vocab[np.nonzero(mean_d)]
