from sklearn.preprocessing import normalize, scale
import json

vecs = json.load(open("join_freq2_vecs.json"))
# norm_vecs = normalize(vecs, axis=0)
# json.dump(norm_vecs.tolist(),open("norm2_vecs.json", mode='w+'))
scaled_vecs = scale(vecs, axis=0)
json.dump(scaled_vecs.tolist(),open("scaled2_vecs.json", mode='w+'))
