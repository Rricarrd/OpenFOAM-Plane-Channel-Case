#! /bin/sh

## ------ engine:jinja2 ---------

echo "Setting $case field and boundary conditions."
 
	funkySetFields -time 0
	python initializeCaseFieldBC.py temporal -parameters_file default
	
 


echo "Preparing files for decomposePar"


	echo "Hiding 0.org inside 0"
	cp -r 0.orig 0
	rm 0/*.template

	echo "Copying .finalTemplates into 0.tmp"
	mkdir 0.tmp
	mv 0/*.finalTemplate 0.tmp
	
	pyFoamDecompose.py . 16 
	
	echo "Copying 0.tmp back into each processor folder"
	
		cp 0.tmp/* processor0/0/
	
		cp 0.tmp/* processor1/0/
	
		cp 0.tmp/* processor2/0/
	
		cp 0.tmp/* processor3/0/
	
		cp 0.tmp/* processor4/0/
	
		cp 0.tmp/* processor5/0/
	
		cp 0.tmp/* processor6/0/
	
		cp 0.tmp/* processor7/0/
	
		cp 0.tmp/* processor8/0/
	
		cp 0.tmp/* processor9/0/
	
		cp 0.tmp/* processor10/0/
	
		cp 0.tmp/* processor11/0/
	
		cp 0.tmp/* processor12/0/
	
		cp 0.tmp/* processor13/0/
	
		cp 0.tmp/* processor14/0/
	
		cp 0.tmp/* processor15/0/
	

	echo "Deleting 0.tmp"
	rm -r 0.tmp
	

