#!/bin/bash
python3 -c "import fpdf" > /dev/null 2>&1
if [ $? -eq 1 ]
then
	echo "Installing fpdf for python3"
	pip3 install fpdf
fi
python3 -c "import tkinter" > /dev/null 2>&1
if [ $? -eq 1 ]
then
	echo "Installing tkinter(UI) for python3."
	sudo apt-get install python3-tk
fi

python3 ./src/LogViewer.py
