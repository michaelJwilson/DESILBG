import os
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import astropy.units as u

from astropy.table import Table
from astropy.coordinates import SkyCoord


scr  = os.environ['CSCRATCH']

scnd = fits.open(scr + '/SCNDCOSMOS/082000-scnd.fits')
scnd = scnd['MTL'].data

targ = fits.open(scr + '/SCNDCOSMOS/082000-targ.fits')
targ = targ['MTL'].data

dlbg = Table.read('/global/cscratch1/sd/mjwilson/secondary/sv1/raw/LBG_TOMOG.fits')
dlbg.sort('RA')

fa   = fits.open(scr + '/SCNDCOSMOS/fba-082000.fits')
ftargets = fa['FTARGETS']

fassign = Table.read(scr + '/SCNDCOSMOS/fba-082000.fits', 'FASSIGN')
fassign.sort('TARGET_RA')

dlbg = dlbg[np.isin(dlbg['RA'], fassign['TARGET_RA'])]
fmatch = fassign[np.isin(fassign['TARGET_RA'], dlbg['RA'])]

# c1  = SkyCoord(ra=dlbg['RA'] * u.deg, dec=dlbg['DEC'] * u.deg, frame='icrs')
# c2  = SkyCoord(ra=fmatch['TARGET_RA'] * u.deg, dec=fmatch['TARGET_DEC'] * u.deg, frame='icrs')
# 
# idx, d2d, d3d = c1.match_to_catalog_sky(c2)

dlbg.pprint()

samples, cnts = np.unique(dlbg['SAMPLE'], return_counts=True)                                                                                                                                                                                          
# CLAUDS-BX:  174
# CLAUDS-G:  1662
# CLAUDS-TMG: 575
# CLAUDS-U:  1188

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

for s, c in zip(samples, colors):
    ss = dlbg[dlbg['SAMPLE'] == s]

    pl.plot(ss['RA'], ss['DEC'], c=c, marker='.', lw=0.0, markersize=1, label=s)

pl.legend(frameon=False, loc=1, ncol=2)      
pl.ylim(0.75, 4.25)
pl.show()
