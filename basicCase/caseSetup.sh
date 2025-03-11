#! /bin/sh

## ------ engine:jinja2 ---------

echo "Setting $case field and boundary conditions."
 
	# Generate initial spatial K-waves for the whole simulation
	python initializeCaseFieldBC.py spatial default
	
	# Set initial field to a parabolic profile using funkySetFields
	funkySetFields -time 0
	
 
