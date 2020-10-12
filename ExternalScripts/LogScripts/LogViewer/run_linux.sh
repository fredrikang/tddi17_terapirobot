#!/bin/bash
python3 -c "import fpdf" > /dev/null 2>&1
if [ $? -eq 1 ]
then
	pip3 install fpdf
fi
python3 -c "import tkinter" > /dev/null 2>&1
if [ $? -eq 1 ]
then
	pip3 install tk-tools
fi

python3 ./src/LogViewer.py
