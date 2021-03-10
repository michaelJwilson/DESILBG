import numpy as np
import pandas as pd

from astropy.table import Table
from not_bright import not_bright

from selection.gdrops import gdrops

from datamodel import datamodel

# Safeguard, but should be unncessary. 
np.random.seed(seed=314)

# Area in u-band (approx); [sq. deg.]
cosmos_garea = 7.84
cosmos_uarea = 4.41

# Load latest clauds catalog.
cat = Table.read('/global/cscratch1/sd/mjwilson/clauds/March2021/COSMOS_v9_v210225.fits')

print('Latest COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to uband area.
cat = cat[cat['MASK'] == 0]

print('After stellar masking, COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to the u imaging footprint. Table A1 of https://www.overleaf.com/read/wdtmwbwvnjgc.
cat = cat[cat['FLAG_FIELD_BINARY'][:,0] == True]

print('After limiting to the g imaging, COSMOS catalog has {} sources.'.format(len(cat)))

isin = not_bright(cat)

cat = cat[isin]

print('After removing bright sources, COSMOS catalog has {} sources.'.format(len(cat)))

is_gdrop = gdrops(cat)

cat = cat[is_gdrop]

print('COSMOS catalog has {} sources meeting g selection at a target density of {:.3f} per sq. deg.'.format(len(cat), len(cat) / (cosmos_garea - cosmos_uarea)))

# Keep column list.                                                                                                                                                                                                             
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

cat = cat[cols]

cat.write('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/G/g.fits', format='fits', overwrite=True)

cat = datamodel(cat)

cat.write('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/G/scnd_g.fits', format='fits', overwrite=True)

print('Writing to {}.'.format('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/G/g.fits'))
