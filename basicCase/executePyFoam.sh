# Run openfoam case with PyFoam
echo "Running case with parameters $name.parameters"
pyFoamPlotRunner.py --clear --progress --with-courant --no-continuity  --hardcopy mpirun -np 16 pimpleFoam -parallel
