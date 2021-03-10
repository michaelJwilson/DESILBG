import numpy as np

def g_nondetect(clauds):
    '''
    ug non detections. 
    '''

    # 'Detection' band. 
    band='i'
    magmin=20.0
    maglim=25.5

    # Check these targets have g available.
    assert  np.all(clauds['FLAG_FIELD_BINARY'][:,0] == True)

    # Non-detected in u and g: u ~-99.
    isin = (clauds['u'] < -40.)
    isin = isin & (clauds['g'] < -40.)

    isin = isin & (clauds['r'] > 0.0)
    isin = isin & (clauds['i'] > 0.0)
    
    # SNR cuts in g and r.
    isin = isin & (clauds['r_err'] <= 0.1)
    isin = isin & (clauds['i_err'] <= 0.2)

    # same as g drops. 
    isin = isin & (clauds['r'] - clauds['i'] < 1.0)
    
    isin = isin & (clauds[band] < maglim)
    isin = isin & (clauds[band] > magmin)
    
    return  isin


