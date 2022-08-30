import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import time
import numpy as np
import math

def addColumns(df,switch=False):
    df['theta']       = (df['theta_min'] +  df['theta_max'])/2
    df['Delta_theta'] = (df['theta_max'] -  df['theta_min'])/2
    df['p']           = (df['p_min']     +  df['p_max']    )/2
    df['Delta_p']     = (df['p_max']     -  df['p_min']    )/2
    df['Uncert']      = np.sqrt(df['Stat']*df['Stat'] + df['Sys']*df['Sys'] )
    df['x_F']         = 0.06451612903*df['p']*np.cos(0.001*df['theta'])  # 0.06451612903 is for 2/sqrt(s) #0.001 is mrad --> rad
    df['zero']        = 0.*df['p']
    if switch:
        df['K12']          = (0.500*df['dKdThetadP_Plus'] +  0.500*df['dKdThetadP_Minus'])
        df['K34']          = (0.250*df['dKdThetadP_Plus'] +  0.750*df['dKdThetadP_Minus'])
        df['K38']          = (0.375*df['dKdThetadP_Plus'] +  0.625*df['dKdThetadP_Minus'])
        df['KPercentDiff'] = 100*np.abs(df['K34'] - df['K38'] )/df['K34']
        df['KDiff']        = np.abs(df['K34'] - df['K38'] ) 
        # Uncertainty
        df['Uncert_P']    = np.sqrt(df['Stat']      *df['Stat']       + df['Sys']      *df['Sys'      ] )
        df['Uncert_M']    = np.sqrt(df['Stat_Minus']*df['Stat_Minus'] + df['Sys_Minus']*df['Sys_Minus'] )
        df['RelUncert_M'] = df['Uncert_M']/df['dKdThetadP_Minus']
        df['RelUncert_P'] = df['Uncert_P']/df['dKdThetadP_Plus' ]
        df['Uncert34'] = np.sqrt(0.0625*df['Uncert_P']*df['Uncert_P'] + 0.5625*df['Uncert_M']*df['Uncert_M'])
        df['Uncert38'] = np.sqrt(0.140625*df['RelUncert_P']*df['RelUncert_P'] + 0.390625*df['RelUncert_M']*df['RelUncert_M'])
    return df





def sliceDF(df):
    df_v   = []

    return df_v



#Read Dataframe
df_KPlus = pd.read_csv("SingleBinChargedKaons.csv")
df_KPlus.dropna(inplace=True)


df_KZeros = pd.read_csv("SHINE31GeV_Kaon_Data_K0S.csv")
df_KZeros.dropna(inplace=True)

df_KPlus  = addColumns(df_KPlus,True)
df_KZeros = addColumns(df_KZeros)

dFs_Plus    = df_KPlus.groupby('theta_max')
angles_Plus = df_KPlus['theta_max'].unique()

dFs_Zeros    = df_KZeros.groupby('theta_max')
angles_Zeros = df_KZeros['theta_max'].unique()

print(angles_Plus)
#print(angles_Zeros)
#KPercentDiff

'''
fig, ax = plt.subplots(2,math.ceil(len(df_KZeros['theta_min'].unique())/2), figsize=(16, 8))
for count, a in enumerate(angles_Plus):
    df_plus  = dFs_Plus .get_group(a)
    if a > 20:
        df_zeros = dFs_Zeros.get_group(a)
    if count < 4:
        ax[0,count].errorbar(df_plus['p'] ,df_plus['K34'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert34'] , label="3/4" ,marker="o", markersize=10,ls='none')
        ax[0,count].errorbar(df_plus['p'] ,df_plus['K38'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert38'] , label="3/8" ,marker="o", markersize=10,ls='none')
        if a > 20:
            ax[0,count].errorbar(df_zeros['p'],df_zeros['dKdThetadP'],xerr=df_zeros['Delta_p'], yerr=df_zeros['Uncert'], label="K Zeros",marker="o", markersize=10,ls='none')
        ax[0,count].legend()
        ax[0,count].set(xlabel='Momentum', ylabel='Differential Yield')    
    else:
        ax[1,count-4].errorbar(df_plus['p'] ,df_plus['K34'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert34'] , label="3/4"  ,marker="o", markersize=10,ls='none')
        ax[1,count-4].errorbar(df_plus['p'] ,df_plus['K38'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert38'] , label="3/8"  ,marker="o", markersize=10,ls='none')
        if a > 20:
            ax[1,count-4].errorbar(df_zeros['p'],df_zeros['dKdThetadP'],xerr=df_zeros['Delta_p'], yerr=df_zeros['Uncert'], label="K Zeros" ,marker="o", markersize=10,ls='none')
        ax[1,count-4].legend()
        ax[1,count-4].set(xlabel='Momentum', ylabel='Differential Yield')    



fig, ax = plt.subplots(2,math.ceil(len(df_KZeros['theta_min'].unique())/2), figsize=(16, 8))
for count, a in enumerate(angles_Plus):
    if count < 4:
        ax[0,count].errorbar(df_plus['p'] ,df_plus['K34'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert34'] , label="3/4" ,marker="o", markersize=10,ls='none')
        ax[0,count].errorbar(df_plus['p'] ,df_plus['K38'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert38'] , label="3/8" ,marker="o", markersize=10,ls='none')

    else:
        ax[1,count-4].errorbar(df_plus['p'] ,df_plus['K34'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['Uncert34'] , label="3/4"  ,marker="o", markersize=10,ls='none')
        ax[1,count-4].legend()
        ax[1,count-4].set(xlabel='Momentum', ylabel='Differential Yield')    
'''


