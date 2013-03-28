import os
import socket
import sendmsg
import struct
import threading
import sys

class ServingThread(threading.Thread):
     def __init__(self, server):
         threading.Thread.__init__(self)
         self.server = server

     def run(self):
        while True:
            try:
                print 'Server accepting connections on %d' % os.getpid()
                client, addr = self.server.accept()
                print 'Client connected, serving him'
                client.send('Hello from process %d' % os.getpid())
                client.close()
            except Exception,e:
                print e
                print 'Will terminate now'
                break

#used to communicate with standby process and hand-over it the listnening socket
#when requested
class ControlThread(threading.Thread):
     def __init__(self, server):
         threading.Thread.__init__(self)
         self.server = server

     def run(self):
        us = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        us.bind(('mig.sock'))
        us.listen(1)
        print 'waiting for standby process to start and connect to unix socket'
        uconn, addr = us.accept()
        print 'standby process connected, hand it over our server-socket'
        payload = struct.pack('i', self.server.fileno())
        sendmsg.sendmsg( uconn.fileno(), '', 0, (socket.SOL_SOCKET, sendmsg.SCM_RIGHTS, payload))
        print 'Sent server-socket...awaiting for handover complete signal', self.server.fileno()
        result = uconn.recv(1024)
        if result == 'KILL':
            #1. TODO: wait for already clients connected to complete
            #2. Terminate
            return

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 5566))
server.listen(10)

server_thread = ServingThread(server)
control_thread = ControlThread(server)
server_thread.start()
control_thread.start()

control_thread.join()
server_thread._Thread__stop()

print 'Done.'


