import numpy as np
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt



# setup test data
raw_data = [2.0, 2.0, 2.0], [1.5, 1.5, 1.5], [0.5, 0.5, 0.5],[3.0, 2.0, 1.0], [3.0, 2.0, 1.0],\
       [3.0, 2.0, 1.0], [2.4, 2.5, 2.2], [2.4, 3.0, 2.5], [4.0, 3.3, 8.0]

# convert data into proper format
x_data = []
y_data = []
z_data = []
for item in raw_data:
    x_data.append(item[0])
    y_data.append(item[1])
    z_data.append(item[2])

# get fit parameters from scipy curve fit
parameters, covariance = curve_fit(function, [x_data, y_data], z_data)

# create surface function model
# setup data points for calculating surface model
model_x_data = np.linspace(min(x_data), max(x_data), 30)
model_y_data = np.linspace(min(y_data), max(y_data), 30)
# create coordinate arrays for vectorized evaluations
X, Y = np.meshgrid(model_x_data, model_y_data)
# calculate Z coordinate array
Z = function(np.array([X, Y]), *parameters)

# setup figure object
fig = plt.figure()
# setup 3d object
ax = Axes3D(fig)
# plot surface
ax.plot_surface(X, Y, Z)
# plot input data
ax.scatter(x_data, y_data, z_data, color='red')
# set plot descriptions
ax.set_xlabel('X data')
ax.set_ylabel('Y data')
ax.set_zlabel('Z data')

plt.show()
