import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem
)

def save_to_db():
    user_input = input_box.text()
    if not user_input:
        QMessageBox.warning(window, "خطا", "ورودی خالی است!")
        return

    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')

    cursor.execute("INSERT INTO messages (content) VALUES (?)", (user_input,))
    conn.commit()
    conn.close()

    QMessageBox.information(window, "موفقیت", "داده ذخیره شد!")
    input_box.clear()
    load_data()  # بعد از ذخیره، داده‌ها رو دوباره بارگذاری کن

def load_data():
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, content FROM messages")
    rows = cursor.fetchall()
    conn.close()

    table.setRowCount(len(rows))
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(["ID", "متن"])

    for row_idx, row_data in enumerate(rows):
        for col_idx, item in enumerate(row_data):
            table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("ذخیره و نمایش داده‌ها با PyQt6")

layout = QVBoxLayout()

input_box = QLineEdit()
input_box.setPlaceholderText("متنی بنویس...")

save_button = QPushButton("ذخیره در دیتابیس")
save_button.clicked.connect(save_to_db)

table = QTableWidget()

layout.addWidget(input_box)
layout.addWidget(save_button)
layout.addWidget(table)

window.setLayout(layout)

load_data()  # بارگذاری اولیه داده‌ها

window.show()
sys.exit(app.exec())