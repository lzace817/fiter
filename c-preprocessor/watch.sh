#!/bin/bash

set -e

COLOR="\033[4;33m"
RESET="\033[0m"

path=$1

srclink="${COLOR}build.sh:1:${RESET}"
echo -e "${srclink} ready to play"

update() {
    clear
    echo -e "${srclink}"
    ./build.sh || true
}

update

# mac
if [[ $OSTYPE == darwin* ]]; then
fswatch build.sh | while read; do
    update
done
fi

# linux
inotifywait -q -m -e close_write playground.c | while read; do
    update
done
