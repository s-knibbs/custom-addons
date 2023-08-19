#!/usr/bin/with-contenv bashio

export MODEL=$(bashio::config 'model')
export CHUNK_LENGTH=$(bashio::config 'chunk_length')
export RHASSPY_URL=$(bashio::config 'rhasspy_url')
export THRESHOLD=$(bashio::config 'threshold')
export VAD_THRESHOLD=$(bashio::config 'vad_threshold')
export NOISE_SUPPRESSION=$(bashio::config 'noise_suppression')
export VERIFIER_MODEL=$(bashio::config 'verifier_model')
export VERIFIER_THRESHOLD=$(bashio::config 'verifier_threshold')

/usr/bin/python3 wakeword.py