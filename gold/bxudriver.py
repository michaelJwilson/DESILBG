import numpy as np
import pandas as pd

from astropy.table import Table
from not_bright import not_bright

from selection.bxu import bxu
from selection.u_nondetect import u_nondetect
from gold_footprint import gold_footprint
from uniform_magpriority import uniform_magpriority

from datamodel import datamodel

overwrite=False

root='/global/cscratch1/sd/mjwilson/DESILBG/TEST/'
# root='/global/cscratch1/sd/mjwilson/DESILBG/GOLD/'

# Safeguard, but should be unncessary. 
np.random.seed(seed=314)

# Area in u-band (approx); [sq. deg.]
cosmos_uarea = 4.41

# Load latest clauds catalog.
cat = Table.read('/global/cscratch1/sd/mjwilson/clauds/March2021/COSMOS_v9_v210225.fits')

print('Latest COSMOS catalog has {} sources.'.format(len(cat)))

# Apply stellar mask.
cat = cat[cat['MASK'] == 0]

print('After stellar masking, COSMOS catalog has {} sources.'.format(len(cat)))

# Limit to the u imaging footprint. Table A1 of https://www.overleaf.com/read/wdtmwbwvnjgc.
cat = cat[cat['FLAG_FIELD_BINARY'][:,1] == True]

print('After limiting to the u imaging, COSMOS catalog has {} sources.'.format(len(cat)))

# ugrizy all < 17; removes ~1000 sources.
isin = not_bright(cat)

cat = cat[isin]

print('After removing bright sources, COSMOS catalog has {} sources.'.format(len(cat)))

is_bxu = bxu(cat)
is_unondetect = u_nondetect(cat)

print('With BXU selection, COSMOS catalog has {} sources.'.format(np.count_nonzero(is_bxu)))
print('With u-nondetect selection, COSMOS catalog has {} sources.'.format(np.count_nonzero(is_unondetect)))

isin = is_bxu | is_unondetect

cat = cat[isin]

print('COSMOS catalog has {} sources meeting BX | u | u nondetect selection at a target density of {:.3f} per sq. deg.'.format(len(cat), len(cat) / cosmos_uarea))

isin = gold_footprint(cat, interior=True)

cat = cat[isin]

print('COSMOS catalog has {} sources meeting BX | u | u nondetect selection at a target density of {:.3f} per sq. deg., after geometric mask'.format(len(cat), len(cat) / cosmos_uarea))

# For info only. 
is_bxu = bxu(cat)
is_unondetect = u_nondetect(cat)

print('With BXU selection, COSMOS catalog has {} sources, after geometric mask.'.format(np.count_nonzero(is_bxu)))
print('With u-nondetect selection, COSMOS catalog has {} sources, after geometric mask.'.format(np.count_nonzero(is_unondetect)))

check_cat = Table(cat, copy=True)
check_ids = np.array(np.unique(check_cat['ID']), copy=True)

##  --- Prioritization ---
prioritized_cat = uniform_magpriority('r', 22.5, 24.5, cat)

assert np.all(np.sort(prioritized_cat['ID']) == check_ids)

assert np.all(prioritized_cat['RA'][np.argsort(prioritized_cat['ID'])] == check_cat['RA'][np.argsort(check_cat['ID'])])                                                                                                                       
assert np.all(prioritized_cat['DEC'][np.argsort(prioritized_cat['ID'])] == check_cat['DEC'][np.argsort(check_cat['ID'])])                                                                                                                     
assert np.all(prioritized_cat['r'][np.argsort(prioritized_cat['ID'])] == check_cat['r'][np.argsort(check_cat['ID'])])  

# Clauds-like datamodel.
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

prioritized_cat = prioritized_cat[cols]

print('\n\n')

prioritized_cat.pprint()

if overwrite:
    prioritized_cat.write('{}/DESILBG_BXU/desilbg_bxu.fits'.format(root), format='fits', overwrite=overwrite)

    ##  ADM-like datamodel.
    prioritized_cat = datamodel(prioritized_cat)

    prioritized_cat.write('{}/DESILBG_BXU/desilbg_bxu_scnd.fits'.format(root), format='fits', overwrite=overwrite)

    print('Writing to {}.'.format('{}/DESILBG_BXU/desilbg_bxu.fits'.format(root)))

else:
    print('WARNING:  Test run, files not written.  Would write to: {}'.format('{}/DESILBG_BXU/desilbg_bxu.fits'.format(root)))
