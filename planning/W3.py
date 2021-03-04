import os
import astropy.io.fits as fits

scr = os.environ['CSCRATCH']

dat = fits.open(scr + '/GOLDRUSH/goldrush_mizukizs.fits')[1].data

inra  = (dat['ra'] > 212.8) & (dat['ra'] < 215.67)
indec = (dat['dec'] > 51.66) & (dat['dec'] < 53.28)

dat = dat[inra]


