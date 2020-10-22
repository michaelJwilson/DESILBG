import os
import fitsio
import desimodel
import astropy
import pandas                as     pd
import pylab                 as     pl
import numpy                 as     np
import astropy.io.fits       as     fits
import matplotlib.pyplot     as     plt

from   datetime              import datetime
from   astropy.table         import Table, vstack, join
from   astropy.coordinates   import Angle, SkyCoord
from   astropy               import units as u

from   desimodel.footprint   import is_point_in_desi
from   desimodel             import io
from   desitarget.geomask    import circles
from   desitarget.targetmask import desi_mask, obsconditions

def get_goldrush():
    # https://arxiv.org/pdf/1704.06004.pdf
    dat   = fitsio.read('/global/cscratch1/sd/mjwilson/goldrush_mizukizs.fits')    
    
    return dat

def get_splash():
    dat   = fitsio.read('/global/cscratch1/sd/mjwilson/SPLASH/SPLASH_SXDF_Mehta+_v1.6.fits')

    # In Musubi, 1.7 sq. deg.
    dat   = dat[dat['COVERAGE_FLAG_musubi_u'] > 0]
    Area  = 1.7
    
    
    dat   = Table(dat)
    
    dat['u-g'] = dat['MAG_AUTO_musubi_u'] - dat['MAG_AUTO_hsc_g']
    dat['g-r'] = dat['MAG_AUTO_hsc_g']    - dat['MAG_AUTO_hsc_r']
    dat['r-i'] = dat['MAG_AUTO_hsc_r']    - dat['MAG_AUTO_hsc_i']
    
    return  dat, Area

def splash_drops(dband='u'):
    # https://arxiv.org/pdf/0903.3951.pdf

    isin      = np.ones(len(splash), dtype=bool)

    if dband == 'BX':
        # LATIS, https://arxiv.org/pdf/2002.10676.pdf
        # 0.5 < u - g < 2.2 and -0.1 < g - r < 1.0 and u - g > 0.5 + 2.3 (g - r - 0.35). 
        isin &= splash['u-g'] >  0.5
        isin &= splash['u-g'] <  2.2
        isin &= splash['g-r'] > -0.1
        isin &= splash['g-r'] <  1.0
        isin &= splash['u-g'] >  0.5 + 2.3 * (splash['g-r'] - 0.35)

    elif dband == 'u':
      # u drops.
      # 1.5 < u - g and -1.0 < g - r < 1.2 and 1.5 (g - r) < (u - g) - 0.75
      isin &= splash['u-g'] >  1.5
      isin &= splash['g-r'] > -1.0
      isin &= splash['g-r'] <  1.2
      isin &= 1.5 * splash['g-r'] <  splash['u-g'] - 0.75

    elif dband == 'g':
        # g drops
        # 1.0 < (g - r) and - 1.0 < (r - i) < 1.0 and 1.5 (r-i) < (g-r) - 0.8
        isin &= splash['g-r'] >  1.0
        isin &= splash['r-i'] > -1.0
        isin &= splash['r-i'] <  1.0
        isin &= 1.5 * splash['r-i'] < splash['g-r'] - 0.80

    else:
        raise  ValueError('dband of {} is not supported; try [u, g].'.format(dband))
    
    return  isin  

# grush      = get_goldrush()

splash, Area = get_splash()
splash_zspec = splash[splash['ZSPEC'] > 0.]

sxdrops      = splash_drops(dband='BX')
sudrops      = splash_drops(dband='u')
sgdrops      = splash_drops(dband='g')

sadrops      = sxdrops | sudrops | sgdrops

sxdrops      = splash[sxdrops]
sudrops      = splash[sudrops]
sgdrops      = splash[sgdrops]

sadrops      = splash[sadrops]

##
fig, axes    = plt.subplots(1, 3, figsize=(15, 3)) 

axes[0].scatter(sxdrops['g-r'], sxdrops['u-g'], c=sxdrops['MAG_ISO_hsc_i'], lw=0.0, s=2, vmin=22., vmax=26., marker='.')

axes[0].set_xlabel('$g-r$')
axes[0].set_ylabel('$u-g$')

axes[0].set_xlim(-1.5, 4.)
axes[0].set_ylim(-1.5, 4.)

im        = axes[1].scatter(sudrops['g-r'], sudrops['u-g'], c=sudrops['MAG_ISO_hsc_i'], lw=0.0, s=2, vmin=22., vmax=26., marker='.')

axes[1].set_xlabel('$g-r$')
axes[1].set_ylabel('$u-g$')

axes[1].set_xlim(-1.5, 4.)
axes[1].set_ylim(-1.5, 4.)

axes[2].scatter(sgdrops['r-i'], sgdrops['g-r'], c=sgdrops['MAG_ISO_hsc_i'], lw=0.0, s=2, vmin=22., vmax=26., marker='.')

axes[2].set_xlabel('$r-i$')
axes[2].set_ylabel('$g-r$')

axes[2].set_xlim(-1.5, 4.)
axes[2].set_ylim(-1.5, 4.)           

cax = fig.add_axes([0.415, 0.2, 0.2, 0.05])
fig.colorbar(im, cax=cax, orientation='horizontal')

# fig.suptitle('Splash BX, $u$ & $g$ dropouts')

pl.savefig('colors.pdf', rasterized=True)

pl.clf()


## -- Redshift Distribution.
dz         = 0.1
bins       = np.arange(0.0, 4.5, dz) 

fig, ax    = plt.subplots(1, 1, figsize=(5,5)) 

for sample, label, color in zip([sxdrops['ZPHOT'], sudrops['ZPHOT'], sgdrops['ZPHOT']], ['BX', '$u$', '$g$'], ['y', 'b', 'g']):
  cnts, lo = np.histogram(sample, bins=bins)
  mid      = lo + 0.5 * dz

  cnts     = cnts / Area
  
  ax.bar(mid[:-1], cnts, alpha=0.5, color=color, label=label, width=dz) 

ax.set_xlim(0.0, 4.5)

ax.set_xlabel('$z$')
ax.set_ylabel('$dN$ / sq. deg. / $\Delta z = 0.1$')

ax.legend(frameon=False)

ax.set_title(r'SPLASH photo-$z$')

pl.savefig('Nz.pdf', rasterized=True)

## -- Magnitude distribution.
