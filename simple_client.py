import os
import socket
import tarfile
import sys

MSGLEN = 4096

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def receive_response(sock):
    chunks = []
    bytes_recd = 0
    while bytes_recd < MSGLEN:
        chunk = sock.recv(1024)
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return join(chunks)

# path = input("Digite o caminho dos seus arquivos:")
path = "/home/mtandrade/PycharmProjects/SdProject/TestExamples/Java_example/"

make_tarfile("ClientFiles/client.tar.gz", path)
size = os.path.getsize("ClientFiles/client.tar.gz")

s = socket.socket()
s.connect(("localhost", 9001))
file = open("ClientFiles/client.tar.gz", "rb")
src = file.read()

s.sendall(src)