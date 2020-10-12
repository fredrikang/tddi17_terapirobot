import socket as socket
import os
import sys
import threading
import io
import requests # Imported.
from time import sleep
from pathlib import Path

PORT = 8888
HOST = '192.168.0.105' # Default host-IP of Furhat simulator.
if len(sys.argv) > 1:
    try:
        socket.inet_aton(sys.argv[1])
        HOST = sys.argv[1]
    except socket.error:
        print('Bad IP! Defaults ' + HOST + ' instead.')


def connect():
    """
    Connect to the server
    """
    global s    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(s.connect_ex((HOST, PORT)) != 0):
          sleep(5)

def createLogFile(data):
    """
    Create a log file with the timestamp received before this call.
    Fetches log file data from either webaddress or from the robot itself.
    This is decided based on the format of the timestamp, as there's currently no support
    from the from the robot for sending the cloud link this can somewhat be ignored.

    Will only accept timestamps (filenames) of 'YYYY-MM-dd%YYHH-mm-ss', 'YYYY-MM-dd%HH-mm-ss', 'YYYY-MM-dd HH-mm-ss'
    any other format of the timestamp may result in exception. Other names may get approved but can still cause errors.
    """
    logDir = os.path.join(Path.home(), 'FurhatLogs', 'logs')
    try:
        if data.find('%') != -1:
            if len(data) > 24:
                timestamp = data.split('/')[-1].split('\'')[0].split('%')
            else:
                timestamp = data.split('\'')[1].split('%')
        
            date = timestamp[0][0:11] + ' '
            time = timestamp[1][2:10]
        else:
            date = data[2:12] + ' '
            time = data[13:21]
    except: 
        print('Failed to get timestamp')
        return

    try:
        if not os.path.exists(logDir):
            os.makedirs(logDir)
    except:
        print('Failure to create or find log directory "FurhatLogs"')
        return

    fname = os.path.join(logDir, date + time, 'dialog.json')
    if not os.path.exists(os.path.dirname(fname)):
        try:
            os.makedirs(os.path.dirname(fname))
        except:
            print('Failed to create folder: ' + os.path.dirname(fname))
            return
    try: # Try to fetch from url
        log = requests.get(data[2:len(data)-1]).content
        log = log[str(log).index('[') - 4:len(log) - 10]
        with open(fname, "wb") as f:
            f.write(log)
            f.close()
    except:        
        connect()
        flog = s.recv(65350)
        if str(flog).find('version') != -1:
            with open(fname, "wb") as f:
                f.write(flog)                    
                f.close()
            return
        else:
            print('Bad file!')
            return

print('Trying to connect to: ' + HOST + ' via port: ' + str(PORT))
connect()  
print('Connected.')

try:
    while(True):    
        data = s.recv(1024)
        if len(data) == 0:
            connect()
        else:
            print('received', repr(data))
            createLogFile(repr(data))
            connect()
except:
    print('Lost connection.')