import pylab as pl
import numpy as np
import matplotlib.pyplot as plt

from astropy.table import Table

def gold_footprint(cat, interior=True):
    isa     = (cat['RA'] >= 149.03) & (cat['RA'] <= 151.18) & (((cat['DEC'] >= 0.95) & (cat['DEC'] <= 1.95)) | ((cat['DEC'] > 2.45) & (cat['DEC'] <= 3.45)))
    isb     = (cat['RA'] >= 148.92) & (cat['RA'] <= 151.30) & (((cat['DEC'] >= 1.20) & (cat['DEC'] <= 1.70)) | ((cat['DEC'] >= 2.70) & (cat['DEC'] <= 3.20)))
    isc     = (cat['RA'] >= 149.52) & (cat['RA'] <= 150.70) & (cat['DEC'] > 1.95) & (cat['DEC'] < 2.45)

    isin    = isa | isb | isc

    if interior:
        is_int  = (np.abs(cat['RA'] - 149.145) >= 0.025) | ((np.abs(cat['DEC']-1.535) >= 0.040) & (np.abs(cat['DEC']-3.075) >= 0.125))
        is_int &= (np.abs(cat['RA'] - 150.345) >= 0.025) | ((np.abs(cat['DEC']-1.535) >= 0.040) & (np.abs(cat['DEC']-3.075) >= 0.125))
        is_int &= (np.abs(cat['RA'] - 149.755) >= 0.025) | ((np.abs(cat['DEC']-2.265) >= 0.065))
        is_int &= (np.abs(cat['RA'] - 150.200) >= 0.020) | ((np.abs(cat['DEC']-1.150) >= 0.050))

        isin = isin & is_int
    
    return isin

    
if __name__ == '__main__': 
   band   ='r'
   title  ='Clauds'
   fpath  = '/global/cscratch1/sd/mjwilson/clauds/March2021/COSMOS_v9_v210225.fits'
   
   dat    = Table.read(fpath)
   
   dat    = dat[dat['FLAG_FIELD_BINARY'][:,1] == True]   
   dat    = dat[::10]
   
   # No interior mask. 
   isin  = gold_footprint(dat, interior=False)
   
   # Interior mask applied.    
   isint = gold_footprint(dat, interior=True)

   exterior_excluded = ~isin 
   interior_excluded = isin & (~isint)

   fig, ax = plt.subplots(1, 1, figsize=(10,10))

   # ax.plot(dat['RA'], dat['DEC'], marker='.', lw=0.0, markersize=.5, c='k')
   
   ax.plot(dat['RA'][exterior_excluded], dat['DEC'][exterior_excluded], marker='.', lw=0.0, markersize=.5, c='r')
   ax.plot(dat['RA'][interior_excluded], dat['DEC'][interior_excluded], marker='.', lw=0.0, markersize=.5, c='m')   
   ax.plot(dat['RA'][isint], dat['DEC'][isint], marker='.', lw=0.0, markersize=.5, c='k')
   
   ax.set_title('Gold geometric mask')

   pl.show()
