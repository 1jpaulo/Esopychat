import socket
import threading

class Server:

    def __init__(self, hostname='localhost', port=9000):
        # saves all incoming client connections
        self.connections = []
        
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind((hostname, port))
        # listen up to 5 connections
        self.conn.listen(5)

        self.start()

    def recv_from(self, c, a):
        '''
            Receive data from each client 
            socket in their current thread
        '''
        while True:
            data = c.recv(2048)
            if not data:
                break
            for conn in self.connections:
                if not conn is c:
                    conn.send(data)
    
    def start(self):
        while True:
            (clientsocket, address) = self.conn.accept()
            self.connections.append(clientsocket)
            
            cthread = threading.Thread(target=self.recv_from, args=(clientsocket, address))
            cthread.start()
            
            print("Client {}:{} ".format(address[0], address[1]))

if __name__ == "__main__":
    s = Server()
