import numpy as np
import astropy.io.fits as fits

from   astropy.table import Table, vstack


# Made by make_cat; sorted highest priority first. 
lbgs = Table.read('/global/cscratch1/sd/mjwilson/secondary/sv1/raw/Mar21/LBG_LBGLAE.fits')

# Made by target/proposals/docs/master-comp.ipynb; matched to 1 arcsec. 
dups = Table.read('/global/cscratch1/sd/mjwilson/DESILBG/tomog/lbglae-matches.fits')

# Made by Christophe. 
tmgs = Table.read('/global/cfs/cdirs/desi/target/secondary/sv1/indata/LBG_TOMOG.fits')

print('Len LBGS: {}'.format(len(lbgs)))
print('Len DUPS: {}'.format(len(dups)))
print('Len TMGS: {}'.format(len(tmgs)))

exclude = np.isin(lbgs['ID'], dups['ID'])

lbgs = lbgs[~exclude]

print('LEN LBGS NON DUP: {}'.format(len(lbgs)))

# [('RA', '>f8'), ('DEC', '>f8'), ('PMRA', '>f4'), ('PMDEC', '>f4'), ('REF_EPOCH', '>f4'), ('OVERRIDE', '?')]

#
cat = lbgs['RA', 'DEC', 'PMRA', 'PMDEC', 'REF_EPOCH', 'OVERRIDE', 'U', 'U_ERR', 'G', 'G_ERR', 'R', 'R_ERR', 'I', 'I_ERR']

# Assumed 2015.                                                                                                                                                                                                      
cat['RA']  = cat['RA'].data.astype('>f8')
cat['DEC'] = cat['DEC'].data.astype('>f8')
cat['PMRA'] = cat['PMRA'].data.astype('>f4')
cat['PMDEC'] = cat['PMDEC'].data.astype('>f4')
cat['REF_EPOCH'] = np.array([0.0] * len(cat), dtype='>f4')
cat['OVERRIDE'] = False                    

cat = vstack((tmgs, cat))

cat.pprint()

assert np.count_nonzero(cat['I'].mask) == len(tmgs)

cat.write('/global/cscratch1/sd/mjwilson/secondary/sv1/indata/LBG_TOMOG.fits', format='fits', overwrite=True)

cat_tmgs = cat[cat['I'].mask]

print(len(cat_tmgs), len(tmgs))

assert  np.all(cat_tmgs['RA']  == tmgs['RA'])
assert  np.all(cat_tmgs['DEC'] == tmgs['DEC'])
