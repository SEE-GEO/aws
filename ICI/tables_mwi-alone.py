#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 21:57:41 2020

@author: inderpreet

Calculate statistics for point estimates from QRNN-mwi
"""


import matplotlib.pyplot as plt
import numpy as np
import stats as S
from ici_mwi_alone import iciData
plt.rcParams.update({'font.size': 26})
from typhon.retrieval.qrnn import set_backend, QRNN
set_backend("pytorch")
import stats
from tabulate import tabulate
#%%
def read_qrnn(file, inChannels, target):

    data = iciData(test_file, 
                   inChannels, target, 
                   batch_size = batchSize)  



# read QRNN    
#    file = 'qrnn_ici_%s_%s_%s_single.nc'%(depth, width, target)
#    print (file)
    qrnn = QRNN.load(file)
    y_pre, y_prior, y0, y, y_pos_mean = S.predict(data, qrnn, add_noise = True)
    
    return y_pre, y_prior, y0, y, y_pos_mean
#%%
def correction(y_pre, y_prior, i183):    
    bins = np.arange(-75, 10, 5)
    im = np.abs(y_pre[:, 3] - y_prior[:, i183]) >=  20
    
    cloud = y_prior[im, i183] - y0[im]
    corr = y_prior[im, i183] - y_pre[im, 3]   
    
    hist= np.histogram(cloud, bins, density = True)
    hist1 = np.histogram(corr, bins, density = True)
    
    return hist[0], hist1[0], bins

if __name__ == "__main__":

    #%% input parameters
    depth     = 4
    width     = 128
    quantiles = np.array([0.002, 0.03, 0.16, 0.5, 0.84, 0.97, 0.998])
    batchSize = 128
    
    targets = [ 'I1V',  'MWI-15', 'MWI-16', 'I2V', 'I3V',]
    #targets = [ 'I1V']
    test_file = "TB_ICI_mwi_test.nc"
    
    iq = np.argwhere(quantiles == 0.5)[0,0]
    
    
    color = ['k', 'b', 'r', 'g','c' ]
    
    #%%
    fig, ax = plt.subplots(1,1)
    for i,target in enumerate(targets):
        inChannels_single = np.array(['I1V', 'I2V', 'I3V', 'MWI-15', 'MWI-16'])
        file_single = 'qrnn_ici_%s_%s_%s_mwi-alone.nc'%(depth, width, target)
        print (file_single)
        i183, = np.argwhere(inChannels_single == target)[0]
        print (i183)
        y_pre, y_prior, y0, y, y_pos_mean = read_qrnn(file_single, inChannels_single, target )
    #    im = np.abs(y_pre[:, 3] - y_prior[:, i183]) <= 7.5
        im = np.abs(y_prior[:, i183]- y0) <= 10.0
        print ((1 - np.sum(im)/im.size)* 100)
        
        
        bia      = stats.calculate_bias(y_prior, y0, y, y_pre[:, 3], im, i183)
        std      = stats.calculate_std(y_prior, y0, y, y_pre[:, 3], im, i183)
        ske      = stats.calculate_skew(y_prior, y0, y, y_pre[:, 3], im, i183)
        mae      = stats.calculate_mae(y_prior, y0, y, y_pre[:, 3], im, i183)
        
        
    #%%
        bia = list(bia )
        mae = list(mae )
        ske = list(ske )
        std = list(std )
    #%%    
        sets = []
        for j in [0, 1, 4, 2, 3]:
            
            l = [bia[j], mae[j], std[j], ske[j]]  
            sets.append(l)
        sets_names = ['bias', 'mae', 'std', "skewness"]#, 'corrected(1sigma)', 'sreerekha et al', 'filtered(1sigma)']
    
    
    
        table  = [[sets_names[ii], sets[0][ii], \
                                   sets[1][ii],
                                   sets[2][ii],
                                   sets[3][ii],
                                   sets[4][ii],
    
               ] for ii in range(4)]
    
        print(tabulate(table
                 ,  tablefmt="latex", floatfmt=".2f"))
    #%%
    
        hist, hist1, bins = correction(y_pre, y_prior, i183)
        ax.plot(bins[:-1],hist, '--', color = color[i], )
        ax.plot(bins[:-1],hist1, color = color[i])
    ax.legend(["cloud", "corr"])  
    ax.set_yscale('log')  
    #%%
    
    #ax.set_yscale('log')
    fig, ax = plt.subplots(1, 1)
    ax.scatter(y_prior[:, i183] - y0, y_pre[:, iq] - y0)
