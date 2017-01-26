import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
from util import *


def projectData(data, ndim=2):
  return PCA(n_components=ndim).fit_transform(data)


def plotData(data, colors,text, genre=None, means=None,  all_means=None):

  data_proj = projectData(data, 3)
 
  p_data = []
  """
  trace2 = go.Scatter(
            x=data_proj[:,0],
            y=data_proj[:,1],
            text=text,
            mode='markers',
            marker=dict(
                size=12,
                opacity=1,
                color=colors,
                line= dict(width=3,
                          color=genre),
                colorscale='Jet',
                symbol='o'
            
            )
        )
    """


  trace2 = go.Scatter3d(
        x=data_proj[:,0],
        y=data_proj[:,1],
        z=data_proj[:,2],
        mode='markers',
        marker=dict(
            size=6,
            color=colors,
            line= dict(width=6,
                      color=genre),
            #color=error,
            colorscale='Jet',
            #opacity=0.5
        )   
    )   

  p_data.append(trace2)


  layout = go.Layout( hovermode="closest" )

  fig = go.Figure(data=p_data, layout=layout)
  plot_url = py.plot(fig, filename='kmeans_result')
  return plot_url


if __name__ == "__main__":

  n_centroids = 4
  n_points = 2000
  models = [KMeans(n_clusters = n_centroids)]

  print "Loading BoW Data..."
  data = loadData('../data/country_bows.npy')
  data2 = loadData('../data/hiphop_bows.npy')
  data = np.vstack((data[:1000,:],data2[:1000,:]))

  print "Standardizing Data..."
  # zero mean and unit variance
  #data = StandardScaler().fit_transform(data)
  # unit length (l2 norm = 1)
  data = Normalizer().fit_transform(data)
  print "DONE"

  for model in models:
    print "Building Model: %s", model
    model.fit(data[:n_points, :])
    print "DONE"
    print "plotting"
    data_proj = plotData(data[:n_points,:], model.labels_, range(n_points), ['green']*1000 + ['orange']*1000)
    print "DONE"
