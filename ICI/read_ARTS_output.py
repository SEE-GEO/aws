#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 12:20:00 2020

@author: inderpreet
"""

import xarray

def read_all_files(files):
    """
    function to concatenate the ARTS output of multiple files together

    Parameters
    ----------
    files : filename from ARTS output

    Returns
    -------
    TB : an xarray containing TB from all files in "files"

    """
    
    first_iteration = True
    for file in files:

        y = xarray.open_dataset(file)
        y_ici = y.y_ici
        if first_iteration:  
# initialise the xarray DataArray            
            y_ici_all = y_ici

            first_iteration = False
        else:
            y_ici_all = xarray.concat([y_ici_all, y_ici], dim = 'cases')
            
    return y_ici_all
