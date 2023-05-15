#!/usr/bin/env bashio

export LENGTH_SCALE=$(bashio::config 'length_scale')
/usr/bin/python3 run.py