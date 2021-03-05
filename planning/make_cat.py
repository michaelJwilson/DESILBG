import glob
import pandas as pd
import numpy as np
import healpy as hp
import astropy.io.fits as fits

from desitarget.geomask import is_in_hp
from astropy.table import Table, vstack


root  = '/global/cscratch1/sd/mjwilson/DESILBG/Mar21/targets/' 
cat   = None

# Keep restricted column list. 
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

for tracer in ['bxdrops', 'udrops', 'gdrops']:
    print('Solving for {}.'.format(tracer))
    
    files = glob.glob(root + '/{}/*.fits'.format(tracer))

    print('{} files to be collected.'.format(len(files)))
    
    for f in files:
        toexclude = f.split('-')[1][0]

        # Skip minus priorities (objects lost as a fixed number of objects per priority class kept).
        if toexclude == 'm':
            print('Skipping {}'.format(f))
            continue
        
        if cat is None:
            cat = Table.read(f)[cols]

        else:
            cat = vstack((cat, Table.read(f)[cols])) 
            
print('Collected {}K LBGLAE targets.'.format(len(cat) / 1.e3))

cat['OVERRIDE'] = cat['OVERRIDE'].data.astype(bool)
'''
# Deprecated:  Now handled by duplicates.
# Append tomog.
tomog = '/global/cscratch1/sd/mjwilson/DESILBG/tomog/tomog.fits'
dat = Table.read(tomog)
dat['SAMPLE'] = 'CLAUDS-TMG'
dat['PMRA']   = 0.0
dat['PMDEC']  = 0.0

print('Collected {}K TMG targets.'.format(len(dat) / 1.e3))

# Remove overlap
overlap  = np.isin(cat['ID'], dat['ID'])
# doverlap = np.isin(dat['ID'], cat['ID']) 

types = np.unique(cat['SAMPLE'])

for tt in types:
    istype = cat['SAMPLE'] == tt

    istypeoverlap = istype & overlap

    print(tt, np.count_nonzero(istype), np.count_nonzero(istypeoverlap))
    
# cat.sort('ID')
# dat.sort('ID')

# cat[overlap].pprint()
# dat[doverlap].pprint()

cat   = cat[~overlap]
'''

cat.sort('PRIORITY')

# Reverse: highest priority first.
cat = cat[::-1]

cat.pprint()

# cat   = vstack((dat, cat))

print('Total candidates: {}k'.format(len(cat) / 1.e3))

for band in ['u', 'uS', 'g', 'r']:
    print(band, np.sort(cat[band].data))
    
# Patch bands:                                                                                                                                                         
for band in ['u', 'uS', 'g', 'r', 'i', 'z', 'y', 'Yv', 'J', 'H', 'Ks']:
    cat[band.upper()] = cat[band]
    cat[band.upper() + '_ERR'] = cat[band + '_err']

    del cat[band]
    del cat[band + '_err']

# Exclude bright objects.
for band in ['U', 'G', 'R', 'I']:
    # Defined magnitudes 
    isin = cat[band] > -99.

    exclude = isin & (cat[band] < 19.)

    print(band, 'Excluding: ', np.count_nonzero(exclude))

    cat = cat[~exclude]

cat.pprint()
    
opath = '/global/cscratch1/sd/mjwilson/secondary/sv1/raw/Mar21/LBG_LBGLAE.fits'
cat.write(opath, format='fits', overwrite=True)

'''
# Deprecated: now handled by duplicates.py
# 
# [('RA', '>f8'), ('DEC', '>f8'), ('PMRA', '>f4'), ('PMDEC', '>f4'), ('REF_EPOCH', '>f4'), ('OVERRIDE', '?')]
cat = cat['RA', 'DEC', 'PMRA', 'PMDEC', 'REF_EPOCH', 'OVERRIDE']

# Assumed 2015.
cat['RA']  = cat['RA'].data.astype('>f8')
cat['DEC'] = cat['DEC'].data.astype('>f8')

cat['PMRA'] = cat['PMRA'].data.astype('>f4')
cat['PMDEC'] = cat['PMDEC'].data.astype('>f4')

cat['REF_EPOCH'] = np.array([0.0] * len(cat), dtype='>f4')
cat['OVERRIDE'] = False

opath = '/global/cscratch1/sd/mjwilson/secondary/sv1/indata/LBG_LBGLAE.fits'

print('Writing to {}.'.format(opath))

cat.pprint()

cat.write(opath, format='fits', overwrite=True)

# nside      = 8
# theta, phi = np.radians(90.-cat['DEC'].data), np.radians(cat['RA'].data)
# pixnums    = hp.ang2pix(nside, theta, phi, nest=True)
# pixnums    = np.unique(pixnums)
# 
# print(pixnums)

dat = fits.open('/global/cfs/cdirs/desi/target/secondary/sv1/indata/LBG_TOMOG.fits')                                                                                                            

print('Currently in official secondary dir.: {}k'.format(len(dat[1].data) / 1.e3))
'''
