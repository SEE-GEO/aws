"""Module for processing ATMS files
"""
import os
import numpy as np
import netCDF4 as nc
import pandas as pd
from parse import parse
import datetime as dt
import pickle

class ATMS:
    
	def __init__(self, filePath, fileName):
        
		totalPath = os.path.join(filePath, fileName)

#	self.fileName = 'SNDR.SNPP.ATMS.20150907T0000.m06.g001.L1B.std.v02_05.G.180910082449.nc'
		self.dataset = nc.Dataset(totalPath, 'r+')

		self.lat = self.dataset.variables["lat"][:]
		self.lon = self.dataset.variables["lon"][:]
		self.surf_alt = self.dataset.variables["surf_alt"][:]
		self.antenna_temp = self.dataset.variables["antenna_temp"][:]
		self.view_angle = self.dataset.variables["sat_zen"][:]

	def doMask(self, latlims, height):
		""" Arguments: latlims (tuple)- provide the min and max latitude limits
#                       height- max height above which no values are to be considered
#            returns: mask - np.array (boolean), mask based on latitude and height limits             
		 """
		mask_lat = (self.lat >= latlims[0]) & (self.lat <= latlims[1])
		mask_height = (self.surf_alt < height) & (self.surf_alt >=0.0)  	
		mask = np.logical_and(mask_lat, mask_height)
		return mask
        
	def extractBT(self, mask):
		""" arguments: mask
		"""
		BT_17 = self.antenna_temp[:,:,16][mask]
		BT_18 = self.antenna_temp[:,:,17][mask]
		BT_19 = self.antenna_temp[:,:,18][mask]
		BT_20 = self.antenna_temp[:,:,19][mask]
		BT_21 = self.antenna_temp[:,:,20][mask]
		BT_22 = self.antenna_temp[:,:,21][mask]
		lat_subset = self.lat[mask]
		lon_subset = self.lon[mask]
		alt_subset = self.surf_alt[mask]
		vza_subset = self.view_angle[mask]
		lat = pd.DataFrame(lat_subset, columns =  ['lat'])
		lon = pd.DataFrame(lon_subset, columns =  ['lon'])
		alt = pd.DataFrame(alt_subset, columns =  ['alt'])
		vza = pd.DataFrame(vza_subset, columns =  ['vza'])
		BT17 = pd.DataFrame(BT_17, columns =  ['BT17'])
		BT18 = pd.DataFrame(BT_18, columns =  ['BT18'])
		BT19 = pd.DataFrame(BT_19, columns =  ['BT19'])
		BT20 = pd.DataFrame(BT_20, columns =  ['BT20'])
		BT21 = pd.DataFrame(BT_21, columns =  ['BT21'])
		BT22 = pd.DataFrame(BT_22, columns =  ['BT22'])
		
		ATM_Data = pd.concat([lat, lon, alt, vza, BT17, BT18, BT19, BT20, BT21, BT22], axis = 1) 
		return ATM_Data
	 	


if __name__ == "__main__" :
	
	filePath = '/home/inderpreet/Dendrite/SatData/ATMS_GES/L1B/2015/08'
	latlims = (-30.0, 30.0)
	height = 500.0
	DF = pd.DataFrame()			        
	#fileName = 'SNDR.SNPP.ATMS.20150831T2142.m06.g218.L1B.std.v02_05.G.180909124636.nc'
	with open('allfiles.txt') as f:
		fileNames = f.read().splitlines()
	for fileName in fileNames: 
		A = ATMS(filePath, fileName)
		mask = A.doMask(latlims, height)
		if not mask.any():
			print('Data in {} lies outside the limits.'.format(fileName))
		else:
#			
			DF = DF.append( A.extractBT(mask), ignore_index = True) 	             
			
	DF.to_hdf('brightness_temp_zen.h5', key = 'DF', mode= 'w', complevel = 9)


