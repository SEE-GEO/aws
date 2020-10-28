#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:46:41 2020

@author: inderpreet
This code plots the calibration curves for both QRNN-single and QRNN-all
"""
import matplotlib.pyplot as plt
import numpy as np
import netCDF4
import os
import ICI.stats as stats
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from typhon.retrieval.qrnn import set_backend, QRNN
set_backend("pytorch")
import ICI.stats as S

from ICI.calibration import calibration
from read_qrnn import read_qrnn
import random
plt.rcParams.update({'font.size': 26})


#%% input parameters
depth     = 3
width     = 128
quantiles = np.array([0.002, 0.03, 0.16, 0.5, 0.84, 0.97, 0.998])
batchSize = 128

targets = [11, 12, 13, 14, 15]
test_file = os.path.expanduser("~/Dendrite/Projects/AWS-325GHz/MWHS/data/TB_MWHS_test.nc")

iq = np.argwhere(quantiles == 0.5)[0,0]

#qrnn_dir = "C89+150"
#qrnn_dir = "C150"
qrnn_dir = "C89+150"

if qrnn_dir == "C89+150":
    channels = [ 1, 10]
  
target = 14 

#%% read input data
        
print(qrnn_dir, channels)

qrnn_path = os.path.expanduser("~/Dendrite/Projects/AWS-325GHz/MWHS/qrnn_output/all_with_flag/%s/"%(qrnn_dir))

inChannels = np.concatenate([[target], channels])

print(qrnn_dir, channels, inChannels)
    
qrnn_file = os.path.join(qrnn_path, "qrnn_mwhs_%s.nc"%(target))

print (qrnn_file)
i183, = np.argwhere(inChannels == target)[0]

y_pre, y_prior, y0, y, y_pos_mean = read_qrnn(qrnn_file, test_file, inChannels, target)

# calibration plot data with correction greater than 15K

fig, ax = plt.subplots(1, 1, figsize = [8,8])   

im = np.arange(0, y0.size, 1)
a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)
    

(ax.plot(intervals[:], [ a1/len(y0[:]), a2/len(y0[:]), a3/len(y0[:]), 
                           a4/len(y0[:]), a5/len(y0[:]),
                          ], 'r.-', ms = 15, linewidth = 2.5))

im = np.where(np.abs(y_pre[:, iq] - y_prior[:, i183]) >= 5)[0]
a1, a2, a3, a4, a5, a6, intervals  = calibration(y_pre, y0, im, quantiles)     

(ax.plot(intervals[:], [ a1/len(y0[im]), a2/len(y0[im]), a3/len(y0[im]), 
                           a4/len(y0[im]), a5/len(y0[im]),
                          ], 'b.-', ms = 15, linewidth = 2.5))

ax.set_title("MWHS-2 channel %s"%str(target), fontsize = 24)

#%% set the plot parameters

x = np.arange(0,1.2,0.2)
y = x
ax.plot(x, y, 'k:', linewidth = 1.5)
ax.set(xlim = [0, 1], ylim = [0,1])
ax.set_aspect(1.0)
ax.set_xlabel("Predicted frequency")
ax.set_ylabel("Observed frequency")
ax.xaxis.set_minor_locator(MultipleLocator(0.2))
ax.grid(which = 'both', alpha = 0.2)
fig.savefig('Figures/calibration_plot_%s'%target)

(ax.legend(["All data", "correction > 10K"],
            prop={'size': 22}, frameon = False))  

fig.savefig("Figures/calibration_QRNN_MWHS_%s.pdf"%target, bbox_inches = 'tight')
#%%
fig, ax = plt.subplots(1, 1, figsize = [10, 10])
bins = np.arange(220, 300, 1)
bin_center = (bins[:-1] + bins[1:]) / 2
hist_prior = np.histogram(y_prior[:, i183], bins, density = True)              
ax.plot(bin_center, hist_prior[0], 'r', linewidth = 2.5)

hist_pre = np.histogram(y_pre[:, 3], bins, density = True)

ax.plot(bin_center, hist_pre[0], 'b', linewidth = 2.5)
                                    
hist0 = np.histogram(y0, bins, density = True)              
ax.plot(bin_center, hist0[0], 'g' ,linewidth = 2.5)
ax.set_yscale('log')
ax.set_xlabel('Brightness temperature [K]')
ax.set_ylabel('Occurence frequency [#/K]')
ax.legend(["Uncorrected", "Predicted", "Simulated"],  prop={'size': 24}) 
ax.set_title('MWHS-2 channel %s'%str(target))
ax.xaxis.set_minor_locator(MultipleLocator(2))

ax.grid(which = 'both', alpha = 0.2)
fig.savefig('Figures/QRNN_output_mwhs.pdf', bbox_inches = 'tight')
