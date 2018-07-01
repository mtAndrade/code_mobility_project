import os
import socket
import tarfile
import sys

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


# path = input("Digite o caminho dos seus arquivos:")
path = "/home/mtandrade/PycharmProjects/SdProject/Client_Path_Test/"

make_tarfile("ClientFiles/client.tar.gz", path)
s = socket.socket()
s.connect(("localhost", 9000))
file = open("ClientFiles/client.tar.gz", "rb")
src = file.read()
s.sendall(src)
