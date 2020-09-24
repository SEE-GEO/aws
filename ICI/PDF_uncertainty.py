#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:54:58 2020

@author: inderpreet

plot error distributions in uncertainty bins
"""

import matplotlib.pyplot as plt
import numpy as np
import netCDF4
import stats as S
from ici import iciData
plt.rcParams.update({'font.size': 32})
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

from typhon.retrieval.qrnn import set_backend, QRNN
set_backend("pytorch")

#%%
def PDF_uncertainty_bins(y_pre, y0, ulim):
    dtb =(y_pre[:, 3] - y0)
    uncertain = y_pre[:, 5] - y_pre[:, 1]
 #I1V
    #ulim = [3, 4] #I2V
    #ulim = [1, 1.5 ]#I3V
    
    im = uncertain < ulim[0]
    print (np.sum(im))
    bins = np.arange(-12.5, 15., 0.8)
    hist0 = np.histogram(dtb[im], bins, density = True)
    
    
    im = np.logical_and((uncertain < ulim[1]), ( uncertain >= ulim[0]) )
    hist1 = np.histogram(dtb[im], bins, density = True)
 
#    im = np.logical_and((uncertain < ulim[2]), ( uncertain >= ulim[1]) )
#    hist2 = np.histogram(dtb[im], bins, density = True)

    
    im = uncertain >=ulim[1]
    hist2 = np.histogram(dtb[im], bins, density = True)
    
    
    return hist0[0], hist1[0],  hist2[0], bins
#%%

#%% input parameters
depth     = 4
width     = 128
quantiles = np.array([0.002, 0.03, 0.16, 0.5, 0.84, 0.97, 0.998])
batchSize = 128

targets = ['I1V', 'I2V','I3V']

binstep = 0.5
bins = np.arange(-20, 15, binstep)
iq = np.argwhere(quantiles == 0.5)[0,0]
ulim = [3, 8]

#%% 

fig, ax = plt.subplots(1, 3, figsize = [30, 10])
plt.subplots_adjust(wspace = 0.001)
for i,target in enumerate(targets):
    inChannels = np.array([target, 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
    data = iciData("TB_ICI_test.nc", 
                   inChannels, target, 
                   batch_size = batchSize)  

    i183, = np.argwhere(inChannels == target)[0]

# read QRNN    
    file = 'qrnn_ici_%s_%s_%s_single.nc'%(depth, width, target)
    print (file)
    qrnn = QRNN.load(file)
    y_pre, y_prior, y0, y, y_pos_mean = S.predict(data, qrnn, add_noise = True)
    
    hist0, hist1, hist2, bins = PDF_uncertainty_bins(y_pre, y0, ulim)
    center = (bins[:-1] + bins[1:])/2
    ax[i].plot(center, hist0, 'k', linewidth = 2.5)
    ax[i].plot(center, hist1, 'r', linewidth = 2.5)
    ax[i].plot(center, hist2, 'b', linewidth = 2.5)
#    ax[i].plot(center, hist3, 'g', linewidth = 2.5)
    ax[i].xaxis.set_minor_locator(MultipleLocator(5))
    ax[i].grid(which = 'both', alpha = 0.4)
    
    ax[i].set_ylim(0, 1)
    ax[i].set_title("Channel:%s"%target, fontsize = 30)
ax[0].set_ylabel('Occurence frequency [#/K]', fontsize = 32)
ax[1].set_xlabel('Deviation to noise free clear-sky [K]', fontsize = 32)
ax[1].set_yticklabels([])
ax[2].set_yticklabels([])
ax[1].legend([  '0 - ' + str(ulim[0]) + ' K',
            str(ulim[0]) +' - ' + str(ulim[1]) + ' K',
             '> ' + str(ulim[1]) + ' K' ], title = "uncertainty bins (2$\sigma$)", prop={'size': 24}, \
             frameon = False, bbox_to_anchor=(0.85, 1.0), ncol=2)



fig.savefig('Figures/PDF_uncertainty_bins_QRNN-single.pdf')    

                           
                                