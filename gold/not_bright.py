import numpy as np

def not_bright(clauds):
    isin = np.ones(len(clauds), dtype=bool)
    
    for band in ['u', 'g', 'r', 'i', 'z', 'y']:
        # Detected in this band.  Exclude -99.
        det = (clauds[band] > -40.)

        # Detected and mag < 17. 
        is_bright = det & (clauds[band] < 17.)

        isin[is_bright] = False

        print('Excluding {} bright source in {} [{:.2f}, {:.2f}].'.format(np.count_nonzero(is_bright), band, clauds[band][is_bright].min(), clauds[band][is_bright].max()))

        # More than this and we likely have a problem. 
        # assert  np.count_nonzero(is_bright) < 1000

    print('Excluding a total of {} bright source.'.format(np.count_nonzero(isin == False)))
        
    return  isin