fig, ax = plt.subplots(2,3, figsize=(16, 8))
for count, a in enumerate(angles_Plus):
    df_plus  = dFs_Plus .get_group(a)
    df_zeros = dFs_Zeros.get_group(a)
    print(math.floor(count/3))
    ax[math.floor(count/3), count-math.floor(count/3)*3].plot(df_plus['p'] ,df_plus['K34'] , '-', label=r'p-p: $\frac{ N(K^+) + 3N(K^-)}{4}$')
    ax[math.floor(count/3), count-math.floor(count/3)*3].plot(df_plus['p'] ,df_plus['K38'] , '-', label=r'p-C: $\frac{3N(K^+) + 5N(K^-)}{8}$')
    ax[math.floor(count/3), count-math.floor(count/3)*3].plot(df_plus['p'] ,df_plus['K12'] , '-', label=r'p-p: $\frac{ N(K^+) +  N(K^-)}{2}$')
    ax[math.floor(count/3), count-math.floor(count/3)*3].fill_between(df_plus['p'], df_plus['K34'], df_plus['K12'], alpha=0.2)
    ax[math.floor(count/3), count-math.floor(count/3)*3].errorbar(df_zeros['p'],df_zeros['dKdThetadP'],xerr=df_zeros['Delta_p'], yerr=df_zeros['Uncert'], label="NA64/SHINE K0 Data",marker="o", markersize=5,ls='none')
    ax[math.floor(count/3), count-math.floor(count/3)*3].legend()
    ax[math.floor(count/3), count-math.floor(count/3)*3].set(xlabel='Momentum [GeV]', ylabel=r'$\frac{d\sigma}{dp d\theta}$ [mb (mrad GeV/c)$^{-1}$]')
    #ax[math.floor(count/3), count-math.floor(count/3)*3].set(xlabel='Momentum [GeV]', ylabel='Percentage Difference')
    
    '''
        ax[0,count].plot(df_plus['p'] ,df_plus['K34'] , '-', label="3/4")
        ax[0,count].plot(df_plus['p'] ,df_plus['K38'] , '-', label="3/8")
        ax[0,count].fill_between(df_plus['p'], df_plus['K34'], df_plus['K38'], alpha=0.2)
        ax[0,count].errorbar(df_zeros['p'],df_zeros['dKdThetadP'],xerr=df_zeros['Delta_p'], yerr=df_zeros['Uncert'], label="K Zeros",marker="o", markersize=5,ls='none')
    '''




    #ax .errorbar(df_plus['p'] ,df_plus['K34'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['zero'] , label="3/4" ,marker="x", markersize=4,ls='none')
    #ax .errorbar(df_plus['p'] ,df_plus['K38'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['zero'] , label="3/8" ,marker="x", markersize=4,ls='none')
    #ax .errorbar(df_plus['p'] ,df_plus['dKdThetadP_Plus']  ,xerr=df_plus['zero'] , yerr=df_plus['Uncert_P'] , label="K Plus" ,marker="o", markersize=4,ls='none')
    #ax .errorbar(df_plus['p'] ,df_plus['dKdThetadP_Minus'] ,xerr=df_plus['zero'] , yerr=df_plus['Uncert_M'] , label="K Minus" ,marker="o", markersize=4,ls='none')
    #ax.errorbar(df_plus['p'] ,df_plus['KDiff'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['zero'] , label="diff"  ,marker="o", markersize=10,ls='none')
    #ax.errorbar(df_plus['p'] ,df_plus['Uncert34'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['zero'] , label="Uncert_P"  ,marker="o", markersize=10,ls='none')
    #ax.errorbar(df_plus['p'] ,df_plus['Uncert38'] ,xerr=df_plus['Delta_p'] , yerr=df_plus['zero'] , label="Uncert_M"  ,marker="o", markersize=10,ls='none')


plt.tight_layout()    
plt.show()
    
