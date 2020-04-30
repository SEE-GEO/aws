import xarray
import numpy as np
from arts_output import aws
import math
import scipy.interpolate as interpolate
from scipy.stats import gaussian_kde

def get_BT(files):
    print (len(files))
    if len(files) == 1:
        B = aws(files[0])    
        BT = B.y_aws
        return BT
    else:
        B = aws(files[0])    
        BT = B.y_aws
        n = 0
        for fileName in files[1:]:
            B = aws(fileName)
            BT_alsky = B.y_aws
            print(BT_alsky.shape)
            n += BT_alsky.shape[0]
            BT = xarray.concat([BT, BT_alsky], dim = 'cases')
        print(n)    
        return BT


def calculate_polarisations(BT,  no_of_channels):
    """
    calculates the horizontal and vertical polarisations from first two elements of stokes vector
    arguments : BT
    theta_ind :
    theta :
    returns H, V
    """
    cases = BT.shape[0]
    channels = np.arange(0, no_of_channels, 1)
    nchannels = len(channels)
    atm_views = [135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0, 170.0, 175.0, 180.0] 
    nviews = len(atm_views)
    polarisation = 2
    TB = xarray.DataArray(np.zeros([cases, nviews, nchannels, polarisation]),
                     dims=('cases', 'atm_views', 'channels', 'polarisation'),
                    coords={'cases': np.arange(0, cases, 1), 
                            'atm_views' : atm_views,
                            'channels' : channels,
                            'polarisation' : ['H', 'V']})

    for itheta, theta in enumerate(atm_views): 
        for ic in range(no_of_channels):
            theta = math.radians(180.0 - theta)
            I = BT[:, itheta, ic, 0]
            Q = BT[:, itheta, ic, 1]
            I = I.where((I < 1e36) & (Q < 1e36), drop = True)
            Q = Q.where((I < 1e36) & (Q < 1e36), drop = True)
            I_v = I + Q
            I_h = I - Q

            TB[:, itheta, ic, 0] = I_v * (np.sin(theta))**2 + I_h * (np.cos(theta))**2
            TB[:, itheta, ic, 1] = I_h * (np.sin(theta))**2 + I_v * (np.cos(theta))**2
    return TB

def interpolate_spline(TB, channel, channel_fine):
    """
    spline interpolation of the brightness temperature between the monochromatic frequencies from ARTS
    input:
        TB = brightness tempertaure (H/V polarisation) for the channels given as variable 'channels'
        channel = the channel name under consideration
        channel_fine = fine frequency grid
    returns :
        TB_fine = interpolated TB
    """

    TB_fine = []

    for i in range(TB.shape[0]):
        tck = interpolate.splrep(channel, TB[i, :], s=0)
        TB_fine.append(interpolate.splev(channel_fine, tck, der=0, ext = 0))
    TB_fine = np.array(TB_fine)


    return TB_fine

def get_channel_BT(TB_fine, channel_fine, aws_channels, bandwidths):
    
    C = []
    for aws_channel, bandwidth in zip(aws_channels, bandwidths):
        index = np.argwhere((channel_fine >= aws_channel - bandwidth/2.0) & (channel_fine <= aws_channel + bandwidth/2.0)) 
        C.append(np.mean(TB_fine[:, index], axis = 1))   
    
    return np.squeeze(np.array(C))

  
