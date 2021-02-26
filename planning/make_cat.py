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
tomog = '/global/cscratch1/sd/mjwilson/DESILBG/tomog/tomog.fits'
dat   = Table.read(tomog)
dat['SAMPLE'] = 'CLAUDS-TMG'
dat['PMRA']   = 0.0
dat['PMDEC']  = 0.0

# Remove overlap
overlap = np.isin(cat['ID'], dat['ID'])

cat   = cat[~overlap]

cat   = vstack((cat, dat))

opath = '/global/cscratch1/sd/mjwilson/secondary/sv1/raw/LBG_TOMOG.fits'
cat.write(opath, format='fits', overwrite=True)

# [('RA', '>f8'), ('DEC', '>f8'), ('PMRA', '>f4'), ('PMDEC', '>f4'), ('REF_EPOCH', '>f4'), ('OVERRIDE', '?')]
cat = cat['RA', 'DEC', 'PMRA', 'PMDEC', 'REF_EPOCH', 'OVERRIDE']

# Assumed 2015.
cat['RA']  = cat['RA'].data.astype('>f8')
cat['DEC'] = cat['DEC'].data.astype('>f8')

cat['PMRA'] = cat['PMRA'].data.astype('>f4')
cat['PMDEC'] = cat['PMDEC'].data.astype('>f4')

cat['REF_EPOCH'] = np.array([0.0] * len(cat), dtype='>f4')
cat['OVERRIDE'] = False

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
