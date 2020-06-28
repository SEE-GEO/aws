#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:17:11 2020

@author: inderpreet
"""

import numpy as np
import os
from TB_aws import TB_AWS
from tabulate import tabulate
import matplotlib.pyplot as plt
from interpolate import interpolate_DoF
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

plt.rcParams.update({'font.size': 16})

channels_3 =  ['C21','C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C41', 'C42', 'C43']
channels_4 =  ['C21','C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C41', 'C42', 'C43', 'C44']
channels_4X = ['C21','C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C4X']
T_recs   = [None, 1, 2]

file_3a  = '~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60.nc'
file_3b  = '~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_three_b.nc'
file_3c  = '~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_three_c.nc'
file_3d  = '~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_three_d.nc'
file_4  = '~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_four.nc'
file_4a  = '~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60_four_a.nc'
file_4X = '~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60.nc'

#=============================================================
#options 3a, 3b, 4, 4X
files    = [file_3a, file_3c,  file_4, file_4X]
channels = [channels_3, channels_3, channels_4, channels_4X]
options = ["3a", "3c", "4", "3b"]

#=============================================================
# options 3c and 3d
#options = ["4", "4a"]
#files    = [file_4, file_4a]
#channels = [channels_4, channels_4]
#=============================================================

T_recs = [None]
#=============================================================
# set the sky condition here
all_cases = False
cloudy    = False
clear     = True
#=============================================================

DoF = np.zeros([len(options), 3])


fig, ax = plt.subplots(1, 1, figsize = [8, 8])

for i, (channel, file, option) in enumerate(zip(channels, files, options)):
#    print (channel, file, option)
    max_DoF = len(channel)
    xx = np.arange(1, max_DoF+1, 1)
    for j , T_rec in enumerate(T_recs):
        
 #       print (i, j,  T_rec)
        Y = TB_AWS(os.path.expanduser(file),
                    inChannels = channel, 
                    option     = option, 
                    T_rec      = T_rec, 
                    all_cases  = all_cases,
                    cloudy     = cloudy,
                    clear      = clear)

#        print (Y.index_183)
        
        s_epsilon = Y.add_noise(Y)
    
        U, S, V = Y.svd()
        S_l = Y.get_S_lambda(U, s_epsilon)
        
        S_y = Y.cov_mat()
        
        DoF[i,j]= len(np.where(S > S_l.diagonal())[0])

        dof = interpolate_DoF(S, S_l, xx)      

        ax.plot(xx, S/S_l.diagonal())
        DoF[i,j] = np.round(dof, decimals = 1)              
 #       DoF[i,j] = dof  
    

table  = [[options[i], DoF[i, 0], DoF[i, 1], DoF[i, 2]] for i in range(len(options))]

print(tabulate(table
         , ['T_rec = 1200 K', 'T_rev = 1800 K', 'T_rec = 2400 K'], tablefmt="latex"))

#print ('DoF 4X', DoF[3, :])
ax.legend(['three-a', 'three-b', 'four', 'AWS-4X'])
ax.set_yscale('log')
ax.axhline(y = 1, c = 'k', linestyle = '--')
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.grid(which = 'both', alpha = 0.4)
ax.set_xlabel('Eigenvalue index')    
ax.set_ylabel(r"$\mathrm{\frac{\Lambda}{S_{\Lambda}}}$", fontsize=24)
fig.savefig('DoF.png', bbox_inches='tight')
