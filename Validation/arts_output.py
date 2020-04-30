# -*- coding: utf-8 -*-
import xarray
import numpy as np

class atms():
    """
    Defining a new `class` `arts_output` to read the output simulation data from ARTS

    * The results are stored in NetCDF4 format. The siulated brightness temperatures together with the sensor position and viewing angles are stored in the variables y_atms, atms_position and atms_line_of_sight contained in the root of the file structure.

    * The data can be read conveniently using the xarray package.

    * In addition to the simulated brightness temperatures, the results contain the filename that the profile was taken from and the index of the profile in the `inputs` group of the file.

    Dimensions :
    * atms_channels: 6, atms_stokes_dim: 2, atms_views: 10
    
    Dimensions without coordinates:     
    * atms_channels, atms_stokes_dim, atms_views, cases

    Data variables:
    * atms_position       (cases, atms_views) float32 ...    
    * atms_line_of_sight  (cases, atms_views) float32 ...    
    * y_atms              (cases, atms_views, atms_channels, atms_stokes_dim) float32 

    """
    
    def __init__(self, fileName):
        
        simulation_results = xarray.open_dataset(fileName)
        simulation_results
        self.y_atms = simulation_results["y_atms"][:]
        self.atms_position = simulation_results["atms_position"][:]
        self.atms_line_of_sight = simulation_results["atms_line_of_sight"][:]
            
        self.input_data = xarray.open_dataset(fileName)    


        
class aws():
    """
    Defining a new `class` `arts_output` to read the output simulation data from ARTS

    * The results are stored in NetCDF4 format. The siulated brightness temperatures together with the sensor position and viewing angles are stored in the variables y_atms, atms_position and atms_line_of_sight contained in the root of the file structure.

    * The data can be read conveniently using the xarray package.

    * In addition to the simulated brightness temperatures, the results contain the filename that the profile was taken from and the index of the profile in the `inputs` group of the file.

    Dimensions :
    * aws_channels: 18, atms_stokes_dim: 2, atms_views: 10
    
    Dimensions without coordinates:     
    * aws_channels, aws_stokes_dim, aws_views, cases

    Data variables:
    * aws_position       (cases, atms_views) float32 ...    
    * aws_line_of_sight  (cases, atms_views) float32 ...    
    * y_aws              (cases, atms_views, atms_channels, atms_stokes_dim) float32 

    """
    
    def __init__(self, fileName):
        
        simulation_results = xarray.open_dataset(fileName)
        simulation_results
        self.y_aws = simulation_results["y_aws"][:]
        self.aws_position = simulation_results["aws_position"][:]
        self.aws_line_of_sight = simulation_results["aws_line_of_sight"][:]
            
        self.input_data = xarray.open_dataset(fileName)  

