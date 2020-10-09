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
    global s    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(s.connect_ex((HOST, PORT)) != 0):
          sleep(5)

def createLogFile(data):
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
    try:
        log = requests.get(data[2:len(data)-1]).content
        log = log[str(log).index('[') - 4:len(log) - 10]
        with open(fname, "wb") as f:
            f.write(log)
            f.close()
    except:        
        connect()
        flog = s.recv(8169)
        if str(flog).find('version') != -1:
            with open(fname, "wb") as f:
                f.write(flog)                    
                f.close()
            return 0
        else:
            print('Bad file!')
            return -1

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
    print('Lost connection, exiting.')
    exit(code=0)
