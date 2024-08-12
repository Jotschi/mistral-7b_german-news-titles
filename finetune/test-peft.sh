#!/bin/bash

set -o nounset
set -o errexit

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

. $SCRIPT_DIR/venv/bin/activate

export CUDA_VISIBLE_DEVICES="0,1"

echo "Invoking PEFT test for checkoint $1"
python "$SCRIPT_DIR/src/test-peft-inference.py" "$1"
