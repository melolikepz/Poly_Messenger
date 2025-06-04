from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QWidget
)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ورود به مسنجر")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(placeholderText="نام کاربری")
        self.password_input = QLineEdit(placeholderText="رمز عبور", echoMode=QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton("ورود")
        self.register_btn = QPushButton("ثبت نام")

        layout.addWidget(QLabel("پیام‌رسان ساده"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


class ChatWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"مسنجر - {username}")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.chat_display = QTextEdit(readOnly=True)
        self.message_input = QLineEdit(placeholderText="پیام خود را بنویسید...")
        self.send_btn = QPushButton("ارسال")

        layout.addWidget(self.chat_display)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)