#!/bin/bash
SCRIPT=`realpath -s $0`
echo $SCRIPT
SCRIPTPATH=`dirname $SCRIPT` 
python3 $SCRIPTPATH/src/LogViewer.py
