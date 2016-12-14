from sklearn.cluster import KMeans
import json
import numpy as np
from datetime import datetime
startTime = datetime.now()
vecs = json.load(open("join_vecs.json"))
means = KMeans(2)
means.fit(vecs)
np.savetxt("mean_join_2vecs.dat", means.cluster_centers_)
print datetime.now() - startTime
print means.inertia_
