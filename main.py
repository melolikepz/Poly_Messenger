import socket
import sys
import time
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

        # Initialize chat variables
        self.chat_window = None
        self.client_thread = None
        self.current_username = None

    def handle_login(self):
        """Handle login button click"""
        username = self.login_window.username_input.text()
        password = self.login_window.password_input.text()

        if not username or not password:
            QMessageBox.warning(self.login_window, "خطا", "نام کاربری و رمز عبور نمی‌توانند خالی باشند!")
            return

        if check_user(username, password):
            self.current_username = username
            self.start_chat()
        else:
            QMessageBox.warning(self.login_window, "خطا", "نام کاربری یا رمز عبور اشتباه است!")

    def handle_register(self):
        """Handle register button click"""
        username = self.login_window.username_input.text()
        password = self.login_window.password_input.text()

        if not username or not password:
            QMessageBox.warning(self.login_window, "خطا", "نام کاربری و رمز عبور نمی‌توانند خالی باشند!")
            return

        if add_user(username, password):
            QMessageBox.information(self.login_window, "موفق", "ثبت نام با موفقیت انجام شد!")
        else:
            QMessageBox.warning(self.login_window, "خطا", "نام کاربری تکراری است!")

    def start_chat(self):
        """Start chat session"""
        self.login_window.hide()

        # Create chat window
        self.chat_window = ChatWindow(self.current_username)

        # Setup client thread
        self.client_thread = ClientThread('127.0.0.1', 1234)
        self.client_thread.new_message.connect(self.show_message)
        self.client_thread.start()

        # Wait for connection
        if not self.wait_for_connection():
            QMessageBox.critical(self.chat_window, "خطا", "اتصال به سرور برقرار نشد!")
            self.chat_window.close()
            self.login_window.show()
            return

        # Set username after connection is established
        self.client_thread.set_username(self.current_username)

        # Connect send button
        self.chat_window.send_btn.clicked.connect(self.send_message)

        # Connect window close event
        self.chat_window.closeEvent = self.close_chat

        self.chat_window.show()

    def wait_for_connection(self, timeout=5):
        """Wait for socket connection"""
        start_time = time.time()
        while not hasattr(self.client_thread, 'connected') or not self.client_thread.connected:
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.1)
            QApplication.processEvents()  # Keep UI responsive
        return True

    def show_message(self, message):
        """Display new message in chat window"""
        self.chat_window.chat_display.append(message)

    def send_message(self):
        """Send message to server"""
        message = self.chat_window.message_input.text()
        if message:
            self.client_thread.send_message(message)
            self.chat_window.message_input.clear()

    def close_chat(self, event):
        """Handle chat window closing"""
        if self.client_thread:
            self.client_thread.close_connection()
        event.accept()

    def run(self):
        """Run the application"""
        self.login_window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    # Check if server is running
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.connect(('127.0.0.1', 1234))
        test_socket.close()
    except:
        QMessageBox.critical(None, "خطا", "سرور در حال اجرا نیست! لطفاً اول سرور را اجرا کنید.")
        sys.exit(1)

    app = MessengerApp()
    app.run()