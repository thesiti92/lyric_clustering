from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
import json
import numpy as np
from datetime import datetime
startTime = datetime.now()
vecs = json.load(open("join_freq_vecs.json"))
normalize(vecs, copy=False, axis=0)
print "normalized"
means = KMeans(2)
means.fit(vecs)
np.savetxt("freq_2means_norm.dat", means.cluster_centers_)
print datetime.now() - startTime
