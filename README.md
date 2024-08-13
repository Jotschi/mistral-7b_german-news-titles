# Finetune Mistral 7B v0.3 German News Titles Scripts

This repository contains the finetune and dataset generation scripts for the german news titles finetune project.

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

```bash
./test-peft_v3.sh results/checkpoint-100/
```

## Merge PEFT

```bash
./merge-peft.sh  results/checkpoint-100/ dummy
```

## Test via Transformers inference

```bash
./test-peft.sh models/dummy
```

# Test via VLLM

```bash
# Start vLLM
./start-vllm.sh models/dummy/

# Run inference
./vllm-test.sh dummy
```

