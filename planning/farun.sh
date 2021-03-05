export PRIMINFO=/global/cscratch1/sd/mjwilson/secondary/sv1/outdata/0.50.0/priminfo-dr9-0.50.0/

# --scnd /global/cscratch1/sd/mjwilson/dr9/0.50.0.dev4501/targets/sv1/secondary/dark/
# fba_sv1  --dr dr9 --dtver 0.50.0 --rundate 2020-01-01T00:00:00 --tilera 150.12  --tiledec 2.20  --tileid 82000  --faflavor sv1scndcosmos  --priority custom --outdir $CSCRATCH/SCNDCOSMOS

fba_sv1 --dr dr9 --dtver 0.50.0 --rundate 2020-01-01T00:00:00 --tilera 150.12  --tiledec 2.20  --tileid 82000  --faflavor sv1scndcosmos  --priority custom --outdir $CSCRATCH/SCNDCOSMOS --scnd /global/cscratch1/sd/mjwilson/dr9/0.50.0/targets/sv1/secondary/dark/
