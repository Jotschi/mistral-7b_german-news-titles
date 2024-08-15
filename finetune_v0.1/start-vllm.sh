#!/bin/bash

set -o nounset
set -o errexit

PORT=10300
LLM_NAME=$(basename $1)
LLM="/models/$LLM_NAME"
IMAGE="vllm/vllm-openai"
VERSION="v0.5.4"
NAME=vllm

if [ ! -e models/$LLM_NAME ] ; then
  echo "Could not find LLM in models folder"
  exit 10
fi
podman pull $IMAGE:$VERSION

echo "Using LLM $LLM"
podman rm -f $NAME || true
podman run -d --shm-size 16G \
      --device nvidia.com/gpu=all \
      --name $NAME \
      -p 0.0.0.0:$PORT:8000/tcp \
      -v $(pwd)/.cache:/root/.cache/huggingface \
      -v $(pwd)/models:/models \
      $IMAGE:$VERSION \
      --model $LLM \
      --max-model-len 4096 \
      --load-format safetensors

echo "Starting log output. Press CTRL+C to exit log"
docker logs -f $NAME

