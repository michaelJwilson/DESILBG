import glob
import pandas as pd

from astropy.table import Table, vstack

root  = '/global/cscratch1/sd/mjwilson/DESILBG/Feb21/targets/' 
cat   = None

# Keep restricted column list. 
cols  = pd.read_csv('cols.txt', names=['names']).names
cols  = cols.tolist()

for tracer in ['bxdrops', 'udrops', 'gdrops']:
    print('Solving for {}.'.format(tracer))
    
    files = glob.glob(root + '/{}/*.fits'.format(tracer))

    print('{} files to be collected.'.format(len(files)))
    
    for f in files:
        if cat is None:
            cat = Table.read(f)[cols]

        else:
            cat = vstack((cat, Table.read(f)[cols])) 
            
print('Collected {}M LBGLAE targets.'.format(len(cat) / 1.e6))

cat.sort('PRIORITY')

opath = '{}/desi_lbg.fits'.format(root)

print('Writing to {}.'.format(opath))

cat.pprint()

cat.write(opath, format='fits', overwrite=True)
