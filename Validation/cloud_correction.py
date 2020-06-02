import numpy as np
import xarray
import matplotlib.pyplot as plt
from tqdm import trange, tqdm
plt.rcParams.update({'font.size': 13})

def get_index(c, channel_id):
    index = np.argwhere(channel_id == c)[0,0]
    return index

def get_clearsky_fit(ic1, ic2, TB, cls, channel):
    x = TB[ic1, cls, :]
    y = TB[ic2, cls, :]
    coef = np.polyfit(x,y,1)
    clearskyfit = np.poly1d(coef)

    plt.plot(x,y, 'y.', x, clearskyfit(x), 'k')
    plt.ylabel('%s_clearsky'%channel[ic1])
    plt.xlabel('%s_clearsky'%channel[ic2])

