'''
A few functions to plot the 31 GeV SHINE data
Two modes available: 2D and 3D, just try them
run with 

python 

'''

from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from mpl_toolkits.mplot3d.axes3d import get_test_data

import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import time
import numpy as np
import math
import argparse

    


# Modify the dataframes to add a number of variables
def addColumns(df):
    df['theta']       = (df['theta_min'] +  df['theta_max'])/2
    df['Delta_theta'] = (df['theta_max'] -  df['theta_min'])/2
    df['p']           = (df['p_min']     +  df['p_max']    )/2
    df['Delta_p']     = (df['p_max']     -  df['p_min']    )/2
    df['Uncert']      = np.sqrt(df['Stat']*df['Stat'] + df['Sys']*df['Sys'] )
    df['p_T']         = df['p']*np.sin(0.001*df['theta'])  #0.001 is mrad --> rad
    df['p_L']         = df['p']*np.cos(0.001*df['theta'])  #0.001 is mrad --> rad
    df['x_F']         = df['p']/31.  # I'm using xF = P_lab/E_protonIncident which is 31 GeV/c
    return df


# Bogus 3D fit function
def Fit3DFunction(data, a, b, c):
    x = data[0]
    y = data[1]
    return a * (x**b) * (y**c)



# Read running options
parser = argparse.ArgumentParser()
parser.add_argument("a")
args = parser.parse_args()



#Read Dataframe
df_KPlus = pd.read_csv("SHINE31GeV_Kaon_Data_K+.csv")
df_KPlus.dropna(inplace=True)

df_KMinus = pd.read_csv("SHINE31GeV_Kaon_Data_K-.csv")
df_KMinus.dropna(inplace=True)

df_KZeros = pd.read_csv("SHINE31GeV_Kaon_Data_K0S.csv")
df_KZeros.dropna(inplace=True)

# Add new variables to all dFs
df_KPlus  = addColumns(df_KPlus)
df_KMinus = addColumns(df_KMinus)
df_KZeros = addColumns(df_KZeros)

###  I don't remember what this does,  but it was important at a certain point, so lets keep it
dFs_Plus    = df_KPlus.groupby('theta_max')
angles_Plus = df_KPlus['theta_max'].unique()

dFs_Minus    = df_KMinus.groupby('theta_max')
angles_Minus = df_KMinus['theta_max'].unique()

dFs_Zeros    = df_KZeros.groupby('theta_max')
angles_Zeros = df_KZeros['theta_max'].unique()

''' 
#Some debug
print(angles_Plus)
print(angles_Minus)
print(angles_Zeros)
'''

# If we're plotting the 3D curves
if args.a == '3D':
    # get fit parameters from scipy curve fit
    parameters, covariance = curve_fit(Fit3DFunction, [df_KPlus['p_T'],  df_KPlus['x_F'] ],df_KPlus['dKdThetadP'])
    # create surface function model
    # setup data points for calculating surface model
    model_x_data = np.linspace(min(df_KPlus['p_T']), max(df_KPlus['p_T']), 30)
    model_y_data = np.linspace(min(df_KPlus['x_F']), max(df_KPlus['x_F']), 30)
    # create coordinate arrays for vectorized evaluations
    X, Y = np.meshgrid(model_x_data, model_y_data)
    # calculate Z coordinate array
    Z = Fit3DFunction(np.array([X, Y]), *parameters)


    # set up a figure 
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.scatter3D (df_KPlus['p_T'],  df_KPlus['x_F'],  df_KPlus['dKdThetadP'], color='orange', linewidth=0, antialiased=False)
    ax.plot_surface(X, Y, Z)
    ax.set(xlabel='p_T [GeV/c]', ylabel= 'x_F [unitless]', zlabel='Differential Yield [mb/rad/(GeV/c)]')
    plt.title("Positive Kaons, 31 GeV/c data")
    
# in all other cases
else:
    fig, ax = plt.subplots(2,math.ceil(len(df_KZeros['theta_min'].unique())/2), figsize=(16, 8))
    for count, a in enumerate(angles_Minus):
        df_plus  = dFs_Plus .get_group(a)
        df_minus = dFs_Minus.get_group(a)
        if a > 20:
            df_zeros = dFs_Zeros.get_group(a)
        if count < 4:
            ax[0,count].errorbar(df_plus['p'] ,df_plus['dKdThetadP'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert'] , label="K Plus" ,marker="o", markersize=10,ls='none')
            ax[0,count].errorbar(df_minus['p'],df_minus['dKdThetadP'],xerr=df_minus['Delta_p'], yerr=df_minus['Uncert'], label="K Minus",marker="o", markersize=10,ls='none')
            ax[0,count].legend()
            ax[0,count].set(xlabel='Momentum', ylabel='Differential Yield')    
        else:
            ax[1,count-4].errorbar(df_plus['p'] ,df_plus['dKdThetadP'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert'] , label="K Plus"  ,marker="o", markersize=10,ls='none')
            ax[1,count-4].errorbar(df_minus['p'],df_minus['dKdThetadP'],xerr=df_minus['Delta_p'], yerr=df_minus['Uncert'], label="K Minus" ,marker="o", markersize=10,ls='none')
            ax[1,count-4].legend()
            ax[1,count-4].set(xlabel='Momentum', ylabel='Differential Yield')        


plt.show()
