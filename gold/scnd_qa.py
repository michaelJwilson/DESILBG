import fitsio
import numpy as np
import pylab as pl

from   astropy.table                 import Table
from   desitarget.sv1.sv1_targetmask import desi_mask, bgs_mask, mws_mask
from   desitarget.sv1.sv1_targetmask import scnd_mask

from   astropy.coordinates           import SkyCoord
from   astropy                       import units as u


scnd            = Table.read('/global/cfs/cdirs/desi/target/catalogs/dr9/0.52.0/targets/sv1/secondary/dark/sv1targets-dark-secondary.fits')

scnd_yeche      = scnd[(scnd['SV1_SCND_TARGET'] & scnd_mask['LBG_TOMOG_COSMOS_FINAL']) != 0 ]
scnd_bxu        = scnd[(scnd['SV1_SCND_TARGET'] & scnd_mask['DESILBG_BXU_FINAL']) != 0 ]

sc_scnd_yeche   = SkyCoord(ra=scnd_yeche['RA'], dec=scnd_yeche['DEC'])
sc_scnd_bxu     = SkyCoord(ra=scnd_bxu['RA'], dec=scnd_bxu['DEC'])

idx, d2d, d3d   = sc_scnd_yeche.match_to_catalog_sky(sc_scnd_bxu)

matched         = scnd_yeche[d2d.arcsecond < 1.]
matched_bxu     = scnd_bxu[idx][d2d.arcsecond < 1.]

matched.sort('RA')                                                                                                                                                                                                              

matched_bxu.sort('RA')                                                                                                                                                                                                          

for x in ['RA', 'DEC', 'PMRA', 'PMDEC', 'REF_EPOCH']:
    print(x, np.mean(matched[x] == matched_bxu [x]), np.count_nonzero(matched[x] != matched_bxu [x]))

    
