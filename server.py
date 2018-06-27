import socket
import docker
import tarfile

# HOST = ''
# PORT = 9000
#
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen(1)
# print('Waiting Connection...')
# connection, addr = server_socket.accept()
#
# with connection:
#     print('Connected by', addr)
#     serv_file = open("srv_file.txt", 'wb')  # Open in binary
#     while True:
#         data = connection.recv(1024)
#         while(data):
#             if not data: break
#             serv_file.write(data)
#             data = connection.recv(1024)
#         break
#     serv_file.close()
#
print("Call container")

tar = tarfile.open("Shared/test.tar", "w")
tar.add("srv_file.txt")

client = docker.from_env()

image, json = client.images.build(path=".", tag="sd-project-img")

container = client.containers.create(image,
                                     #name="SdProject",
                                     stdin_open=True,
                                     auto_remove=True)
container.start()
cmds = list()
cmds.append("cat /mnt/shared/teste.txt")
exit_code, output = container.exec_run(cmds[0])

print(output)