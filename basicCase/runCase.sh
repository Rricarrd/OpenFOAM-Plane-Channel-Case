#!/bin/sh

# If parameter name is available, use it. Otherwise use default.
if [ -z "$1" ]; then
    name="default"
else
    name="$1"
fi

# Clearing case
bash ./clearCase.sh

# Perpare openfoam case with PyFoam
echo "Preparing case with parameters $name.parameters"
pyFoamPrepareCase.py . --parameter-file="$name.parameters"


# Run openfoam case with PyFoam
echo "Running case with parameters $name.parameters"
pyFoamPlotRunner.py --clear --progress --with-courant --with-iterations --hardcopy --autosense-parallel  pisoFoam

# Reconstructing
echo "Reconstructing data and generating mesh center files"
reconstructPar
postProcess -func writeCellCentres


# Plotting
echo "Postprocessing and plotting"
mkdir -p ./plots
python ./plot.py
