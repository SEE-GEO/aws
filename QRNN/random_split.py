#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:18:09 2020

@author: inderpreet
"""


import numpy as np
import xarray
import os
import matplotlib.pyplot as plt

def get_TB(TB, TB0, ic, cases):
    
    x_train = TB[:, :, cases[:int(0.9*ic.shape[0])]]
    x_train0 = TB0[:, :, cases[:int(0.9*ic.shape[0])]]
    
    x_test  = TB[:, :, cases[int(0.8*ic.shape[0]):]]
    x_test0 = TB0[:, :, cases[int(0.8*ic.shape[0]):]]
    
    
    x_val0 = TB0[:, :, cases[int(0.9*ic.shape[0]):]]
    x_val = TB[:, :, cases[int(0.9*ic.shape[0]):]]
    
    return x_test0, x_test


y = xarray.open_dataset(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_four.nc'))
TB0 = y.TB
cases = TB0.cases.values

y = xarray.open_dataset(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_noise_four.nc'))
TB = y.TB_noise

ic = np.arange(0, len(cases), 1)
np.random.shuffle(ic)

x_test0, x_test = get_TB(TB, TB0, ic, cases)

x_test.to_netcdf(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/testing_data_noise_four.nc'), 'w')
x_test0.to_netcdf(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/testing_data_four.nc'), 'w')


#=====================================================================================================
#Repeat same for three channel option A with same shuffled indices
#=====================================================================================================

y = xarray.open_dataset(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_three_a.nc'))
TB0 = y.TB

y = xarray.open_dataset(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_noise_three_a.nc'))
TB = y.TB_noise

x_test0, x_test = get_TB(TB, TB0, ic, cases)

x_test.to_netcdf(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/testing_data_noise_three_a.nc'), 'w')
x_test0.to_netcdf(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/testing_data_three_a.nc'), 'w')


#=====================================================================================================
#Repeat same for three channel option B with same shuffled indices
#=====================================================================================================

y = xarray.open_dataset(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_three_b.nc'))
TB0 = y.TB

y = xarray.open_dataset(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_noise_three_b.nc'))
TB = y.TB_noise

x_test0, x_test = get_TB(TB, TB0, ic, cases)

x_test.to_netcdf(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/testing_data_noise_three_b.nc'), 'w')
x_test0.to_netcdf(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/testing_data_three_b.nc'), 'w')






dtb = x_test[4, 1, :] - x_test0[4, 0, :] 

bins = np.arange(-30, 5, 0.2)
hist = np.histogram(dtb, bins, density = True)
fig, ax = plt.subplots()
ax.plot(bins[:-1], hist[0])
ax.set_yscale('log')
