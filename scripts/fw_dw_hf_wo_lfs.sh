#!/usr/bin/env bash
#
# Downloads models from HF without LFS for faster-whisper
# NOTE: This is specific to faster-whisper

set -euo pipefail

url_pfx="https://huggingface.co/guillaumekln"
function fetch {
    git clone "$hf_url" "$WSCRIBE_MODELS_DIR/$model_name"
    curl -L "$hf_url/resolve/main/model.bin" -o "$WSCRIBE_MODELS_DIR/$model_name/model.bin"
}

if [[ -z "$WSCRIBE_MODELS_DIR" ]]; then
    printf "WSCRIBE_MODELS_DIR env missing"
    exit 2
fi

if [[ $# -ne 1 ]]; then
    printf "Usage: %s <faster-whisper-model-size>\n Files are downloaded to %s\n" "$0" "$WSCRIBE_MODELS_DIR"
    exit 1
fi

model_name="faster-whisper-$1"
hf_url="$url_pfx/$model_name"
size_regex='(small|medium|large-v2)'

if ! [[ $1 =~ $size_regex ]]; then
    printf "%s should match %s" "$1" "$size_regex"
    exit 1
fi

fetch
printf "%s was downloaded to %s" "$model_name" "$WSCRIBE_MODELS_DIR/$model_name"
