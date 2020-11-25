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

SCRIPT=`realpath -s $0`
echo $SCRIPT
SCRIPTPATH=`dirname $SCRIPT` 
python3 $SCRIPTPATH/src/LogViewer.py
