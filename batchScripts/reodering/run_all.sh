#!/bin/bash

DIR=$1
OUT=$2

cd ../../

mkdir out
mkdir out/$OUT


cd ./batchScripts/reodering

other_order=( true false )
generics_first=( true false )

for oo in "${other_order[@]}";
do
    for gf in "${generics_first[@]}";
    do

        cat $DIR | while read filename || [ -n "$filename" ]; do sbatch ./run_single.sh "${oo}_${gf}_${filename}" $OUT $oo $gf; done 
    done
done

# Additional commands or post-processing can go here
exit
