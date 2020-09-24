#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 11:18:03 2020

@author: inderpreet
"""


def ICI_channel_TB(TB, nchannels):
    """
    

    Parameters
    ----------
    TB : TYPE
        DESCRIPTION.
    nchannels : TYPE
        DESCRIPTION.

    Returns
    -------
    TB_ICI : TYPE
        DESCRIPTION.

    """
    n = int(nchannels/2)
    TB_ICI = TB.copy(deep = True, data= None)[:, :,  0:n, :]

    for ic in range(n):
        print ('total_channels', ic, nchannels-ic-1)
        ic1 = ic
        ic2 = nchannels-ic-1
        TB_ICI[:, :, ic, :]= (TB[:, :, ic1, :] + TB[:, :,  ic2, :])/2
    return TB_ICI