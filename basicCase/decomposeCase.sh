#! /bin/sh
## ------ engine:jinja2 ---------

echo "Preparing files for decomposePar"
{% if numberOfProcessors>1 %}

	echo "Removing templates from 0"
	rm 0/*.template

	# echo "Copying .finalTemplates into 0.tmp"
	# mkdir 0.tmp
	# mv 0/*.finalTemplate 0.tmp
	
	decomposePar
	
	# echo "Copying 0.tmp back into each processor folder"
	# {% for p in range(numberOfProcessors) %}
	# 	cp 0.tmp/* processor{{p}}/0/
	# {% endfor %}

	# echo "Deleting 0.tmp"
	# rm -r 0.tmp
	
{% endif %}

