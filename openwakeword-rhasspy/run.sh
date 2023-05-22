#!/usr/bin/with-contenv bashio

export MODEL=$(bashio::config 'model')
export CHUNK_LENGTH=$(bashio::config 'chunk_length')
export RHASSPY_URL=$(bashio::config 'rhasspy_url')
export THRESHOLD=$(bashio::config 'threshold')

/usr/bin/python3 wakeword.py