#!/bin/bash

yes | sudo pacman -S python

yes | sudo pacman -S python-pip

yes | pip install -r requirements.txt

yes | sudo pacman -S ffmpeg