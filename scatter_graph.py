import plotly.plotly as py
import plotly.graph_objs as go
import json
# Create random data with numpy
import numpy as np

words = json.load(open("2_features.json"))
# dtype = dict(names=['n-word', 'baby'])
country_vecs = np.array([song.values() for song in words['country_songs']])
rap_vecs = np.array([song.values() for song in words['rap_songs']])[:len(country_vecs)]
# Create a trace
ctrace = go.Scatter(
    x = country_vecs[:,0],
    y = country_vecs[:,1],
    mode = 'markers',
    marker={"color":"red"},
    name="country"
)
rtrace = go.Scatter(
    x = rap_vecs[:,0],
    y = rap_vecs[:,1],
    mode = 'markers',
    marker = {"color":"blue"},
    name="rap"
)
layout= go.Layout(
    title= 'N-Word vs. Baby',
    hovermode= 'closest',
    xaxis= dict(
        title= 'Baby',
        ticklen= 5,
        gridwidth= 2
    ),
    yaxis=dict(
        title= 'n-word',
        ticklen= 5,
        gridwidth= 2
    ),
    showlegend= True
)

data = [rtrace, ctrace]
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig)
print plot_url
