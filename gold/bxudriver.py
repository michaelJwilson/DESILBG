import numpy as np
import pandas as pd

from astropy.table import Table
from not_bright import not_bright

from selection.udrops import udrops
from selection.bx import bx
from selection.u_nondetect import u_nondetect

from datamodel import datamodel

# Safeguard, but should be unncessary. 
np.random.seed(seed=314)

# Area in u-band (approx); [sq. deg.]
cosmos_uarea = 4.41

# Load latest clauds catalog.
cat = Table.read('/global/cscratch1/sd/mjwilson/clauds/March2021/COSMOS_v9_v210225.fits')

print('Latest COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to uband area.
cat = cat[cat['MASK'] == 0]

print('After stellar masking, COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to the u imaging footprint. Table A1 of https://www.overleaf.com/read/wdtmwbwvnjgc.
cat = cat[cat['FLAG_FIELD_BINARY'][:,1] == True]

print('After limiting to the u imaging, COSMOS catalog has {} sources.'.format(len(cat)))

isin = not_bright(cat)

cat = cat[isin]

print('After removing bright sources, COSMOS catalog has {} sources.'.format(len(cat)))

is_bx = bx(cat)
is_udrop = udrops(cat)
is_unondetect = u_nondetect(cat)

print('With BX selection, COSMOS catalog has {} sources.'.format(np.count_nonzero(is_bx)))
print('With u selection, COSMOS catalog has {} sources.'.format(np.count_nonzero(is_udrop)))
print('With u-nondetect selection, COSMOS catalog has {} sources.'.format(np.count_nonzero(is_unondetect)))

isin = is_bx | is_udrop | is_unondetect

cat = cat[isin]

print('COSMOS catalog has {} sources meeting BX | u | u nondetect selection at a target density of {:.3f} per sq. deg.'.format(len(cat), len(cat) / cosmos_uarea))

##  --- Prioritization ---

# Keep column list.                                                                                                                                                                                                             
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

cat   = cat[cols]

cat.pprint()

cat.write('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/BXU/bxu.fits', format='fits', overwrite=True)

##  Prioritization scheme for BX | U selection.
cat = datamodel(cat)

cat.write('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/BXU/scnd_bxu.fits', format='fits', overwrite=True)

print('Writing to {}.'.format('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/BXU/bxu.fits'))
