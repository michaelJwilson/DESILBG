import numpy as np

from astropy.table import Table


cat = Table.read('/global/cscratch1/sd/mjwilson/secondary/sv1/indata/ToO.fits')

# [('RA', '>f8'), ('DEC', '>f8'), ('PMRA', '>f4'), ('PMDEC', '>f4'), ('REF_EPOCH', '>f4'), ('OVERRIDE', '?')]
cat = cat['RA', 'DEC', 'PMRA', 'PMDEC', 'REF_EPOCH', 'OVERRIDE']

# Assumed 2015.                                                                                                                                                                                                                            
cat['RA']  = cat['RA'].data.astype('>f8')
cat['DEC'] = cat['DEC'].data.astype('>f8')

cat['PMRA'] = cat['PMRA'].data.astype('>f4')
cat['PMDEC'] = cat['PMDEC'].data.astype('>f4')

cat['REF_EPOCH'] = np.array([0.0] * len(cat), dtype='>f4')
cat['OVERRIDE'] = False

opath = '/global/cscratch1/sd/mjwilson/secondary/sv1/indata/ToO.fits'

cat.write(opath, format='fits', overwrite=True)
