import numpy as np
import pandas as pd

from astropy.table import Table
from not_bright import not_bright

from selection.gdrops import gdrops
from selection.g_nondetect import g_nondetect

from uniform_magpriority import uniform_magpriority

from datamodel import datamodel


overwrite=False

root='/global/cscratch1/sd/mjwilson/DESILBG/TEST/'
# root='/global/cscratch1/sd/mjwilson/DESILBG/GOLD/'  

# Safeguard, but should be unncessary. 
np.random.seed(seed=314)

# Area in g band (approx); [sq. deg.]
cosmos_garea = 7.84

# Load latest clauds catalog.
cat = Table.read('/global/cscratch1/sd/mjwilson/clauds/March2021/COSMOS_v9_v210225.fits')

print('Latest COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to no stellar mask. 
cat = cat[cat['MASK'] == 0]

print('After stellar masking, COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to the hsc imaging footprint. Table A1 of https://www.overleaf.com/read/wdtmwbwvnjgc.
cat = cat[cat['FLAG_FIELD_BINARY'][:,0] == True]

print('After limiting to the g imaging, COSMOS catalog has {} sources.'.format(len(cat)))

# Fainter than 17th mag in ugrizy. 
isin = not_bright(cat)

cat = cat[isin]

print('After removing bright sources, COSMOS catalog has {} sources.'.format(len(cat)))

is_gdrop = gdrops(cat)
is_gnondetect = g_nondetect(cat)

print('With g selection, COSMOS catalog has {} sources.'.format(np.count_nonzero(is_gdrop)))
print('With g-nondetect selection, COSMOS catalog has {} sources.'.format(np.count_nonzero(is_gnondetect)))

isin = is_gdrop | is_gnondetect

cat = cat[isin]

print('COSMOS catalog has {} sources meeting g | g nondetect selection at a target density of {:.3f} per sq. deg.'.format(len(cat), len(cat) / cosmos_garea))

##  --- Prioritization ---
prioritized_cat = uniform_magpriority('i', 22.5, 25.5, cat)

# clauds-like data model.                                                                                                                                                                                                             
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

prioritized_cat = prioritized_cat[cols]

print('\n\n')

prioritized_cat.pprint()

if overwrite:
    prioritized_cat.write('{}/DESILBG_G/desilbg_g.fits'.format(root), format='fits', overwrite=overwrite)

    # ADM-like data model. 
    prioritized_cat = datamodel(prioritized_cat)

    prioritized_cat.write('{}/DESILBG_G/desilbg_g_scnd.fits'.format(root), format='fits', overwrite=overwrite)

    print('Writing to {}.'.format('{}/DESILBG_G/desilbg_g.fits'.format(root)))
    
else:
    print('WARNING:  Test run, files not written.  Would write to: {}'.format('{}/DESILBG_G/desilbg_g.fits'.format(root)))
