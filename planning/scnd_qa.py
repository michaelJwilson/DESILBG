import numpy as np

from   astropy.table                 import Table
from   desitarget.sv1.sv1_targetmask import desi_mask, bgs_mask, mws_mask
from   desitarget.sv1.sv1_targetmask import scnd_mask

'''
scnd_mask.names()                                                                                                                                                                                                                      
['VETO',
 'UDG',
 'FIRST_MALS',
 'LBG_TOMOG',
 'QSO_RED',
 'M31_KNOWN',
 'M31_QSO',
 'M31_STAR',
 'MWS_CLUS_GAL_DEEP',
 'LOW_MASS_AGN',
 'FAINT_HPM',
 'GW190412',
 'IC134191',
 'PV_BRIGHT',
 'PV_DARK',
 'LOW_Z',
 'BHB',
 'SPCV',
 'DC3R2_GAMA',
 'UNWISE_BLUE',
 'UNWISE_GREEN',
 'HETDEX_MAIN',
 'HETDEX_HP',
 'HPM_SOUM',
 'SN_HOSTS',
 'GAL_CLUS_BCG',
 'GAL_CLUS_2ND',
 'GAL_CLUS_SAT',
 'HSC_HIZ_SNE',
 'ISM_CGM_QGP',
 'STRONG_LENS',
 'WISE_VAR_QSO',
 'MWS_CALIB',
 'BACKUP_CALIB',
 'MWS_MAIN_CLUSTER_SV',
 'MWS_RRLYR',
 'BRIGHT_HPM',
 'WD_BINARIES_BRIGHT',
 'WD_BINARIES_DARK']
'''
'''
These are the secondary programs for the Cosmos field, in order of priority:
==========================================================
- ISM_CGM_QGP
- HSC_HIZ_SNE
- LBG_TOMOG
- Hitherto not-bit-defined Clauds program (equal priority to LBG_TOMOG?)

These are the secondary programs for the CFHTLS-W3 field, in order of priority:
=============================================================
- HETDEX_HP
- HETDEX_MAIN  (this will need to be downsampled by a factor of 5x in desitarget before we run fiberassign)
- LBG_TOMOG
- Hitherto not-bit-defined Clauds program (equal priority to LBG_TOMOG?)
'''

# * full fiber reach on all petals.
# * LBG_TOMOG,ISM_CGM_QGP,HSC_HIZ_SNE from the secondary targets (priorities 4000, 4100, 4000, respectively)
# * Main QSOs as fillers.
# * 10 standard per petal + 20 sky per petal

desilbg  = Table.read('/global/cscratch1/sd/mjwilson/DESILBG/Feb21/targets/desi_lbg.fits')
dat      = Table.read('/global/cfs/cdirs/desi/target/catalogs/dr9/0.50.0/targets/sv1/secondary/dark/sv1targets-dark-secondary.fits')

for x in dat.dtype.names:
    print(x)

hizsne   = (dat['SV1_SCND_TARGET'] & scnd_mask['HSC_HIZ_SNE']) != 0 
tomog    = (dat['SV1_SCND_TARGET'] & scnd_mask['LBG_TOMOG'])   != 0 
ism      = (dat['SV1_SCND_TARGET'] & scnd_mask['ISM_CGM_QGP']) != 0

het_main = (dat['SV1_SCND_TARGET'] & scnd_mask['HETDEX_MAIN']) != 0
het_hp   = (dat['SV1_SCND_TARGET'] & scnd_mask['HETDEX_HP'])   != 0

for x in [ism , hizsne, tomog, het_hp, het_main]:
    print(np.count_nonzero(x))

tomog    = dat[tomog]
# tomog.pprint()

# np.count_nonzero(tomog['RA'].data == desilbg['RA'].data)
