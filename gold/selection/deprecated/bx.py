import numpy as np

from .udrops import udrops

def bx(cat):
    '''
    bx color selection.
    '''
    
    rmin=22.5
    rmax=24.5

    # Check these targets have u band imaging available.                                                                                                                                                 
    assert  np.all(cat['FLAG_FIELD_BINARY'][:,1] == True)
    
    # https://arxiv.org/pdf/0903.3951.pdf
    isin = np.ones(len(cat), dtype=bool)

    umg = cat['u'] - cat['g']
    gmr = cat['g'] - cat['r']
    
    # LATIS, https://arxiv.org/pdf/2002.10676.pdf
    isin &= (umg >  0.0)
    isin &= (umg <  3.0)
    isin &= (gmr > -0.5)
    isin &= (gmr <  1.2)
    isin &= (umg >  1.0 + 2.3 * (gmr - 0.35))

    isin = isin & (cat['r'] > rmin)
    isin = isin & (cat['r'] < rmax)
    
    # Not a u dropout.
    isin = isin & (~udrops(cat))

    # Catch -99 for ill defined magnitudes. **  Deal with u non-detections independently **.
    isin = isin & (cat['u'] > 0.0)
    isin = isin & (cat['g'] > 0.0)
    isin = isin & (cat['r'] > 0.0)
    
    # SNR cuts in g and r.                                                                                                                                                                                                                  
    isin = isin & (cat['g_err'] <= 0.1)
    isin = isin & (cat['r_err'] <= 0.2)
    
    return  isin