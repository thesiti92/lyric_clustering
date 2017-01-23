from sklearn.cluster import KMeans
import json
import numpy as np
from datetime import datetime
startTime = datetime.now()
vecs = json.load(open("scaled2_vecs.json"))
print vecs[0]
means = KMeans(3)
means.fit(vecs)
np.savetxt("freq_3means_scaled.dat", means.cluster_centers_)
print datetime.now() - startTime
