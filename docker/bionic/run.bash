#!/usr/bin/env bash


SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR_PATH=$(dirname "$SCRIPT_PATH")
SRC_PATH=$(realpath "$SCRIPT_DIR_PATH/../../src")

xhost +

docker run -it \
    --gpus=all \
    --net=host \
    --env="DISPLAY=$DISPLAY" \
    --env="/tmp/.X11-unix:/tmp/.X11-unix" \
    --volume="$SRC_PATH:/ompl_demo/src" \
    --runtime=nvidia \
    ompl_demo

xhost -
