#!/usr/bin/env bash

docker run -it \
    --env="DISPLAY=$DISPLAY" \
    --runtime=nvidia \
    ompl_demo
