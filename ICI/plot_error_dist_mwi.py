#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 21:35:37 2020

@author: inderpreet

this code plots the PDF of the predictions and errors of best estimate (median)
MWI channels predicted using QRNN-mwi
"""


import matplotlib.pyplot as plt
import numpy as np
import stats as S
from ici_mwi_alone import iciData
plt.rcParams.update({'font.size': 32})
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from typhon.retrieval.qrnn import set_backend, QRNN
set_backend("pytorch")

#%% input parameters
depth     = 4
width     = 128
quantiles = np.array([0.002, 0.03, 0.16, 0.5, 0.84, 0.97, 0.998])
batchSize = 128

targets = [ 'I1V', 'MWI-15', 'MWI-16', 'I2V', 'I3V',]

targets_mwi = ['MWI-14', 'MWI-15', 'MWI-16', 'MWI-17', 'MWI-18'] 
test_file = "TB_ICI_mwi_test.nc"
output_file = 'Figures/error_distribution_MWI-alone.pdf'

binstep = 0.5
bins = np.arange(-20, 15, binstep)
iq = np.argwhere(quantiles == 0.5)[0,0]


#%% Plot error of best estimate for all ICI channels

fig, ax = plt.subplots(1, 5, figsize = [50, 10])
plt.subplots_adjust(wspace = 0.001)
for i,target in enumerate(targets):
    inChannels_single = np.array(['I1V', 'I2V', 'I3V', 'MWI-15', 'MWI-16'])
    file_single = 'qrnn_ici_%s_%s_%s_mwi-alone.nc'%(depth, width, target)
    data = iciData(test_file, 
                   inChannels_single, target, 
                   batch_size = batchSize)  

    i183, = np.argwhere(inChannels_single == target)[0]

# read QRNN    
    file_single = 'qrnn_ici_%s_%s_%s_mwi-alone.nc'%(depth, width, target)
    print (file_single)
    qrnn = QRNN.load(file_single)
    y_pre, y_prior, y0, y, y_pos_mean = S.predict(data, qrnn, add_noise = True)
    im = np.abs(y_pre[:, iq] - y_prior[:, i183]) <= 7.5
#    im = np.abs(y_prior[:, i183] - y0) > 33.5
    hist_noise, hist_pre, hist_prior, hist_pos_mean, hist_pos_mean_5, hist_filter  = \
        S.calculate_all_histogram(y, y0, y_pre, y_prior, iq, bins, im, i183)
                                
                                
    center = (bins[:-1] + bins[1:]) / 2

    ax[i].plot(center, hist_noise[0], 'k', linewidth = 2.5)
    ax[i].plot(center, hist_prior[0], 'g', linewidth = 2.5)
    ax[i].plot(center, hist_pre[0],'b', linewidth = 2.5)

    ax[i].plot(center, hist_pos_mean_5[0], 'y', linewidth = 2.5)
    ax[i].plot(center, hist_filter[0], 'r', linewidth = 2.5)
    ax[i].set_yscale('log')
#    ax[i].set_yticklabels([])
#    ax[i].set_xticklabels([]) 
    ax[i].xaxis.set_minor_locator(MultipleLocator(1))
    ax[i].yaxis.set_minor_locator(MultipleLocator(5))
    ax[i].grid(which = 'both', alpha = 0.2)
    ax[i].set_title('Channel:%s'%targets_mwi[i], fontsize = 28)

#    ax[i].set(ylim = [0, 1])
    
ax[0].set_ylabel('Occurence frequency [#/K]')
ax[1].set_xlabel('Deviation to noise free clear-sky [K]')
ax[1].set_yticklabels([])
ax[2].set_yticklabels([])
                            
(ax[2].legend(["Noise", "Uncorrected", "Predicted (all)", "Predicted (5K)", \
               "Filtered(5K)"],
            prop={'size': 32}, frameon = False, bbox_to_anchor=(0.55, -0.12),ncol=3))                                
                                
                                
fig.savefig(output_file, bbox_inches = 'tight')                              
                                