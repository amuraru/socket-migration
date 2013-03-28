import os
import socket
import sendmsg
import struct

us = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
us.connect(('mig.sock'))
print 'Make unix connection', us

result = sendmsg.recvmsg(us.fileno())
identifier, flags, [(level, type, data)] = result
print identifier, flags, [(level, type, data)]
fd = struct.unpack('i', data)[0]
print 'Get remote process fd', fd

conn = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
os.close(fd)

primary = False
while True:
    print 'waiting for client connections'
    client, addr = conn.accept()
    client.send('Hello, from process %d' % os.getpid())
    client.close()
    if not primary:
        print 'First client served succesfully, KILL peer process'
        us.send('KILL')
        primary = True

print 'Done.'
