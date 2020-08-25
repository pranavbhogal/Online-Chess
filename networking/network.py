import socket
import pickle



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 97.107.134.52 server ip
        self.server = "192.168.1.39"  # this ip address should match the one in server
        self.port = 5555
        self.adrs = (self.server, self.port)
        self.p = self.connect()


    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.adrs)
            return self.client.recv(2048).decode()  # loads bytedata
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)














