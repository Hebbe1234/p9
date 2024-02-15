#!/bin/bash

#SBATCH --mail-user=fhyldg18@student.aau.dk
#SBATCH --mail-type=FAIL
#SBATCH --partition=dhabi
#SBATCH --mem=3G

graph=$1
out=$2

case $graph in
	0.1)
		python3 AAU_create_json_and_make_pdfs.py --dirs $out --xaxis 0 --legend new
esac