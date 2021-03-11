import numpy as np

from astropy.table import Table

def snr(cat, band):
    return 2.5 / np.log(10.) / cat['{}_err'.format(band)].data


if __name__ == '__main__':
    mag_errs = np.arange(0.1, 1.0, 0.1)

    cat = Table()

    cat['u_err'] = mag_errs
    
    snrs = snr(cat, 'u')

    print(snrs)
