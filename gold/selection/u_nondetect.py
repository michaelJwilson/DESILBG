import numpy as np


def u_nondetect(clauds):
    '''
    u-drop color selection.
    '''

    # 'Detection' band. 
    band='r'
    magmin=20.0
    maglim=24.5
    
    # Check these targets have u band imaging available. 
    assert  np.all(clauds['FLAG_FIELD_BINARY'][:,1] == True)

    # Non-detected in u: u ~-99.
    isin = clauds['u'] < -40.

    # SNR cuts in g and r.
    isin = clauds['g_err'] <= 0.1
    isin = clauds['r_err'] <= 0.2

    # Same as u drops.
    isin = clauds['g'] - clauds['r'] < 1.2
    
    isin = isin & (clauds[band] < maglim)
    isin = isin & (clauds[band] > magmin)
        
    return  isin


