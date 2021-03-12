export DUST_DIR=/global/cfs/cdirs/cosmo/data/dust/v0_1
export MASK_DIR=/global/cfs/cdirs/desi/target/masks
export GAIA_DIR=/global/cfs/cdirs/desi/target/gaia_dr2
export URAT_DIR=/global/cfs/cdirs/desi/target/urat_dr1
export TYCHO_DIR=/global/cfs/cdirs/desi/target/tycho_dr2
# export TOO_DIR=/global/cfs/cdirs/desi/target/ToO

export PRIMINFO=/global/cscratch1/sd/mjwilson/DESILBG/GOLD/secondary/sv1/outdata/0.51.0/priminfo-dr9-0.51.0/

# desienv master
# addrepo ../desitarget (tag 0.51.0)

# rm -r $CSCRATCH/secondary/sv1/outdata/...

# select_sv_targets sweepdir dest
# srun -N 1 select_sv_targets /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/south/sweep/9.0 /global/cscratch1/sd/mjwilson/DESILBG/GOLD/secondary/sv1/outdata/ -s2 /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/north/sweep/9.0 --nside 8 --healpixels 425 --numproc 4 --scnddir /global/cscratch1/sd/mjwilson/DESILBG/GOLD/secondary/

# srun -N 1 select_sv_targets /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/south/sweep/9.0 /global/cscratch1/sd/mjwilson/DESILBG/GOLD/secondary/sv1/outdata/ -s2 /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/north/sweep/9.0 --nside 8 --healpixels 427 --numproc 4 --scnddir /global/cscratch1/sd/mjwilson/DESILBG/GOLD/secondary/  

select_secondary $PRIMINFO /global/cscratch1/sd/mjwilson/DESILBG/GOLD/secondary/sv1/outdata/ --scnddir /global/cscratch1/sd/mjwilson/DESILBG/GOLD/secondary/ 

