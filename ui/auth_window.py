from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QLabel
)


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Welcome")
        self.resize(300, 200)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("login")
        self.signup_btn = QPushButton("register")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Poly massager"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.signup_btn)

        self.setLayout(layout)