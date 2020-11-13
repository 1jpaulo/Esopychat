import socket
import threading

class Client:

    def recv_msg(self):
        while True:
            data = self.conn.recv(2048)
            if not data:
                break
            print(data.decode('UTF-8'))

    def send_msg(self):
        while True:
            msg = (self.username + ": " + input(self.username + ": ")).encode('UTF-8')
            self.conn.send(msg)

    def __init__(self, hostname='localhost', port=9000):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((hostname, port))

        self.username = input("Username: ")

        input_thread = threading.Thread(target=self.send_msg)
        input_thread.start()

        output_thread = threading.Thread(target=self.recv_msg)
        output_thread.start()

if __name__ == "__main__":
    c = Client()