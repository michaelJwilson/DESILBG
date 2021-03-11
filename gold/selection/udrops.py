import numpy as np


def udrops(clauds):
    '''
    u-drop color selection.
    '''

    # 'Detection' band. 
    band='r'
    magmin=22.5
    maglim=24.5
    
    # Check these targets have u band imaging available. 
    assert  np.all(clauds['FLAG_FIELD_BINARY'][:,1] == True)
    
    isin = clauds['g'] - clauds['r'] < 1.2
    isin = isin & (clauds['g'] - clauds['r'] > -0.5)

    isin = isin & (clauds['u'] - clauds['g'] > 0.88)
    isin = isin & (clauds['u'] - clauds['g'] > 1.99 * (clauds['g'] - clauds['r']) + 0.68)

    isin = isin & (clauds[band] < maglim)
    isin = isin & (clauds[band] > magmin)
    
    # Catch -99 for ill defined magnitudes. ** Deal with non-detections independently. ** 
    isin = isin & (clauds['u'] > 0.0)
    isin = isin & (clauds['g'] > 0.0)
    isin = isin & (clauds['r'] > 0.0)
    
    # SNR cuts in g and r.                                                                                                                                                                                                                  
    isin = isin & (clauds['g_err'] <= 0.1)
    isin = isin & (clauds['r_err'] <= 0.2)
    
    return  isin
