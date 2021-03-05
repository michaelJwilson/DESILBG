import numpy as np
import astropy.io.fits as fits

from astropy.table import Table, vstack

lbgs = Table.read('/global/cscratch1/sd/mjwilson/secondary/sv1/raw/Mar21/LBG_LBGLAE.fits')
dups = Table.read('/global/cscratch1/sd/mjwilson/DESILBG/tomog/lbglae-matches.fits')
tmgs = Table.read('/global/cfs/cdirs/desi/target/secondary/sv1/indata/LBG_TOMOG.fits')

for x in [lbgs, dups, tmgs]:
    print(len(x))

exclude = np.isin(lbgs['ID'], dups['ID'])

lbgs = lbgs[~exclude]

print(len(lbgs))                  

cat = vstack((tmgs, lbgs))

# [('RA', '>f8'), ('DEC', '>f8'), ('PMRA', '>f4'), ('PMDEC', '>f4'), ('REF_EPOCH', '>f4'), ('OVERRIDE', '?')]                                                                                                                              
cat = cat['RA', 'DEC', 'PMRA', 'PMDEC', 'REF_EPOCH', 'OVERRIDE']                                                                                                                                                                                                                                                                                                                                                                                                                        
# Assumed 2015.                                                                                                                                                                                                                            
cat['RA']  = cat['RA'].data.astype('>f8')                                                                                                                                                                                                  
cat['DEC'] = cat['DEC'].data.astype('>f8')                                                                                                                                                                                                   
cat['PMRA'] = cat['PMRA'].data.astype('>f4')                                                                                                                                                                                                 
cat['PMDEC'] = cat['PMDEC'].data.astype('>f4')                                                                                                                                                                                                                                                                                                                                                                                                                                            
cat['REF_EPOCH'] = np.array([0.0] * len(cat), dtype='>f4')                                                                                                                                                                                   
cat['OVERRIDE'] = False                    

cat.pprint()

cat.write('/global/cscratch1/sd/mjwilson/secondary/sv1/indata/LBG_TOMOG.fits', format='fits', overwrite=True)
