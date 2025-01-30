models = {
    "Llama-3-8B": "meta-llama/Meta-Llama-3-8B-Instruct",
    #"Llama-3-70B": "meta-llama/Meta-Llama-3-70B-Instruct",
    "Llama-2-7B": "meta-llama/Llama-2-7b-chat-hf",
    "Llama-2-13B": "meta-llama/Llama-2-13b-chat-hf",
    "Mistral-7B": "mistralai/Mistral-7B-Instruct-v0.2",
    "Qwen2.5-0.5B": "Qwen/Qwen2.5-0.5B-Instruct",
    "Qwen2.5-7B": "Qwen/Qwen2.5-7B-Instruct"
}

script_template = """#!/bin/bash

#SBATCH --partition=gpu_h100
#SBATCH --gpus=1
#SBATCH --job-name={job_name}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --time=05:00:00
#SBATCH --output=slurm_output_%A.out

module purge
module load 2023
module load Anaconda3/2023.07-2

source activate GovComGPTQ
cd $HOME/GovSim

srun python3 -m simulation.main experiment={experiment} llm.path={llm_path} seed={seed} group_name={job_name}
"""

from pathlib import Path

Path("scripts").mkdir(exist_ok=True, parents=True)

for model, path in models.items():
    for seed in [0, 21, 42]:
        for experiment in ["fish_baseline_concurrent_universalization", "fish_baseline_concurrent", "fish_baseline_japanese", "trash_baseline_concurrent"]:
            Path(f"scripts/{experiment}_{seed}").mkdir(exist_ok=True, parents=True)
            filename = f"scripts/{experiment}_{seed}/run_{model.replace('-', '').replace('.', '')}_{seed}_{experiment}.sh"
            with open(filename, "w") as f:
                f.write(script_template.format(job_name=model, llm_path=path, seed=seed, experiment=experiment))
            print(f"Generated {filename}")