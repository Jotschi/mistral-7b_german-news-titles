#!/bin/bash

set -o nounset 
set -o errexit 

NAME=ollama
IMAGE=ollama/ollama
VERSION="0.3.6"

podman pull $IMAGE:$VERSION
podman rm -f $NAME || true

podman run -d  --device nvidia.com/gpu=all --shm-size 1g \
        -v /opt/cache/ollama:/root/.ollama \
        -p 0.0.0.0:11435:11434/tcp \
        --name $NAME \
        $IMAGE:$VERSION

echo "Starting log output. Press CTRL+C to exit log"
podman logs -f $NAME

