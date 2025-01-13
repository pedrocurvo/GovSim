#!/bin/bash

#SBATCH --partition=gpu_a100
#SBATCH --gpus=1
#SBATCH --job-name=Llamma3
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --time=20:00:00
#SBATCH --output=slurm_output_%A.out

module purge
module load 2023
module load Anaconda3/2023.07-2

source activate GovSim
cd $HOME/GovSim

srun python3 -m simulation.main experiment=fish_baseline_concurrent_universalization llm.path=meta-llama/Meta-Llama-3-8B-Instruct




