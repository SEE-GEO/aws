#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 21:35:37 2020

@author: inderpreet

this code plots the PDF of the predicted error and observed error (error  of best estimate (median))
ICI channels
"""


import matplotlib.pyplot as plt
import numpy as np
import stats as S
from ici import iciData
plt.rcParams.update({'font.size': 32})
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

from typhon.retrieval.qrnn import set_backend, QRNN
set_backend("pytorch")

#%%
def sample_posterior(x, nn, y0, y_pre):
    """
    estimates histogram of predicted error (random samples drawn from posterior)

    Parameters
    ----------
    x : input data for QRNN predictions
    nn : number of samples required for each case
    y0 : NFCS simulations
    y_pre : predicted median

    Returns
    -------
    hist_sample : frequency and bins of predicted errors
    """
    n = x.shape[0]
    y_pos = []
    for i in range(n):
        y_pos.append(qrnn.sample_posterior(x[i, :], nn))
    y_pos = np.array(y_pos)
    
    d = []
    for j in range(nn):
        
        d.append(y_pos[:, j] - y_pre)
    d = np.array(d).ravel()    
    hist_sample = np.histogram(d, bins, density = True)
    return hist_sample

def predict(test_data, qrnn, add_noise = False):
    """
    predict the posterior mean and median
    """
    if add_noise:
        x_noise = test_data.add_noise(test_data.x, test_data.index)
        x = (x_noise - test_data.mean)/test_data.std
        y_prior = x_noise
        y = test_data.y_noise
        
        y0 = test_data.y
    else:
        x = (test_data.x - test_data.mean)/test_data.std
        y_prior = test_data.x
        y = test_data.y
        y0 = test_data.y0


    y_pre = qrnn.predict(x.data)
    y_pos_mean = qrnn.posterior_mean(x.data)
    
    return y_pre, y_prior, y0, y, y_pos_mean, x.data

if __name__ == "__main__":
    #%% input parameters
    depth     = 4
    width     = 128
    quantiles = np.array([0.002, 0.03, 0.16, 0.5, 0.84, 0.97, 0.998])
    batchSize = 128
    
    targets = ['I1V', 'I2V','I3V']
    targets = ['I2V']
    test_file = "TB_ICI_train.nc"
    
    
    binstep = 0.5
    bins = np.arange(-20, 20, binstep)
    iq = np.argwhere(quantiles == 0.5)[0,0]
    
    #%% Plot error of best estimate for all ICI channels
    
    fig, ax = plt.subplots(1, 2, figsize = [20, 10], sharex=True)
    plt.subplots_adjust(wspace = 0.001)
    for i,target in enumerate(targets):
        inChannels = np.array([target, 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
    #    inChannels = np.array(['I1V', 'I2V','I3V', 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
        data = iciData(test_file, 
                       inChannels, target, 
                       batch_size = batchSize)  
    
        i183, = np.argwhere(inChannels == target)[0]
    
    # read QRNN    
        file = 'qrnn_ici_%s_%s_%s_single.nc'%(depth, width, target)
    #    file = 'qrnn_ici_%s_%s_%s.nc'%(depth, width, target)
        print (file)
        qrnn = QRNN.load(file)
        y_pre, y_prior, y0, y, y_pos_mean, x = predict(data, qrnn, add_noise = True)
        
        im = np.abs(y_pre[:, iq] - y_prior[:, i183]) < 5.0
        hist_noise, hist_pre, hist_prior, hist_pos_mean, hist_pos_mean_5, hist_filter  = \
            S.calculate_all_histogram(y, y0, y_pre, y_prior, iq, bins, im, i183)
                                    
        nn = 1   
        hist_sample = sample_posterior(x, nn, y0, y_pre[:,3])
        center = (bins[:-1] + bins[1:]) / 2
    
    #    ax[i].plot(center, hist_noise[0], 'k', linewidth = 2.5)
    #    ax[i].plot(center, hist_prior[0], 'g', linewidth = 2.5)
        ax[0].plot(center, hist_pre[0],'b', linewidth = 2.5)
    
    #    ax[i].plot(center, hist_pos_mean_5[0], 'y', linewidth = 2.5)
        ax[0].plot(center, hist_sample[0], 'b--', linewidth = 2.5)
    
        
    #    inChannels = np.array([target, 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
        inChannels = np.array(['I1V', 'I2V','I3V', 'I5V' , 'I6V', 'I7V', 'I8V', 'I9V', 'I10V', 'I11V'])
        data = iciData(test_file, 
                       inChannels, target, 
                       batch_size = batchSize)  
    
        i183, = np.argwhere(inChannels == target)[0]
    
    # read QRNN    
    #    file = 'qrnn_ici_%s_%s_%s_single.nc'%(depth, width, target)
        file = 'qrnn_ici_%s_%s_%s.nc'%(depth, width, target)
        print (file)
        qrnn = QRNN.load(file)
        y_pre, y_prior, y0, y, y_pos_mean, x = predict(data, qrnn, add_noise = True)
        
        
        im = np.abs(y_pre[:, iq] - y_prior[:, i183]) < 5.0
        hist_noise, hist_pre, hist_prior, hist_pos_mean, hist_pos_mean_5, hist_filter  = \
            S.calculate_all_histogram(y, y0, y_pre, y_prior, iq, bins, im, i183)
                                    
        nn = 1   
        hist_sample = sample_posterior(x, nn, y0, y_pre[:,3])
                                    
        center = (bins[:-1] + bins[1:]) / 2
    
    #    ax[i].plot(center, hist_noise[0], 'k', linewidth = 2.5)
    #    ax[i].plot(center, hist_prior[0], 'g', linewidth = 2.5)
        ax[1].plot(center, hist_pre[0],'b', linewidth = 2.5)
    
    #    ax[i].plot(center, hist_pos_mean_5[0], 'y', linewidth = 2.5)
        ax[1].plot(center, hist_sample[0], 'b--', linewidth = 2.5)
    #    ax[i].set_yticklabels([])
    #    ax[i].set_xticklabels([]) 
    for i in range(2):
        ax[i].xaxis.set_minor_locator(MultipleLocator(5))
        ax[i].yaxis.set_minor_locator(MultipleLocator(5))
        ax[i].grid(which = 'both', alpha = 0.2)
    
        ax[i].set_yscale('log')
    
    #    ax[i].set(ylim = [0, 1])
    #%%    
    ax[0].set_title('QRNN-single', fontsize = 28)
    ax[1].set_title('QRNN-all', fontsize = 28)
    ax[0].set_ylabel('Occurence frequency [#/K]')
    fig.text(0.5, 0.04, 'Deviation to NFCS [K]', ha='center')
    ax[1].set_yticklabels([])
    ax[1].set_yticklabels([])
                                
    ax[0].legend([ "Observed", "Predicted", ],
                prop={'size': 28}, frameon = False, )                                
    ax[1].legend([ "Observed", "Predicted", ],
                prop={'size': 28}, frameon = False, )                                      
                                    
    fig.savefig('Figures/deviation_posterior_samples_%s_train-set.pdf'%(target),\
                bbox_inches = 'tight')                               
                                    