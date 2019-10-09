#! /bin/bash

# setup venv
# python3 -m venv env
# source env/bin/activate

pip3 install -U opencv-python

# install vidgear
git clone https://github.com/abhiTronix/vidgear.git
cd vidgear
git checkout testing
pip3 install .
cd ..

# create folder for storing videos
mkdir videos
