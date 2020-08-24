#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:50:28 2020

@author: inderpreet
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import glob
from polarisation import calculate_polarisation
from read_ARTS_output import read_all_files
import xarray
from add_gaussian_noise import add_gaussian_noise
from read_clear_allsky_pairs import read_clear_allsky_pairs, read_clear_allsky_pairs_MWI

theta = 135.2

def calculate_histogram(TB, bins, channels):
        hist_arts = []
        for ic in range(channels):
            H = np.histogram(TB[:, ic], bins, density = True)
            hist_arts.append(H[0])   

    
        return hist_arts
#%%
def ICI_channel_TB(TB, nchannels):
    """
    

    Parameters
    ----------
    TB : TYPE
        DESCRIPTION.
    nchannels : TYPE
        DESCRIPTION.

    Returns
    -------
    TB_ICI : TYPE
        DESCRIPTION.

    """
    n = int(nchannels/2)
    TB_ICI = TB.copy(deep = True, data= None)[:, :,  0:n, :]

    for ic in range(n):
        print ('total_channels', ic, nchannels-ic-1)
        ic1 = ic
        ic2 = nchannels-ic-1
        TB_ICI[:, :, ic, :]= (TB[:, :, ic1, :] + TB[:, :,  ic2, :])/2
    return TB_ICI

#%% 


#%%  concatenate all ARTS simulations together         
f_grid = np.concatenate([183.31 + np.array([-7.0, -3.4, -2.0, 2.0, 3.4, 7.0]),
                                243.20 + np.array([-2.5, 2.5]),
                                325.15 + np.array([-9.5, -3.5, -1.5, 1.5, 3.5, 9.5]),
                                448.00 + np.array([-7.2, -3.0, -1.4, 1.4, 3.0, 7.2]),
                                664.00 + np.array([-4.2, 4.2])])

f_grid_mwi = np.concatenate([183.31 + np.array([-7.0, -3.4, -2.0, 2.0, 3.4, 7.0]),
                                243.20 + np.array([-2.5, 2.5]),
                                325.15 + np.array([-9.5, -3.5, -1.5, 1.5, 3.5, 9.5]),
                                448.00 + np.array([-7.2, -3.0, -1.4, 1.4, 3.0, 7.2]),
                                664.00 + np.array([-4.2, 4.2]),
                                183.31 + np.array([-6.1, -4.9, 4.9, 6.1])]) # added two MWI channels

nchannels = len(f_grid)
nedt  = np.array([0.8, 0.8, 0.8, #183Ghz
                  0.7, 0.7,      #243Ghz
                  1.2, 1.3, 1.5, #325Ghz
                  1.4, 1.6, 2.0, #448Ghz
                  1.6, 1.6])      #664Ghz
#                  1.2, 1.2])     #183Ghz, MWI



files = glob.glob(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/ICI_m60_p60/c_of_*clearsky.nc'))
#files = glob.glob(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/ICI_m60_p60/c_of_??.nc'))

#TB = read_all_files(files)

#TB_cs, TB_as  = read_clear_allsky_pairs_MWI(files)
TB_cs, TB_as  = read_clear_allsky_pairs(files)
TB_cs  = calculate_polarisation(TB_cs, nchannels, theta)
TB_as  = calculate_polarisation(TB_as, nchannels, theta)

TB = xarray.concat([TB_cs, TB_as], dim = 'sky' )

#%% extract indicies of all ICI channels

index_183 = np.where(f_grid < 200)[0]
index_243 = np.where((f_grid > 200) & (f_grid < 300))[0]
index_325 = np.where((f_grid > 300) & (f_grid < 350))[0]
index_448 = np.where((f_grid > 400) & (f_grid < 500))[0]
index_664 = np.where((f_grid > 600) & (f_grid < 700))[0]

#%% Form ICI channel TBs, last index of TB_XXX is [H, V]

TB_183 = ICI_channel_TB(TB[:, :, index_183, :], len(index_183[:6]))
TB_243 = ICI_channel_TB(TB[:, :, index_243, :], len(index_243))
TB_325 = ICI_channel_TB(TB[:, :, index_325, :], len(index_325))
TB_448 = ICI_channel_TB(TB[:, :, index_448, :], len(index_448))
TB_664 = ICI_channel_TB(TB[:, :, index_664, :], len(index_664))
#TB_183_MWI = ICI_channel_TB(TB[:, :, index_183, :], len(index_183[6:]))

#%%
TB_ICI = xarray.concat([TB_183[:, :, :, 1],
#                        TB_183_MWI[:, :, :, 1],
                        TB_243[:, :, :, 1],
                        TB_243[:, :, :, 0],
                        TB_325[:, :, :, 1],
                        TB_448[:, :, :, 1],
                        TB_664[:, :, :, 1],
                        TB_664[:, :, :, 0]], dim = 'channels')  
TB_ICI.name = 'TB'
#TB_ICI["channels"] = ['I1V', 'I2V', 'I3V', 'MWI-15', 'MWI-16', 'I4V', 'I4H', 'I5V', 'I6V', 'I7V', 
#                      'I8V', 'I9V', 'I10V', 'I11V', 'I11H']
TB_ICI["channels"] = ['I1V', 'I2V', 'I3V', 'I4V', 'I4H', 'I5V', 'I6V', 'I7V', 
                      'I8V', 'I9V', 'I10V', 'I11V', 'I11H']
TB_ICI["sky"] = ["clear", "all"]

#TB_ICI.to_netcdf('TB_ICI.nc', 'w')

#%% save 75% data as training data and rest as test data
itrain = int(TB_ICI.shape[1] * 0.85)

TB_ICI[:, :itrain, :].to_netcdf('TB_ICI_train.nc', 'w')
TB_ICI[:, itrain:, :].to_netcdf('TB_ICI_test.nc', 'w')

#%% add noise

TB_ICI_noise = TB_ICI.copy()
TB_ICI_noise[0, :, :] = add_gaussian_noise(TB_ICI[0, :, :], nedt)
TB_ICI_noise[1, :, :] = add_gaussian_noise(TB_ICI[1, :, :], nedt)



#TB_ICI.to_netcdf('TB_ICI_noise.nc', 'w')

#%%plot the PDFs of ARTS simulations to test

bins = np.arange(180, 300, 0.5)


for i in range(13):
    
    hist = np.histogram(TB_ICI[1, :, i], bins, nchannels)
    fig, ax = plt.subplots(1, 1, figsize=(7, 7))

    ax.plot( bins[:-1], hist[0])
    ax.set_yscale('log')
    ax.set_xlabel('Brightness Temp (K)', fontsize = 16)  
    ax.set_ylabel('PDF(K$^{-1}$)', fontsize = 16) 
    ax.set_title(str(f_grid[i]) + 'GHz')


y = xarray.open_dataset(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60.nc'))
TB0 = y.TB
nchannels = y.channels.size
channels_id = y.channels.values
TB

hist_atms = np.histogram(TB0[7, 1, :], bins, density = True)
hist_ici = np.histogram(TB_ICI[1, :, 7], bins, density = True)

fig, ax = plt.subplots(1, 1, figsize = (7,7))
ax.plot(bins[:-1], hist_atms[0])
ax.plot(bins[:-1], hist_ici[0])
#ax.plot(bins[:-1], hist[3])
ax.set_yscale('log')
ax.set_xlabel('Brightness Temp (K)', fontsize = 16)  
ax.set_ylabel('PDF(K$^{-1}$)', fontsize = 16) 
#%%