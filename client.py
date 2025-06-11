# client2.py

import socket
import json
import threading
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QTextEdit
)

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setPlaceholderText("Confirm Password")

        self.pic_path = ""

        self.choose_pic_btn = QPushButton("Choose Profile Picture")
        self.choose_pic_btn.clicked.connect(self.choose_picture)

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.clicked.connect(self.send_signup)

        self.layout.addWidget(QLabel("Sign Up Form"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.phone_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.confirm_input)
        self.layout.addWidget(self.choose_pic_btn)
        self.layout.addWidget(self.signup_btn)

        self.setLayout(self.layout)

    def choose_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.pic_path = file_path

    def send_signup(self):
        if self.password_input.text() != self.confirm_input.text():
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        data = {
            "type": "signup",
            "username": self.username_input.text(),
            "phone": self.phone_input.text(),
            "password": self.password_input.text(),
            "profile_pic": self.pic_path
        }

        try:
            with socket.socket() as s:
                s.connect(("localhost", 12345))
                s.send(json.dumps(data).encode())
                response = s.recv(1024).decode()
                QMessageBox.information(self, "Response", response)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign In")
        self.layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.send_login)

        self.layout.addWidget(QLabel("Sign In"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_btn)

        self.setLayout(self.layout)

    def send_login(self):
        data = {
            "type": "signin",
            "username": self.username_input.text(),
            "password": self.password_input.text()
        }

        try:
            with socket.socket() as s:
                s.connect(("localhost", 12345))
                s.send(json.dumps(data).encode())
                response = s.recv(1024).decode()
                QMessageBox.information(self, "Login Result", response)

                if response == "Login successful":
                    self.close()
                    self.main_panel = MainPanel(self.username_input.text())
                    self.main_panel.show()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


class MainPanel(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.setWindowTitle("Messenger - Main Panel")
        self.layout = QVBoxLayout()
        self.current_user = current_user

        self.user_list_layout = QVBoxLayout()
        self.layout.addWidget(QLabel(f"Logged in as: {self.current_user}"))
        self.layout.addLayout(self.user_list_layout)

        self.setLayout(self.layout)
        self.load_users()

    def load_users(self):
        try:
            with socket.socket() as s:
                s.connect(("localhost", 12345))
                data = {"type": "get_users", "username": self.current_user}
                s.send(json.dumps(data).encode())
                response = s.recv(4096).decode()
                users = json.loads(response)

                if isinstance(users, list):
                    for u in users:
                        btn = QPushButton(f"Chat with {u}")
                        btn.clicked.connect(lambda _, u=u: self.start_chat(u))
                        self.user_list_layout.addWidget(btn)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def start_chat(self, target_user):
        self.chat_window = ChatWindow(self.current_user, target_user)
        self.chat_window.show()


class ChatWindow(QWidget):
    def __init__(self, current_user, target_user):
        super().__init__()
        self.setWindowTitle(f"Chat with {target_user}")
        self.current_user = current_user
        self.target_user = target_user

        self.layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        self.layout.addWidget(self.chat_display)
        self.layout.addWidget(self.message_input)
        self.layout.addWidget(self.send_button)
        self.setLayout(self.layout)

        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return

        data = {
            "type": "send_message",
            "from": self.current_user,
            "to": self.target_user,
            "message": message
        }

        try:
            with socket.socket() as s:
                s.connect(("localhost", 12345))
                s.send(json.dumps(data).encode())
                self.chat_display.append(f"You: {message}")
                self.message_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def receive_messages(self):
        while self.running:
            try:
                with socket.socket() as s:
                    s.connect(("localhost", 12345))
                    data = {
                        "type": "receive_messages",
                        "from": self.target_user,
                        "to": self.current_user
                    }
                    s.send(json.dumps(data).encode())
                    response = s.recv(4096).decode()
                    messages = json.loads(response)

                    if isinstance(messages, list):
                        self.chat_display.clear()
                        for msg in messages:
                            self.chat_display.append(f"{msg['sender']}: {msg['text']}")
            except:
                pass
            time.sleep(1.5)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SignInWindow()
    window.show()
    sys.exit(app.exec())