from sklearn.cluster import KMeans
import json
import numpy as np
from datetime import datetime
startTime = datetime.now()
vecs = json.load(open("join_freq_vecs.json"))
means = KMeans(3)
means.fit(vecs)
np.savetxt("freq_3means.dat", means.cluster_centers_)
print datetime.now() - startTime
