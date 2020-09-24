#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 22:09:27 2020

@author: inderpreet

PLot the uncertainties in randomly chosen cases
"""
import matplotlib.pyplot as plt
import numpy as np
import netCDF4

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from typhon.retrieval.qrnn import set_backend, QRNN
set_backend("pytorch")
import stats as S
from ici import iciData
from calibration import calibration
import random
plt.rcParams.update({'font.size': 26})


#%% input parameters
depth     = 4
width     = 128
quantiles = np.array([0.002, 0.03, 0.16, 0.5, 0.84, 0.97, 0.998])
batchSize = 128

target = 'I2V'


inChannels = np.array(['I1V', 'I2V', 'I3V', 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
#inChannels = np.array(['I1V', 'I2V', 'I3V', 'MWI-15', 'MWI-16', 'I5V', 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V', 'I11H'])
inChannels = np.array([target, 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
i183, = np.argwhere(inChannels == target)[0]

binstep = 0.5
bins = np.arange(-20, 15, binstep)
iq = np.argwhere(quantiles == 0.5)[0,0]

#%% Uncertainty plot
plt.rcParams.update({'font.size': 26})
inChannels = np.array([target, 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
i183, = np.argwhere(inChannels == target)[0]
data = iciData("TB_ICI_test.nc", 
               inChannels, target, 
               batch_size = batchSize)  

file = 'qrnn_ici_%s_%s_%s_single.nc'%(depth, width, target)
print (file)
qrnn = QRNN.load(file)

y_pre, y_prior, y0, y, y_pos_mean = S.predict(data, qrnn, add_noise = True)
fig, ax = plt.subplots(1, 1, figsize = [8, 8])
x = np.arange(-3, 4, 1)
ii = 0

randomList = random.sample(range(0, 24000), 1500)
for i in randomList:
    ii +=1
#for i in ind:
    y1 = y_pre[i,  :] - y_pre[i, 3]
    
    ax.plot(x, y1,'b', alpha = 0.3)

ax.xaxis.set_minor_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(5))
ax.grid(which = 'both', alpha = 0.4)

ax.set_xlabel("Quantiles")
ax.set_ylabel("Prediction uncertainty [K]")
ax.set_xticks(x)
ax.set_xticklabels((r'$3\sigma$', r'$2\sigma$', r'$1\sigma$', 0,r'$1\sigma$', r'$2\sigma$', r'$3\sigma$'), va='center')


q_prior = np.quantile(y_prior, quantiles, axis = 0)
#ax.plot(x, q_prior - q_prior[3])

q0 = np.quantile(y0, quantiles, axis = 0)
#ax.plot(x, q0 - q0[3])

y_normal = np.random.normal(270, 0.60, 24000)
q_normal = np.quantile(y_normal, quantiles , axis = 0)
ax.plot(x, q_normal - q_normal[3], 'r', linewidth = 3)
ax.tick_params(axis='x', which='major', pad=10)

#ax2 = ax.twinx()
#ax.set_xticks(x)
#ax.set_xticklabels(quantiles)
ax.tick_params(axis='x', which='major', pad=20)

fig.savefig('Figures/prediction_uncertainty_%s.pdf'%(target), bbox_inches = 'tight')
