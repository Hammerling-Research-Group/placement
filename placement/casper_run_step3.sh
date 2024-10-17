#!/bin/bash 
#PBS -N run_gp
#PBS -A UCSM0014
#PBS -l select=1:ncpus=30:mem=200GB
#PBS -l walltime=11:59:00
#PBS -q casper
#PBS -j oe

export TMPDIR=${SCRATCH}/temp
mkdir -p ${TMPDIR}

### Activate fast Gaussian puff model environment
module load conda
conda activate gp

### Run program
python -u /glade/work/mjia/sensor-placement-optimization/code/demo/step3_simulate_concentrations.py
