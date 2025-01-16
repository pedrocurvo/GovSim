# GovSim: Governance of the Commons Simulation


![GovSim overview](imgs/govsim_pull_figure.png)

<p align="left">Fig 1: Illustration of the GOVSIM benchmark. AI agents engage in three resource-sharing scenarios: fishery, pasture, and pollution. The outcomes are cooperation (2 out of 45 instances) or collapse (43 out of 45 instances), based on 3 scenarios and 15 LLMs.
</p>

This repository accompanies our research paper titled "**Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents**" 

#### Our paper:

"**[Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents](https://arxiv.org/abs/2404.16698)**" by *Giorgio Piatti\*, Zhijing Jin\*, Max Kleiman-Weiner\*, Bernhard Schölkopf, Mrinmaya Sachan, Rada Mihalcea*.

**Citation:**

```bibTeX
@misc{piatti2024cooperate,
      title={Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents}, 
      author={Giorgio Piatti and Zhijing Jin and Max Kleiman-Weiner and Bernhard Schölkopf and Mrinmaya Sachan and Rada Mihalcea},
      year={2024},
      eprint={2404.16698},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```



## **Simulation**

Each experiment in GovSim is defined using a **Hydra configuration**. Follow these steps to run an experiment:

### **Basic Command**
To execute an experiment, use the following command:  
```bash
python3 -m simulation.main experiment=<scenario_name>_<experiment_name>
```

**Example**

To run the experiment fish_baseline_concurrent:

```
python3 -m simulation.main experiment=fish_baseline_concurrent
```

### **General Command Structure**

For more flexibility, you can specify the language model (LLM):

```
python3 -m simulation.main experiment=<experiment_id> llm.path=<path_to_llm>
```

where `<experiment_id>` is the experiment name and `<path_to_llm>` is the API model name or the Hugging Face model name. Some models might require changes to the ```pathfinder``` library, which is used for finding the correct model path.

**Example**

To run the experiment fish_baseline_concurrent with meta-llama/Llama-2-7b-chat-hf:

```
python3 -m simulation.main experiment=fish_baseline_concurrent llm.path=meta-llama/Llama-2-7b-chat-hf
```

### For API-based models (e.g., OpenAI, Anthropic):

1. Rename the .env_example file to .env, since .env is in the .gitignore file because it contains sensitive information and should not be pushed to the repository.
2.	Add your API keys to the .env file.
3.	Run the following command:

```
python3 -m simulation.main experiment=<experiment_id> llm.path=<path_to_llm> llm.is_api=true
```
**Example**

To run the experiment fish_baseline_concurrent with gpt-4-turbo-2024-04-09:

```
python3 -m simulation.main experiment=fish_baseline_concurrent llm.path=gpt-4-turbo-2024-04-09 llm.is_api=true
```

### For MultiGov Experiences:

To run the MultiGov experiments, you can use the following command:

```
python3 -m simulation.main \
    llm.path="[model1, model2, model3, model4, model5]" \
    llm.is_api="[bool, bool, bool, bool, bool]" \
    llm.backend="[transformers, transformers, transformers, transformers, transformers]" \
    experiment=<experiment_id> \
    multigov=true
```

**Example**

```
python3 -m simulation.main \
    llm.path="[deepseek-chat, deepseek-chat, deepseek-chat, deepseek-chat, gpt-4o-mini-2024-07-18]" \
    llm.is_api="[true, true, true, true, true]" \
    llm.backend="[transformers, transformers, transformers, transformers, transformers]" \
    experiment=fish_baseline_concurrent \
    multigov=true
```

### For Hugging Face models:

If you are running the `transformers` library, first you need to login in the Hugging Face API by running `huggingface-cli login`. To see more options of Hugging Face API, please refer to the [Hugging Face API documentation](https://huggingface.co/docs/huggingface_hub/en/guides/cli).
After that, you can run the commands above, but you might need to first accept the model conditions
in your Hugging Face account.

### Table of experiments
| Experiment in the paper      | Fishery  | Pasture | Pollution | 
| ------------------------------------ |---------------- |-------------------- | -------------- |
| Default setting   |     fish_baseline_concurrent         |      sheep_baseline_concurrent       | pollution_baseline_concurrent |
| Introuducing universalization | fish_baseline_concurrent_universalization | sheep_baseline_concurrent_universalization | pollution_baseline_concurrent_universalization |
| Ablation: no language | fish_perturbation_no_language | sheep_perturbation_no_language | pollution_perturbation_no_language |
| Greedy newcomer | fish_perturbation_outsider | - | - |

## Subskills

To run the subskill evaluation, use the following command:

```
python3 -m subskills.<scenario_name> llm.path=<path_to_llm>
```

## Supported LLMs
In principle, any LLM model can be used. We tested the following models:

*APIs:*
- OpenAI: `gpt-4-turbo-2024-04-09`, `gpt-3.5-turbo-0125`, `gpt-4o-2024-05-13`
- Anthropic: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`

*Open-weights models:*
- Mistral: `mistralai/Mistral-7B-Instruct-v0.2`, `mistralai/Mixtral-8x7B-Instruct-v0.1`
- Llama-2: `meta-llama/Llama-2-7b-chat-hf`, `meta-llama/Llama-2-13b-chat-hf`, `meta-llama/Llama-2-70b-chat-hf`
- Llama-3: `meta-llama/Meta-Llama-3-8B-Instruct`, `meta-llama/Meta-Llama-3-70B-Instruct`
- Qwen-1.5: `Qwen/Qwen1.5-72B-Chat-GPTQ-Int4`, `Qwen/Qwen1.5-110B-Chat-GPTQ-Int4`


For inference we use the `pathfinder` library. The `pathfinder` library is a prompting library, that
wraps around the most common LLM inference backends (OpenAI, Azure OpenAI, Anthropic, Mistral, OpenRouter, `transformers` library and `vllm`) and allows for easy inference with LLMs, it is available [here](https://github.com/giorgiopiatti/pathfinder). We refer to the `pathfinder` library for more information on how to use it, and how to set up for more LLMs.



## Code Setup
To use the codes in this repo, first clone this repo:
    

    git clone --recurse-submodules https://github.com/giorgiopiatti/GovSim.git
    cd govsim

Then, to install the dependencies, run the following command if you want to use the `transformers` library only.
    
```setup
bash ./setup.sh
```

or if you want to use the `vllm` library, run the following command:

```setup
bash ./setup_vllm.sh
```

Both setups scripts require conda to be installed. If you do not have conda installed, you can install it by following the instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

### Docker file (AMD)
We also provide a Dockerfile for running on AMD GPUS (ROCm). We do not offer support for this Dockerfile, but it can be used as a reference for running on AMD GPUs.

```bash
docker build -t govsim -f ./govsim-rocm.dockerfile . 
```


