'''
'''

import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import time
import numpy as np


def addColumns(df):
    df['theta']       = (df['theta_min'] +  df['theta_max'])/2
    df['Delta_theta'] = (df['theta_max'] -  df['theta_min'])/2
    df['p']           = (df['p_min']     +  df['p_max']    )/2
    df['Delta_p']     = (df['p_max']     -  df['p_min']    )/2
    df['x_F']         = 0.06451612903*df['p']*np.cos(0.001*df['theta'])  # 0.06451612903 is for 2/sqrt(s) #0.001 is mrad --> rad
    return df



#Read Dataframe
df_KPlus = pd.read_csv("SHINE31GeV_Kaon_Data_K+.csv")
df_KPlus.dropna(inplace=True)

df_KMinus = pd.read_csv("SHINE31GeV_Kaon_Data_K-.csv")
df_KMinus.dropna(inplace=True)


df_KZeros = pd.read_csv("SHINE31GeV_Kaon_Data_K0S.csv")
df_KZeros.dropna(inplace=True)

df_KPlus  = addColumns(df_KPlus)
df_KMinus = addColumns(df_KMinus)
df_KZeros = addColumns(df_KZeros)



fig, (ax1,ax) = plt.subplots(1,2, figsize=(10, 6), gridspec_kw={'width_ratios': [1, 3]})
ax.scatter(x = df_KPlus['x_F'] , y = df_KPlus['dKdThetadP']  , label="KPlus"      )
#ax.scatter(x = df_KMinus['x_F'], y = df_KMinus['dKdThetadP'] , label="KMinus"     )
#ax.scatter(x = df_KZeros['x_F'], y = df_KZeros['dKdThetadP'] , label="KZeros"     )


ax.legend()
ax.set(xlabel='FeynmanX', ylabel='Differential Yield')


plt.show()



