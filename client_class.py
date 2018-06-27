from socket import *

class Client(object):
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

    def connect(self, addr):
        self.clientSocket.connect(addr)

    def _sendFile(self, path):
        sendfile = open(path, 'rb')
        data = sendfile.read()

        self._con.sendall(  (len(data))) # Send the length as a fixed size message
        self._con.sendall(data)


        # Get Acknowledgement
        self._con.recv(1) # Just 1 byte

client = Client()
client.connect(("192.168.0.102", 21000))
client._sendFile(os.path.abspath("file_1.txt")) # If this file is in your current directory, you may just use "file_1.txt"
