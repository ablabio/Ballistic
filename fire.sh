#!/bin/bash

# set up the configs for pm2.
# args: api_keys_path, symbols_file_path
python3 config.py --api_keys_path $1 --symbols_path $2

# execute processes.
for entry in "./pm2_configs"/*
do
	cp $entry ecosystem.config.js
	pm2 start ecosystem.config.js
	rm ecosystem.config.js
done

exit 1