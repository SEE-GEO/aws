import numpy as np
import xarray
import os

T_rec = np.array([390., 650., 650.,650., 650., 650., 650., 1000., 1200., 1200., 1200.])
bandwidth_89 = np.array([4000]) * 1e6
bandwidth_165 = np.array([2800]) * 1e6
bandwidth_183 = np.array([2000, 2000, 1000, 1000, 500])*1e6
bandwidth_229 = np.array([2000])*1e6
bandwidth_325 = np.array([3000, 2500, 1200])* 1e6
delta_f = np.concatenate([bandwidth_89, bandwidth_165, bandwidth_183, bandwidth_229, bandwidth_325])

c = 1.2
delta_t = 0.003

nchannels = 11

y = xarray.open_dataset(os.path.expanduser('~/Projects/git/aws/Validation/TB_AWS_m60_p60.nc'))
TB_AWS = y.TB
cases = TB_AWS.shape[2]
print (cases)
TB_n = np.zeros(TB_AWS.shape)
sigma_noise = np.zeros(TB_AWS.shape)
for ic in range(nchannels):
    for i in range(2):
            T_a = TB_AWS[ic, i, :]
            sigma = c * (T_rec[ic] + T_a)/np.sqrt(delta_f[ic] * delta_t)
            noise = np.random.normal(0, 1, cases)* sigma
            TB_n[ic, i, :] = T_a + noise
print(sigma_noise.shape)
channel_id = np.array(['C21','C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C4X', 'C41', 'C42', 'C43'])
cases = np.arange(0, TB_n.shape[2], 1)
print (cases)
sky = ['clearsky', 'allsky']
TB_AWS_noise = xarray.DataArray(TB_n, coords = [ channel_id, sky, cases], dims = [ 'channels', 'sky','cases'], name = 'TB_noise')
TB_AWS_noise.to_netcdf('TB_AWS_m60_p60_noise.nc', 'w')

