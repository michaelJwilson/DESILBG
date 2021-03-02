import fitsio
import pylab as pl

from astropy.table import Table
from desimodel.footprint import is_point_in_desi

cols = ['ra',
        'dec',
        'ref_cat',
        'ref_id',
        'ref_epoch',
        'mag',
        'mask_mag',
        'radius',
        'radius_pix',
        'pmra',
        'pmdec',
        'parallax',
        'in_desi',
        'istycho',
        'isgaia',
        'isbright',
        'ismedium']

cos = Table.read('/global/cscratch1/sd/mjwilson/clauds/cosmos.fits')
cos.pprint()

# REF_EPOCH 2015.5
dat = fitsio.read('/global/cfs/cdirs/cosmo/data/legacysurvey/dr9/masking/gaia-mask-dr9.fits.gz')


isin = is_point_in_desi(cos, dat['ra'], dat['dec'])

dat = dat[isin]
dat = Table(dat)
dat = dat[cols] 

# print(len(dat))

dat.write('/global/cscratch1/sd/mjwilson/clauds/gaia.fits', format='fits', overwrite=True)

# pl.plot(dat['ra'], dat['dec'], marker='.', lw=0.0, markersize=1.)

# pl.show()
