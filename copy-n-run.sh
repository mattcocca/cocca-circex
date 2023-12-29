#!/bin/bash

if [ $1 ]; then
    TARGET_DIR=$1
    echo "Code target specifed as ${TARGET_DIR}"
else
    TARGET_DIR=/Volumes/CIRCUITPY/
    echo "Code target not specified attempting to use target ${TARGET_DIR}"
fi;

echo "Writing code.py to ${TARGET_DIR}"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cp ${SCRIPT_DIR}/code.py $TARGET_DIR
screen /dev/tty.usbmodem2101 115200
