import socket
import sys


class FurhatTCPConnection:
    def __init__(self, host):
        self.socket_address = (host, 1982)
        print >>sys.stderr, 'starting up on %s port %s'
    
    def run(self):
        self.sock.bind(server_address)
