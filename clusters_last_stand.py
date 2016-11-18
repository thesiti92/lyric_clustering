from sklearn.cluster import KMeans
import json
import numpy as np
from datetime import datetime
startTime = datetime.now()
vecs = json.load(open("song_vecs.json"))
means = KMeans(6)
means.fit(vecs)
np.savetxt("mean_6vecs.dat", means.cluster_centers_)
print datetime.now() - startTime
print means.inertia_
