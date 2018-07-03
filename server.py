import os
import socket
import docker
import tarfile
import zipfile

# import subprocess

def find_language(path):
    dir_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for f in dir_files:
        filename, file_extension = os.path.splitext(f)
        if(file_extension == '.py'):
            return 'python'
        else: 
            if(file_extension == '.java'):
                return 'java'
            else: 
                if(file_extension == '.c'):
                    return 'c'
    return -1

def extract_file(path, to_directory='.'):
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'

    cwd = os.getcwd()
    os.chdir(to_directory)

    try:
        file = opener(path, mode)
        try:
            file.extractall()
        finally:
            file.close()
    finally:
        os.chdir(cwd)

HOST = ''
PORT = 9001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print('Waiting Connection...')
connection, addr = server_socket.accept()

with connection:
    print('Connected by', addr)
    serv_file = open("Shared/srv_file.tar.gz", 'wb')  # Open in binary
    while True:
        data = connection.recv(1024)
        while(data):
            if not data: break
            serv_file.write(data)
            data = connection.recv(1024)
        break
    serv_file.close()

print("Extract on server")
tar = tarfile.open("Shared/srv_file.tar.gz", "r:gz")
tar.extractall("Shared")
tar.close()

# Depois de recer os arquivos e extrair eles na pasta Shared.
# Vamos precisar de um script que reconhece qual o tipo do arquivo aqui
# Algo do tipo? language = find_language(path_of_extracted_files)
language = find_language('./Shared')
if (language == -1):
    print("Error -- the language could not be identified")

print("Call container")
client = docker.from_env()

image, json = client.images.build(path=".", tag="sd-project-img")

container = client.containers.create(image,
                                     #name="SdProject",
                                     stdin_open=True,
                                     auto_remove=True)
container.start()

# List = open("filename.txt").readlines() # pra pegar todos os comandos no arquivo cmd.txt de uma vez
cmds = list()
cmds.append("gcc -Wall Shared/program.c -o hello")
cmds.append("./hello")

exit_code = ""
output = []

for cmd in cmds:
    exit_code, output = container.exec_run(cmd)
    # output = subprocess.check_output(cmd.split())

print(output)

# retorno do resultado para o cliente usando a mesma conexão
connection.sendall(output)
connection.close()
