import numpy as np

def datamodel(cat):
    cat = cat['RA', 'DEC']

    # Assumed 2015.5                                                                                                                                                                                                                         
    cat['PMRA'] = 0.0
    cat['PMDEC'] = 0.0

    cat['REF_EPOCH'] = np.array([0.0] * len(cat), dtype='>f4')
    cat['OVERRIDE'] = True

    cat['RA']  = cat['RA'].data.astype('>f8')
    cat['DEC'] = cat['DEC'].data.astype('>f8')
    cat['PMRA'] = cat['PMRA'].data.astype('>f4')
    cat['PMDEC'] = cat['PMDEC'].data.astype('>f4')

    return cat
