#!/bin/bash

#SBATCH -J quant_trait_BD_sim # job name
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=4-00:00:00  # time (D-HH:MM:SS). 0 should mean no limit.
#SBATCH --mail-user=ananda.bhat@students.iiserpune.ac.in #mail when scripts have run
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT #send emails when job begins and ends, and also send if it fails or times out
#SBATCH --output=/home/shikharabhat/MS_thesis/slurm_messages/model_run_%A_%a.out # output file
#SBATCH --error=/home/shikharabhat/MS_thesis/slurm_messages/model_error_%A_%a.error #error file 
#SBATCH --array=1-11
    
module load python/3.6

START=$SLURM_ARRAY_TASK_ID
NUMLINES=2 #number of parameter values to run in each job
STOP=$((SLURM_ARRAY_TASK_ID*NUMLINES))
START="$(($STOP - $(($NUMLINES - 1))))"

echo "START=$START"

for (( N = $START; N <= $STOP; N++ ))
do
    K=$(sed -n "$N"p /scratch/shikharabhat/MS_thesis/BD_params/K.txt)
    echo This is SLURM task $SLURM_ARRAY_TASK_ID
    echo "K=" $K
    python3 main.py -K $K
done

echo "STOP=$STOP"
