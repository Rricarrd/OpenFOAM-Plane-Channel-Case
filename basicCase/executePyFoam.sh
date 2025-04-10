# Run openfoam case with PyFoam
echo "Running case with parameters $name.parameters"

mpirun -np 16 pimpleFoam -parallel > log.pimpleFoam &

pyFoamPlotWatcher.py log.pimpleFoam
