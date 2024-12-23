#!/bin/bash

if [ $1 ]; then
    TARGET_DEV=$1
    echo "Target device specified as ${TARGET_DEV}"
else
    echo "No target device specified, exiting..."
    exit 1
fi;

if [ $2 ]; then
    TARGET_DIR=$2
    echo "Code target specifed as ${TARGET_DIR}"
else
    TARGET_DIR=/Volumes/CIRCUITPY/
    echo "Code target not specified attempting to use target ${TARGET_DIR}"
fi;

echo "Writing code.py to ${TARGET_DIR}"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cp ${PWD}/code.py $TARGET_DIR
screen ${TARGET_DEV} 115200
