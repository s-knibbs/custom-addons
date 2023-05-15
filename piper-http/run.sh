#!/usr/bin/env bashio

export LENGTH_SCALE=$(bashio::config 'length_scale')
export MODEL_FILE=$(bashio::config 'model_file')
/usr/bin/python3 run.py