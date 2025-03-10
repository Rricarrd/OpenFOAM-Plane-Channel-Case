#!/bin/sh

# If parameter name is available, use it. Otherwise use default.
if [ -z "$1" ]; then
    name="default"
else
    name="$1"
fi

# Perpare openfoam case with PyFoam
echo "Preparing case with parameters $name.parameters"
pyFoamPrepareCase.py . --parameter-file="$name.parameters"


# Run openfoam case with PyFoam
echo "Running case with parameters $name.parameters"
pyFoamPlotRunner.py --clear --progress --autosense-parallel  pisoFoam
