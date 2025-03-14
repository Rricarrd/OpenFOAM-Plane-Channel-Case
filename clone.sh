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


echo "Copying also case generation script"
cp ./basicCase/initializeCaseFieldBC.py $path

echo "Copying also the plotting"
cp ./basicCase/initializeCaseFieldBCplotting.py $path

echo "Copying also 0.orig"
cp -r ./basicCase/0.orig $path


exit 0
