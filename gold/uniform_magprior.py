import numpy as np

from   astropy.table import Table, vstack

npertranche = 200

def uniform_magpriority(band, magmin, magmax, cat):
    # Do not sort in mag.     
    bins = np.arange(magmin, magmax, 0.25)

    # bins[i-1] <= x < bins[i].
    prioritized_cat = None

    todo = np.ones(len(cat), dtype=bool)
    idx  = np.digitize(cat[band], bins, right=False)
    cat['IDX'] = idx

    print('\n\n---- To do summary ----')  
    print(np.unique(cat['IDX'], return_counts=True))
    
    ndone = 0
    warnings = 0
    
    while np.count_nonzero(todo) > 0:        
      for i in range(1 + len(bins)):          
          inbin  = todo & (idx == i)

          # Nothing to do.
          if (np.count_nonzero(inbin) == 0):
              continue
          
          ss     = np.cumsum(inbin) 
          
          subcat = cat[inbin]

          nrow   = np.minimum(len(subcat), npertranche)          

          subcat = subcat[:nrow]          

          subcat.pprint()
          
          if prioritized_cat == None:
              prioritized_cat = subcat

          else:
              prioritized_cat = vstack((prioritized_cat, subcat))

          done = inbin & (ss <= npertranche)

          todo = todo & (~done)

          if np.count_nonzero(todo==False) == ndone:
              warnings += 1

              # print('You have been warned.')
              
              if warnings > 5:
                  raise RuntimeError('Too many warnings.')
          
          # print('Total: {};  Remaining: {}'.format(len(todo), np.count_nonzero(todo==True)))

          ndone = np.count_nonzero(todo==False)
          
          # cat[todo].pprint()

          # print('\n\n---- To do summary ----')
          # print(np.unique(cat[todo]['IDX'], return_counts=True))
          
    print('Done.')
    print('\n\n')

    # Unique
    assert np.all(np.unique(prioritized_cat['ID']) == np.sort(prioritized_cat['ID']))
    
    # Nothing lost.
    assert np.all(np.unique(prioritized_cat['ID']) == np.unique(cat['ID']))
    
    prioritized_cat.pprint()

    # del cat['IDX']

    return prioritized_cat


if __name__ == '__main__':
    import pylab as pl

    
    dat = Table.read('/global/cscratch1/sd/mjwilson/DESILBG/GOLD/G/g.fits')
    dat.pprint()

    dat = uniform_magpriority('i', 20.0, 25.5, dat)

    dat.pprint()
    
    idx = 1 + np.arange(len(dat))

    pl.scatter(idx, dat['i'], c=dat['IDX'], marker='.', lw=0.0, s=5)
    pl.xlabel('ROW (PRIORITY)')
    pl.ylabel('i')    
    pl.xlim(0.9, 25000)
    pl.xscale('log')
    pl.colorbar()
    pl.show()
    
