from sklearn.preprocessing import normalize
import json

vecs = json.load(open("join_freq_vecs.json"))
norm_vecs = normalize(vecs, axis=0)
json.dump(norm_vecs.tolist(),open("norm_vecs.json", mode='w+'))
print "normalized"
