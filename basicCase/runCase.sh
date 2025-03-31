#!/bin/sh

# If parameter name is available, use it. Otherwise use default.
if [ -z "$1" ]; then
    name="default"
else
    name="$1"
fi

# Check for all argument
if [[ " $@ " == *" -all "* ]]; then
    # Remove other files
    echo "Doing some tests"
fi


# Clearing case
bash ./clearCase.sh

# Perpare openfoam case with PyFoam
echo "Preparing case with parameters $name.parameters"
pyFoamPrepareCase.py . --parameter-file="$name.parameters"


# Executing PyFoam
bash ./executePyFoam.sh


# Reconstructing
echo "Reconstructing data and generating mesh center files"
reconstructPar
postProcess -func writeCellCentres


# Plotting
echo "Postprocessing and plotting"
mkdir -p ./plots
python ./plot.py
mv -f *.png plots/ # Move pyFoam plots to plots and overwrite them
