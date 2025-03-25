#!/bin/sh

# Check if a name is provided as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <name>"
  exit 1
fi

name="$1"

# Count files starting with a number in the current directory
count=$(find . -maxdepth 1 -type d -regex "./[0-9].*" | wc -l)

# Append the count to the beginning of the name
path="./$count$name"

echo "Basic case cloned in: $path"
pyFoamCloneCase.py ./basicCase $path


echo "Copying case generation script"
cp ./basicCase/initializeCaseFieldBC.py $path

echo "Copying the plotting"
cp ./basicCase/plot.py $path

echo "Copying paraFoam state"
cp ./basicCase/paraview_test_state.pvsm $path


echo "Copying also 0.orig"
cp -r ./basicCase/0.orig $path


exit 0
