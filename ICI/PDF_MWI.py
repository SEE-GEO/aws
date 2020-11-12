#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:50:28 2020

@author: inderpreet

Combines data from all ARTS simulations and writes the training and testing datasets
for MWI channels
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
#from get_IWP import get_IWP
from ICI_channel_TB import ICI_channel_TB
import random

theta = 135.2
#%%
def calculate_histogram(TB, bins, channels):
        hist_arts = []
        for ic in range(channels):
            H = np.histogram(TB[:, ic], bins, density = True)
            hist_arts.append(H[0])   

    
        return hist_arts

#%%  concatenate all ARTS simulations together         
f_grid = np.concatenate([183.31 + np.array([-7.0, -3.4, -2.0, 2.0, 3.4, 7.0]),
                                243.20 + np.array([-2.5, 2.5]),
                                325.15 + np.array([-9.5, -3.5, -1.5, 1.5, 3.5, 9.5]),
                                448.00 + np.array([-7.2, -3.0, -1.4, 1.4, 3.0, 7.2]),
                                664.00 + np.array([-4.2, 4.2]),
                                183.31 + np.array([-6.1, -4.9, 4.9, 6.1])]) # added two MWI channels

nchannels = len(f_grid)
nedt  = np.array([0.8, 0.8, 0.8, #183Ghz
                  1.2, 1.2,      #183Ghz, MWI
                  0.7, 0.7,      #243Ghz
                  1.2, 1.3, 1.5, #325Ghz
                  1.4, 1.6, 2.0, #448Ghz
                  1.6, 1.6,])    #664Ghz    


files = glob.glob(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/ICI_m60_p60/c_of_*clearsky.nc'))

#%%
TB_cs, TB_as  = read_clear_allsky_pairs_MWI(files)
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
TB_183_MWI = ICI_channel_TB(TB[:, :, index_183, :], len(index_183[6:]))

#%%
TB_ICI = xarray.concat([TB_183[:, :, :, 1],
                        TB_183_MWI[:, :, :, 1],
                        TB_243[:, :, :, 1],
                        TB_243[:, :, :, 0],
                        TB_325[:, :, :, 1],
                        TB_448[:, :, :, 1],
                        TB_664[:, :, :, 1],
                        TB_664[:, :, :, 0]], dim = 'channels')  
TB_ICI.name = 'TB'
TB_ICI["channels"] = ['I1V', 'I2V', 'I3V', 'MWI-15', 'MWI-16', 'I4V', 'I4H', 'I5V', 'I6V', 'I7V', 
                     'I8V', 'I9V', 'I10V', 'I11V', 'I11H']
#TB_ICI["channels"] = ['I1V', 'I2V', 'I3V', 'I4V', 'I4H', 'I5V', 'I6V', 'I7V', 
#                      'I8V', 'I9V', 'I10V', 'I11V', 'I11H']
TB_ICI["sky"] = ["clear", "all"]

#TB_ICI.to_netcdf('TB_ICI.nc', 'w')

#%% save 75% data as training data and rest as test data
randomList = random.sample(range(0, 218856), 218856)

TB_ICI[:, randomList[:175000], :].to_netcdf('TB_ICI_mwi_train.nc', 'w')
TB_ICI[:, randomList[175000:], :].to_netcdf('TB_ICI_mwi_test.nc', 'w')
