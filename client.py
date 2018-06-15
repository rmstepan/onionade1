import socket
import socks
import os
import threading
import time
import subprocess




def _sendmsg(msg):
    buffsize = normalize_buffsize(msg)

    s.sendall(buffsize)
    s.sendall(msg)

def _sender(username):
    while True:
        prompt = raw_input()

        _sendmsg(prompt)

def _listener():
    while True:
        msg = s.recv(1024)
        if msg:
            print msg

def utf8len(s):
    return len(s.encode("utf-8"))

def normalize_buffsize(s):
    res = str(utf8len(s))
    buff = ""
    if len(res)==1:
        buff = "0000"+res
    elif len(res)==2:
        buff = "000"+res
    elif len(res)==3:
        buff = "00"+res
    elif len(res)==4:
        buff = "0"+res
    elif len(res)==5:
        buff = res
    else:
        print "Buffer too big...Exiting"
        time.sleep(0.5)
    return buff

if os.name=='nt':
    path = os.getcwd()+'/win32/Tor/'+"tor.exe"
    subprocess.call(path)
    print "[*] Starting TOR service...Please wait!"
    time.sleep(15);

address = ""
with open("address",'r') as f:
    address = f.read().replace("\n","")


socket.setdefaulttimeout(10)
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s = socks.socksocket()
if s.connect((address,80)):
   print "Could not connect"
else:
    print "Connection Established"
    print s.recv(1024)

    name = raw_input("Username:~$ ")
    _sendmsg(name)

    t_s = threading.Thread(target=_sender,args=(name,))
    t_l = threading.Thread(target=_listener,args=())

    t_l.start()
    t_s.start()
