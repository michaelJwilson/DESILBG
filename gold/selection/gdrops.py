import numpy as np


def gdrops(cat):
    '''
    g dropout selection. 
    '''
    
    # Check these targets have hsc imaging available.                                                                                                                                                                                     
    assert  np.all(cat['FLAG_FIELD_BINARY'][:,0] == True)

    imin=22.5
    imax=25.5
    
    # https://arxiv.org/pdf/0903.3951.pdf    
    isin=np.ones(len(cat), dtype=bool)

    rmi = cat['r'] - cat['i']
    gmr = cat['g'] - cat['r']

    # https://arxiv.org/pdf/1704.06004.pdf
    isin &= gmr >  1.0
    isin &= rmi <  1.0
    isin &= rmi > -1.5
    isin &= gmr >  1.5 * rmi + 0.8
    
    isin  = isin & (cat['i'] > imin)
    isin  = isin & (cat['i'] < imax)
    
    # Catch -99 for ill defined magnitudes. ** Deal with non detects independently.**
    isin = isin & (cat['g'] > 0.0)
    isin = isin & (cat['r'] > 0.0)
    isin = isin & (cat['i'] > 0.0)

    # SNR cuts in r and i.                                                                                                                                                                                                                  
    isin = isin & (cat['r_err'] <= 0.1)
    isin = isin & (cat['i_err'] <= 0.2)
            
    return  isin
