#!/bin/bash

#SBATCH --partition=gpu_a100
#SBATCH --gpus=1
#SBATCH --job-name=env
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=9
#SBATCH --time=04:00:00
#SBATCH --output=slurm_output_%A.out

module purge
module load 2023
module load Anaconda3/2023.07-2

cd $HOME/uvadlc_practicals_2024/
conda env create -n factinai
bash ./setup.sh
