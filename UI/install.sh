#!/bin/bash

is_root() {
  [ ${EUID:-$(id -u)} -eq 0 ]
}

install_linux() {
  if ! is_root; then
    echo "Script must be run as root"
    exit 1
  fi
  DIST=$(lsb_release -is)
  if [[ "$DIST" == "Arch" ]]; then
    yes | pacman -S python python-pip ffmpeg opencv
    pip install -r requirements.txt -vvv
  elif [[ "$DIST" == "Ubuntu" ]]; then
    apt-get install -y python3 python3-pip ffmpeg opencv
    pip3 install -r requirements.txt
  else
    echo "Unsupported OS"
    exit 1
  fi
}

install_mac() {
  if is_root; then
    echo "Dont run the script as root"
    exit
  fi
  if test ! $(which brew); then
    echo "Installing brew"
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  fi
  brew install python3 ffmpeg opencv
  pip3 install -r requirements.txt -vvv
}

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  #linux
  echo "Detecting linux"
  install_linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
  #OSX
  echo "Detecting MAC OSX"
  install_mac
else
  echo "Unsupported OS"
  exit 1
fi
