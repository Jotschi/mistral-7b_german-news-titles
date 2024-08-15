#!/bin/bash

set -o nounset
set -o errexit


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

. $SCRIPT_DIR/venv/bin/activate

BASE_MODEL="mistralai/Mistral-7B-Instruct-v0.3"
PEFT_PATH="$1"
NAME="$2"

if [ ! -e $PEFT_PATH ] ; then
  echo "Failed to find model folder $PEFT_PATH"
  exit 10
fi


echo "Merging PEFT $PEFT_PATH into model with name $NAME"
python $SCRIPT_DIR/src/merge_peft_adapter.py \
    --peft_model_path=$PEFT_PATH \
    --output_dir=models/$NAME \
    --base_model_name_or_path=$BASE_MODEL

