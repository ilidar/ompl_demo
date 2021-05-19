#!/usr/bin/env bash

xhost +

docker run -it \
    --gpus=all \
    --net=host \
    --env="DISPLAY=$DISPLAY" \
    --env="/tmp/.X11-unix:/tmp/.X11-unix" \
    --runtime=nvidia \
    ompl_demo

xhost -
