import pylab as pl
import numpy as np
import matplotlib.pyplot as plt

from   astropy.coordinates import ICRS
from   astropy.coordinates import SkyCoord
from   astropy.table       import Table
from   astropy             import units as u


tomog = '/global/cscratch1/sd/mjwilson/secondary/sv1/indata/LBG_TOMOG.fits'
dat   = Table.read(tomog)

# Cut to COSMOS. 
dat   = dat[dat['DEC'] > 0.5]

# dat.pprint()

# gmr = dat['G'] - dat['R']
# umg = dat['U'] - dat['G'] 

# pl.plot(gmr, umg, marker='.', lw=0.0, c='b', markersize=1)
# pl.xlim(-1., 3.0)
# pl.ylim(-1., 4.5)
# pl.show()

# pl.hist(dat['PHOTO_Z'], bins=100)
# pl.show()

# 
desilbg        = Table.read('/global/cscratch1/sd/mjwilson/DESILBG/Feb21/targets/desi_lbg.fits')

# https://learn.astropy.org/Coordinates.html
c              = SkyCoord(ra=dat['RA'] * u.degree, dec=dat['DEC'] * u.degree, frame='icrs')
catalog        = SkyCoord(ra=desilbg['RA'] * u.degree, dec=desilbg['DEC'] * u.degree, frame='icrs')

idxc, d2d, d3d = c.match_to_catalog_sky(catalog)

# pl.hist(d2d.arcsec, histtype='step', bins=np.logspace(-2., 0.0, 100))
# pl.xlabel('separation [arcsec]', fontsize=9)
# pl.xscale('log')
# pl.show()

# c2015         = c.transform_to(ICRS(equinox='J2015'))
# print(len(idxc), len(dat), len(desilbg))
# print(len(c), len(catalog), len(idxc))

matches         = desilbg[idxc]
matches['SEP']  = d2d.arcsec 
matches         = matches[matches['SEP'] < 0.1]

# dra, ddec     = c.spherical_offsets_to(catalog[idxc])

# matches.pprint()
# dat.pprint()

unmatched       = dat[d2d.arcsec > 1.0]
unmatched.pprint()

gmr             = unmatched['G'] - unmatched['R']                                                                                                                                             
umg             = unmatched['U'] - unmatched['G']  

# pl.plot(gmr, umg, marker='.', lw=0.0, c='b', markersize=1)                                                                                                                                              
# pl.xlim(-1., 3.0)                                                                                                                                                                                        
# pl.ylim(-1., 4.5)                                                                                                                                                                                         
# pl.show()

# pl.hist(unmatched['R'], bins=100)                                                                                                                                                                        
# pl.show()

# pl.hist(unmatched['PHOTO_Z'], bins=100)                                                                                                                                                                 
# pl.show() 

pl.plot(unmatched['RA'], unmatched['DEC'], marker='.', lw=0.0, c='b', markersize=1)
# pl.xlim(-1., 3.0)                                                                                                                                                                                                        
# pl.ylim(-1., 4.5)                                                                                                                                                                                                          
pl.show()
