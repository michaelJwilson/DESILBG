import glob
import pandas as pd
import numpy as np
import healpy as hp

from   desitarget.geomask import is_in_hp
from   astropy.table import Table, vstack


root  = '/global/cscratch1/sd/mjwilson/DESILBG/Feb21/targets/' 
cat   = None

# Keep restricted column list. 
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

for tracer in ['bxdrops', 'udrops', 'gdrops']:
    print('Solving for {}.'.format(tracer))
    
    files = glob.glob(root + '/{}/*.fits'.format(tracer))

    print('{} files to be collected.'.format(len(files)))
    
    for f in files:
        if cat is None:
            cat = Table.read(f)[cols]

        else:
            cat = vstack((cat, Table.read(f)[cols])) 
            
print('Collected {}M LBGLAE targets.'.format(len(cat) / 1.e6))

cat['OVERRIDE'] = cat['OVERRIDE'].data.astype(bool)

# Patch bands:
for band in ['u', 'uS', 'g', 'r', 'i', 'z', 'y', 'Yv', 'J', 'H', 'Ks']:
    cat[band.upper()] = cat[band]
    cat[band.upper() + '_ERR'] = cat[band + '_err']
    
    del cat[band]
    del cat[band + '_err']

cat.sort('PRIORITY')

# Append tomog.
tomog = '/global/cscratch1/sd/mjwilson/secondary/sv1/backup/indata/LBG_TOMOG.fits'
dat   = Table.read(tomog)
dat['SAMPLE'] = 'CLAUDS-TMG'

cat   = vstack((cat, dat))

opath = '/global/cscratch1/sd/mjwilson/secondary/sv1/indata/LBG_TOMOG.fits'

print('Writing to {}.'.format(opath))

cat.pprint()

cat.write(opath, format='fits', overwrite=True)

# nside      = 8
# theta, phi = np.radians(90.-cat['DEC'].data), np.radians(cat['RA'].data)
# pixnums    = hp.ang2pix(nside, theta, phi, nest=True)
# pixnums    = np.unique(pixnums)
# 
# print(pixnums)
