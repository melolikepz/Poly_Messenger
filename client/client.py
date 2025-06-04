import socket
from PyQt6.QtCore import QThread, pyqtSignal


class ClientThread(QThread):
    new_message = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True

            while self.connected:
                try:
                    message = self.socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    self.new_message.emit(message)
                except:
                    break
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.close_connection()

    def set_username(self, username):
        if self.connected and self.socket:
            try:
                self.socket.send(username.encode('utf-8'))
            except Exception as e:
                print(f"Error sending username: {e}")

    def send_message(self, message):
        if self.connected and self.socket:
            try:
                self.socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")

    def close_connection(self):
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            finally:
                self.socket = None