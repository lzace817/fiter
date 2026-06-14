#!/bin/bash

set -e

if [[ -z $1 ]]; then
    echo no script provided
    exit 1
fi

COLOR="\033[4;33m"
RESET="\033[0m"

path=$1
script=$1

srclink="${COLOR}${script}:1:${RESET}"
echo -e "${srclink} ready to play"

update() {
    clear
    echo -e "${srclink}"
    python3 ${script} || true
}

update

# mac
if [[ $OSTYPE == darwin* ]]; then
fswatch ${script} | while read; do
    update
done
fi

# linux
eog out.svg &
inotifywait  -q -m -e close_write ${script} | while read; do
    update
done
