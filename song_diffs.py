import numpy as np
song1 = np.array([0,0,1,0,1,1,0,1,0,0,0,1])
song2= np.array([0,0,0,0,1,1,0,1,0,1,0,1])

diff = song1-song2
diff[diff==-1]=0
print diff
