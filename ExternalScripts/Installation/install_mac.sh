#! /bin/bash

brew help
if [$? -ne 0]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew install python

pip install -r requirements.txt

brew install ffmpeg

