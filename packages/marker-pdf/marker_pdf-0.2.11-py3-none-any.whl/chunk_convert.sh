#!/bin/bash

trap 'pkill -P $$' SIGINT

# Check if NUM_DEVICES is set
if [[ -z "$NUM_DEVICES" ]]; then
    echo "Please set the NUM_DEVICES environment variable."
    exit 1
fi

if [[ -z "$NUM_WORKERS" ]]; then
    echo "Please set the NUM_WORKERS environment variable."
    exit 1
fi


# Get input folder and output folder from args
if [[ -z "$1" ]]; then
    echo "Please provide an input folder."
    exit 1
fi

if [[ -z "$2" ]]; then
    echo "Please provide an output folder."
    exit 1
fi

INPUT_FOLDER=$1
OUTPUT_FOLDER=$2

# Loop from 0 to NUM_DEVICES and run the Python script in parallel
for (( i=0; i<$NUM_DEVICES; i++ )); do
    DEVICE_NUM=$i
    export DEVICE_NUM
    export NUM_DEVICES
    export NUM_WORKERS
    echo "Running convert.py on GPU $DEVICE_NUM"
    cmd="CUDA_VISIBLE_DEVICES=$DEVICE_NUM marker $INPUT_FOLDER $OUTPUT_FOLDER --num_chunks $NUM_DEVICES --chunk_idx $DEVICE_NUM --workers $NUM_WORKERS"
    [[ -n "$METADATA_FILE" ]] && cmd="$cmd --metadata_file $METADATA_FILE"
    [[ -n "$MIN_LENGTH" ]] && cmd="$cmd --min_length $MIN_LENGTH"
    eval $cmd &

    sleep 5
done

# Wait for all background processes to finish
wait
