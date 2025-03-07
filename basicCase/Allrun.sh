#!/bin/sh

pyFoamPrepareCase.py . --parameter-file=default.parameters

pyFoamPlotRunner.py --clear --progress --autosense-parallel  pisoFoam
