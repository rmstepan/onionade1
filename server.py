import socket
import threading
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=100)


def _recvmsg(conn):
    buffsize = int(conn.recv(5))
    print "Buffsize:",buffsize
    msg = conn.recv(buffsize)
    return msg

def _listener(user):
    while True:
        #buffsize = user[0].recv(5)
        #print "Buffsize:", buffsize
        #x = user[0].recv(int(buffsize))
        x = _recvmsg(user[0])
        print user[2]+":"+x

        if x:
             print x
             for usr in users:
                 if usr[2]==user[2]:
                     pass
                 else:
                     msg = user[2]+":~$ "+x
                     usr[0].sendall(msg)

def _initcon(conn,addr):
    conn.sendall("In Onions We Trust!\n")
    buffsize = conn.recv(5)
    print "Buffsize:",buffsize
    name = conn.recv(int(buffsize))
    print "Name:",name
    user = (conn,addr[0],name)
    users.append(user)
    return user

s = socket.socket()
s.bind(("127.0.0.1",2222))
s.listen(100)

users = []

while True:
    conn, addr = s.accept()
    print "#New connection with",addr[0],"at port",addr[1]

    trip = pool.apply_async(_initcon,(conn,addr))
    user = trip.get()

    t_l = threading.Thread(target=_listener,args=(user,))
    t_l.start()
