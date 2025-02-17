#!/bin/sh

script_dir=$(dirname $(readlink -f $0))
name="influx-field-monitor"

session=`tmux ls | grep $name`
if [ -z "$session" ]; then
    tmux new-session -d -s $name \
	 "while true; do python $script_dir/field.py; sleep 2; done" && \
	echo "create session $name"
else
    tmux a -t $name
fi
