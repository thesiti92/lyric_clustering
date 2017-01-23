import plotly.plotly as py
import plotly.graph_objs as go
import json
# Create random data with numpy
import numpy as np

words = json.load(open("2_features.json"))
country_vecs = np.array([song.values() for song in words['country_songs']])
rap_vecs = np.array([song.values() for song in words['rap_songs']])[:len(country_vecs)]

bar = go.Bar(
    x = ['country', 'rap'],
    y = [np.mean(country_vecs[:,1]), np.mean(rap_vecs[:,1])],
    marker={"color":["red", "green", "blue"]},
    )

layout= go.Layout(
    title= 'Average N-Words in Rap vs. Country',
    hovermode= 'x'
)

data = [bar]
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename="average n-words")
print plot_url
