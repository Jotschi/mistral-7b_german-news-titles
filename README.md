# Finetune Mistral 7B v0.3 German News Titles Scripts

This repository contains the finetune and dataset generation scripts for the german news titles finetune project.

## Dataset

The `dataset` scripts generate the entries using Ollama and `dolphin-mixtral:v2.7`.

## Train

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

