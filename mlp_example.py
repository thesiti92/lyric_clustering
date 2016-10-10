from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import json
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
features=[]
Y=[]

with open('song_details.json', mode="r") as i:
    songs = json.load(i)
    for song in songs:
        features.append(song['features'])
        Y.append(song['popularity'])
X = np.vstack(features)
clf = MLPRegressor(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(5, 5), random_state=1)
x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=42)
feat_keys = ['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','valence','tempo']
clf.fit(x_train, y_train)
default = [0.862, 0.608, 7, -4.762, 1, 0.0402, 0.00373, 6.14e-06, 0.825, 120.002]
f_min = X.min(0)
f_max = X.max(0)
for i in range(0,len(default)):
    x = []
    y = []
    cur_min = f_min[i]
    cur_max = f_max[i]
    for j in np.arange(cur_min,cur_max,0.01):
        x.append(j)
        new=default
        new[i]=j
        y.append(clf.predict(new))
    plt.figure(i)
    plt.ylim([0,100])
    plt.scatter(x, y)
    plt.xlabel("%s value from %s-%s" % (feat_keys[i], cur_min, cur_max))
    plt.ylabel("popularity")

print (clf.score(x_test,y_test))

plt.show()
