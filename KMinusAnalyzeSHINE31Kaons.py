'''
'''

import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import time
import numpy as np
import math

def addColumns(df):
    df['theta']       = (df['theta_min'] +  df['theta_max'])/2
    df['Delta_theta'] = (df['theta_max'] -  df['theta_min'])/2
    df['p']           = (df['p_min']     +  df['p_max']    )/2
    df['Delta_p']     = (df['p_max']     -  df['p_min']    )/2
    df['Uncert']      = np.sqrt(df['Stat']*df['Stat'] + df['Sys']*df['Sys'] )
    df['x_F']         = 0.06451612903*df['p']*np.cos(0.001*df['theta'])  # 0.06451612903 is for 2/sqrt(s) #0.001 is mrad --> rad
    return df


def sliceDF(df):
    df_v   = []

    return df_v



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

dFs_Plus    = df_KPlus.groupby('theta_max')
angles_Plus = df_KPlus['theta_max'].unique()

dFs_Minus    = df_KMinus.groupby('theta_max')
angles_Minus = df_KMinus['theta_max'].unique()

dFs_Zeros    = df_KZeros.groupby('theta_max')
angles_Zeros = df_KZeros['theta_max'].unique()

print(angles_Plus)
print(angles_Minus)
print(angles_Zeros)


fig, ax = plt.subplots(2,math.ceil(len(df_KZeros['theta_min'].unique())/2), figsize=(16, 8))
for count, a in enumerate(angles_Minus):
    df_plus  = dFs_Plus .get_group(a)
    df_minus = dFs_Minus.get_group(a)
    if a > 20:
        df_zeros = dFs_Zeros.get_group(a)
    if count < 4:
        #ax[0,count].errorbar(df_plus['p'] ,df_plus['dKdThetadP'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert'] , label="K Plus" ,marker="o", markersize=10,ls='none')
        ax[0,count].errorbar(df_minus['p'],df_minus['dKdThetadP'],xerr=df_minus['Delta_p'], yerr=df_minus['Uncert'], label="K Minus",marker="o", markersize=10,ls='none')
        #if a > 20:
        #    ax[0,count].errorbar(df_zeros['p'],df_zeros['dKdThetadP'],xerr=df_zeros['Delta_p'], yerr=df_zeros['Uncert'], label="K Zeros",marker="o", markersize=10,ls='none')
        ax[0,count].legend()
        ax[0,count].set(xlabel='Momentum', ylabel='Differential Yield')    
    else:
        #ax[1,count-4].errorbar(df_plus['p'] ,df_plus['dKdThetadP'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert'] , label="K Plus"  ,marker="o", markersize=10,ls='none')
        ax[1,count-4].errorbar(df_minus['p'],df_minus['dKdThetadP'],xerr=df_minus['Delta_p'], yerr=df_minus['Uncert'], label="K Minus" ,marker="o", markersize=10,ls='none')
        #if a > 20:
        #    ax[1,count-4].errorbar(df_zeros['p'],df_zeros['dKdThetadP'],xerr=df_zeros['Delta_p'], yerr=df_zeros['Uncert'], label="K Zeros" ,marker="o", markersize=10,ls='none')
        ax[1,count-4].legend()
        ax[1,count-4].set(xlabel='Momentum', ylabel='Differential Yield')    
        
plt.show()

'''
for count, data in enumerate(dFs):
    print(count, data)
    print()



#fig, (ax1,ax) = plt.subplots(1,2, figsize=(10, 6), gridspec_kw={'width_ratios': [1, 3]})

#ax.scatter(x = df_KPlus.index , y = df_KPlus['dKdThetadP']  , label="KPlus"      )
#ax.scatter(x = df_KZeros['x_F'], y = df_KZeros['dKdThetadP'] , label="KZero"     )
#ax.set(xlabel='x_F', ylabel='Differential Yield')
#ax.scatter(x = df_KZeros.index, y = df_KZeros['dKdThetadP'] , label="KZeros"     )
for count, data in enumerate(dFs):
    print(type(data))
    #df_f = pd.DataFrame(data)

#ax.set(xlabel='FeynmanX', ylabel='Differential Yield')



'''

