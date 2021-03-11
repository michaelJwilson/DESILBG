import numpy as np
import pandas as pd

from astropy.table import Table
from not_bright import not_bright
from selection.tomog import tomog
from gold_footprint import gold_footprint
from datamodel import datamodel

# Safeguard, but should be unncessary. 
np.random.seed(seed=314)

# Area in u-band (approx); [sq. deg.]
cosmos_uarea = 4.41

# Load latest clauds catalog.
cat = Table.read('/global/cscratch1/sd/mjwilson/clauds/March2021/COSMOS_v9_v210225.fits')

print('Latest COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to no stellar mask. 
cat = cat[cat['MASK'] == 0]

print('After stellar masking, COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to the u imaging footprint. Table A1 of https://www.overleaf.com/read/wdtmwbwvnjgc.
cat = cat[cat['FLAG_FIELD_BINARY'][:,1] == True]

print('After limiting to the u imaging, COSMOS catalog has {} sources.'.format(len(cat)))

# Less than 17th mag in ugrizy. 
isin = not_bright(cat)

cat = cat[isin]

print('After removing bright sources, COSMOS catalog has {} sources.'.format(len(cat)))

is_tomog = tomog(cat)

cat = cat[is_tomog]

print('COSMOS catalog has {} sources meeting TMG selection at a target density of {:.3f} per sq. deg.'.format(len(cat), len(cat) / cosmos_uarea))

isin = gold_footprint(cat, interior=True)

cat = cat[isin]

print('COSMOS catalog has {} sources meeting TMG selection at a target density of {:.3f} per sq. deg., after geometric mask'.format(len(cat), len(cat) / cosmos_uarea))

# Prioritize by r; brightest first. 
cat.sort('r')

# clauds-like datamodel.                                                                                                                                                                                                             
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

cat   = cat[cols]

print('\n\n')

cat.pprint()

cat.write('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/TMGV9/tmg_v9.fits', format='fits', overwrite=True)

##  ADM-like datamodel.
cat = datamodel(cat)

cat.write('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/TMGV9/scnd_tmg_v9.fits', format='fits', overwrite=True)
