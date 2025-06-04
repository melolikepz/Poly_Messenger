import socket
from PyQt6.QtCore import QThread, pyqtSignal


class ClientThread(QThread):
    new_message = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                self.new_message.emit(message)
            except:
                break

    def send_message(self, message):
        self.socket.send(message.encode('utf-8'))

    def set_username(self, username):
        self.socket.send(username.encode('utf-8'))