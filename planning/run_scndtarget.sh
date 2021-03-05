export GAIA_DIR=/project/projectdirs/cosmo/data/gaia/dr2/

# export PRIMINFO=/global/cscratch1/sd/mjwilson/secondary/sv1/outdata/0.50.0.dev4501/priminfo-dr9-0.50.0.dev4501/
export PRIMINFO=/global/cscratch1/sd/mjwilson/secondary/sv1/outdata/0.50.0/priminfo-dr9-0.50.0/

export TOO_DIR=/global/cscratch1/sd/adamyers/ToO/dr9/0.50.0.dev4501/ToO/

# rm -r $CSCRATCH/secondary/sv1/outdata/0.50.0.dev4501/

# srun -N 1 select_sv_targets /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/south/sweep/9.0 $CSCRATCH -s2 /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/north/sweep/9.0 --nside 8 --healpixels 425 --numproc 4 --scnddir $CSCRATCH/secondary/
# srun -N 1 select_sv_targets /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/south/sweep/9.0 $CSCRATCH -s2 /global/cfs/cdirs/cosmo/data/legacysurvey/dr9/north/sweep/9.0 --nside 8 --healpixels 427 --numproc 4 --scnddir $CSCRATCH/secondary/

select_secondary $PRIMINFO $CSCRATCH --scnddir $CSCRATCH/secondary

