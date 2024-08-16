# Finetune Mistral 7B v0.3 German News Titles Scripts

This repository contains the finetune and dataset generation scripts for the german news titles finetune project.


## Setup

```bash
python3.11 -m venv venv
. venv/bin/activate
pip install -r requirements.txt 
```

## Dataset

* [german-news-titles](https://huggingface.co/datasets/Jotschi/german-news-titles)

## Dataset generation

The `dataset` scripts generate the entries using Ollama and `dolphin-mixtral:v2.7`.

## Models

* [Mistral-7B-v0.1_german-news-titles-v1](https://huggingface.co/Jotschi/Mistral-7B-v0.1_german-news-titles-v1)

## Model training

```bash
./train.sh
```

## Test PEFT

This script loads the PEFT checkpoint and the basemodel. It invokes inferences for a set of titles with different word length variations.

```bash
./test-peft.sh results/checkpoint-100/
```

## Merge PEFT

Once a good checkpoint has been generated the `merge-peft.sh` script can be used to merge the PEFT adapter with the basemodel to generate the final finetuned model.

```bash
./merge-peft.sh  results/checkpoint-100/ dummy
```

# Test via vLLM

Afterwards  the vLLM inference server container can be used to load the final model and test whether the merge was successful.

```bash
# Start vLLM
./start-vllm.sh models/dummy/

# Run inference
./test-vllm.sh dummy
```

