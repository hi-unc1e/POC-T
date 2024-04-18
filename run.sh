#!/bin/bash

# env
sudo apt-get update -y
sudo apt install python2 -y
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o /tmp/get-pip.py && python2  /tmp/get-pip.py 

# install
python2 -m pip install -r requirement.txt