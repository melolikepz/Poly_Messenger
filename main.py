import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from client.client import ClientThread
from client.ui import LoginWindow, ChatWindow
from database.db import init_db, add_user, check_user


class MessengerApp:
    def __init__(self):
        # Initialize database
        init_db()

        # Create Qt application
        self.app = QApplication(sys.argv)

        # Create login window
        self.login_window = LoginWindow()
        self.login_window.login_btn.clicked.connect(self.handle_login)
        self.login_window.register_btn.clicked.connect(self.handle_register)

        # Chat window (will be created after login)
        self.chat_window = None
        self.client_thread = None

    def handle_login(self):
        """Handle login button click"""
        username = self.login_window.username_input.text()
        password = self.login_window.password_input.text()

        if check_user(username, password):
            self.start_chat(username)
        else:
            QMessageBox.warning(self.login_window, "خطا", "نام کاربری یا رمز عبور اشتباه است!")

    def handle_register(self):
        """Handle register button click"""
        username = self.login_window.username_input.text()
        password = self.login_window.password_input.text()

        if add_user(username, password):
            QMessageBox.information(self.login_window, "موفق", "ثبت نام با موفقیت انجام شد!")
        else:
            QMessageBox.warning(self.login_window, "خطا", "نام کاربری تکراری است!")

    def start_chat(self, username):
        """Start chat session"""
        self.login_window.hide()

        # Create chat window
        self.chat_window = ChatWindow(username)

        # Setup client thread
        self.client_thread = ClientThread('127.0.0.1', 1234)
        self.client_thread.new_message.connect(self.chat_window.chat_display.append)
        self.client_thread.start()
        self.client_thread.set_username(username)

        # Connect send button
        self.chat_window.send_btn.clicked.connect(
            lambda: self.send_message()
        )

        self.chat_window.show()

    def send_message(self):
        """Send message to server"""
        message = self.chat_window.message_input.text()
        if message:
            self.client_thread.send_message(message)
            self.chat_window.message_input.clear()

    def run(self):
        """Run the application"""
        self.login_window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = MessengerApp()
    app.run()