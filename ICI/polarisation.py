#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 12:01:49 2020

@author: inderpreet
"""
import numpy as np
import math
import xarray

def calculate_polarisation(BT, no_of_channels, theta_deg):
    """
    

    Parameters
    ----------
    BT : input TB as stokes parameters
    no_of_channels : integer, the total number of channels 
        DESCRIPTION.
    theta_deg : viewing angle in deg    
    Returns
    -------
    TB : a xarray with both H and V polarisations

    """
    cases = BT.shape[0]
    channels = np.arange(0, no_of_channels, 1)
    nchannels = len(channels)

    theta = math.radians(180.0 - theta_deg)

    polarisation = 2
    TB = xarray.DataArray(np.zeros([cases, nchannels, polarisation]),
                     dims=('cases', 'channels', 'polarisation'),
                    coords={'cases': np.arange(0, cases, 1), 
                            'channels' : channels,
                            'polarisation' : ['H', 'V']})
    for ic in range(no_of_channels):
        I = BT[:, ic,  0]
        Q = BT[:, ic,  1]
        I = I.where((I < 1e36) & (Q < 1e36), drop = True)
        Q = Q.where((I < 1e36) & (Q < 1e36), drop = True)
        I_v = I + Q
        I_h = I - Q
    
        TB[:, ic, 0] = I_v * (np.sin(theta))**2 + I_h * (np.cos(theta))**2
        TB[:, ic, 1] = I_h * (np.sin(theta))**2 + I_v * (np.cos(theta))**2
    
    return TB