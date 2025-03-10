#! /bin/sh

## ------ engine:jinja2 ---------

echo "Setting $case field and boundary conditions."

	python initializeCaseFieldBC.py temporal default
	funkySetFields -time 0
	
 
