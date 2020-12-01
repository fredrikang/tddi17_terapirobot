#!/bin/bash

sudo apt-get install -y python3

sudo apt-get install -y python3-pip

yes | pip3 install -r requirements.txt

sudo apt-get install -y ffmpeg