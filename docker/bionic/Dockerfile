FROM nvidia/opengl:1.0-glvnd-devel-ubuntu18.04

ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

RUN apt-get update -y && apt-get install -y \
    vim \
    tmux \
    git \
    wget \
    lsb-release \
    lsb-core \
    tmux \
    vim \
    build-essential \
    g++ \
    gnupg2

ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir ompl && \
    cd ompl && \
    wget https://ompl.kavrakilab.org/install-ompl-ubuntu.sh && \
    chmod u+x install-ompl-ubuntu.sh

RUN cd ompl && \
    ./install-ompl-ubuntu.sh --app
