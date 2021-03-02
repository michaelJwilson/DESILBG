import os
import glob
import fitsio
import numpy as np
import pylab as pl
import astropy.io.fits as fits

from astropy.table import Table, vstack
from desimodel.io import load_tiles 
from desimodel.footprint import is_point_in_desi

scr = os.environ['CSCRATCH']
fs  = glob.glob(scr + '/clauds/March2021/*.fits')

tiles = Table(load_tiles())
tiles = tiles[tiles['PASS'] == 1]

tiles.pprint()

cat = None

for f in fs:
    print('Solving for {}.'.format(f))
    
    tb  = Table.read(f)

    idx = is_point_in_desi(tiles, tb['RA'], tb['DEC'], return_tile_index=True)
    idx = np.unique(idx[1])
    
    ts  = tiles[idx]
    
    field = f.split('/')[-1].split('_')[0]

    pl.plot(ts['RA'], ts['DEC'], marker='.', c='k', lw=0.0)
    
    ts        = ts[:1]
    ts['RA']  = np.median(tb['RA']).astype(np.float64)
    ts['DEC'] = np.median(tb['DEC']).astype(np.float64)
    ts['FIELD'] = field
    
    ts        = ts['FIELD', 'RA', 'DEC']
    
    if cat is None:
        cat = ts

    else:
        cat = vstack((cat, ts))

dat = np.array([('W3', 214., 52.)], dtype=[('FIELD', np.str), ('RA', np.float64), ('DEC', np.float64)])

cat  = vstack((cat, Table(data=dat, names=['FIELD', 'RA', 'DEC'])))
cat[-1]['FIELD'] = 'W3'

cat.pprint()

# pl.show()

# cat.write(scr + '/clauds/tiles.fits', format='fits', overwrite=True)

cosmos = cat[cat['FIELD'] == 'COSMOS']
cosmos.write(scr + '/clauds/cosmos.fits', format='fits', overwrite=True)

