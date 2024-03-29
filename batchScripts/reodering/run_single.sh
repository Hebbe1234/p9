#!/bin/bash
#SBATCH --time=00:01:00
#SBATCH --mail-user=rhebsg19@student.aau.dk
#SBATCH --mail-type=FAIL
#SBATCH --partition=dhabi
#SBATCH --mem=10G
#SBATCH --output=/nfs/home/student.aau.dk/rhebsg19/slurm-output/reordering/reordering-%A_%a.out  # Redirect the output stream to this file (%A_%a is the job's array-id and index)
#SBATCH --error=/nfs/home/student.aau.dk/rhebsg19/slurm-output/reordering/reordering-%A_%a.err   # Redirect the error stream to this file (%A_%a is the job's array-id and index)


let "m=1024*1024*10"
ulimit -v $m

FILENAME=$1
OUTPUT=$2
GROUP_BY_EDGE_ORDER=$3
INTERLEAVE_LAMBDA_BINARY_VARS=$4
GENERICS_FIRST=$5
PREFIX=$6
SPLIT=$7
NUM_SPLITS=$8
TIMEOUT=$9
EXPERIMENT=${10}

cd ../../src



# Create and activate a virtual environment
source bdd_venv/bin/activate
output_file="../out/$OUTPUT/${SLURM_ARRAY_TASK_ID}_${PREFIX}_${FILENAME}.txt"
# Run your Python script
echo $TASK_ID > $output_file

MYCMD="python3 -u reordering.py --filename=$FILENAME --experiment=${EXPERIMENT} --group_by_edge_order=${GROUP_BY_EDGE_ORDER} --interleave_lambda_binary_vars=${INTERLEAVE_LAMBDA_BINARY_VARS} --generics_first=${GENERICS_FIRST} --split=${SPLIT} --num_splits=${NUM_SPLITS} --index ${SLURM_ARRAY_TASK_ID} --timeout=${TIMEOUT} >> ${output_file}"
CMD="timeout ${TIMEOUT} /usr/bin/time -f \"@@@%e,%M@@@\" ${MYCMD} >> ${output_file}"
echo "${FILENAME}; ${GROUP_BY_EDGE_ORDER}; ${INTERLEAVE_LAMBDA_BINARY_VARS};${GENERICS_FIRST}; ${SPLIT}; ${SLURM_ARRAY_TASK_ID}"  # Log command to slurm output file.
echo "${CMD}"  # Log command to slurm output file.
eval "${CMD}"  # Run the command

 
# Deactivate the virtual environment
deactivate
# Additional commands or post-processing can go here
exit
