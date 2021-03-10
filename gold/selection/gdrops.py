import numpy as np


def gdrops(cat):
    # Check these targets have u band imaging available.                                                                                                                                                                                     
    assert  np.all(cat['FLAG_FIELD_BINARY'][:,0] == True)

    imin=20.0
    imax=25.5
    
    # https://arxiv.org/pdf/0903.3951.pdf    
    isin=np.ones(len(cat), dtype=bool)

    cat['rmi'] = cat['r'] - cat['i']
    cat['gmr'] = cat['g'] - cat['r']

    # https://arxiv.org/pdf/1704.06004.pdf
    isin &= cat['gmr'] >  1.0
    isin &= cat['rmi'] <  1.0    
    isin &= cat['gmr'] >  1.5 * cat['rmi'] + 0.8
    
    isin  = isin & (cat['i'] > imin)
    isin  = isin & (cat['i'] < imax)
    
    # Catch -99 for ill defined magnitudes
    isin = isin & (cat['g'] > 0.0)
    isin = isin & (cat['r'] > 0.0)
    isin = isin & (cat['i'] > 0.0)
    
    # Exclude where we have u imaging.
    # isin = isin & (cat['FLAG_FIELD_BINARY'][:,1] == False)
        
    return  isin
