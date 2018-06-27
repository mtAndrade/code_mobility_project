import socket
import sys

s = socket.socket()
s.connect(("localhost", 9000))
f = open("teste.txt", "rb")
s.sendfile(f)
s.close()