import sys
import socket
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, QThread


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1234


class ReceiverThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.running = True

    def run(self):
        while self.running:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if msg:
                    self.message_received.emit(msg.strip())
                else:
                    break
            except:
                break

    def stop(self):
        self.running = False
        self.quit()


class ChatWindow(QWidget):
    def __init__(self, sock, username):
        super().__init__()
        self.sock = sock
        self.username = username
        self.setWindowTitle(f"💬 Group Chat - {username}")
        self.setMinimumWidth(450)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.message_input = QLineEdit()
        self.send_button = QPushButton("📤 Send")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"🟢 Logged in as: {username}"))
        layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)

        self.setStyleSheet("""
            QTextEdit, QLineEdit {
                font-size: 14px;
                padding: 8px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Receiver thread
        self.receiver = ReceiverThread(self.sock)
        self.receiver.message_received.connect(self.display_message)
        self.receiver.start()

    def send_message(self):
        msg = self.message_input.text().strip()
        if msg:
            try:
                self.sock.sendall((msg + '\n').encode('utf-8'))
                self.message_input.clear()
            except:
                QMessageBox.critical(self, "Error", "Disconnected from server.")

    def display_message(self, msg):
        self.chat_display.append(msg)

    def closeEvent(self, event):
        try:
            self.receiver.stop()
            self.sock.close()
        except:
            pass
        event.accept()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Login to Group Chat")
        self.setFixedWidth(350)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("🚀 Login")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("👤 Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("🔑 Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        self.login_button.clicked.connect(self.connect_to_server)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border-radius: 8px;
                border: 1px solid #aaa;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QLabel {
                font-weight: bold;
                margin-top: 10px;
            }
        """)

    def connect_to_server(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password.")
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_HOST, SERVER_PORT))
            sock.sendall((username + '\n').encode('utf-8'))

            # Go to chat window
            self.chat_window = ChatWindow(sock, username)
            self.chat_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", str(e))


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()