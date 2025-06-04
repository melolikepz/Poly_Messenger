import socket
import threading

HOST = '127.0.0.1'  # لوکال‌هست
PORT = 1234  # پورت سرور

clients = {}  # ذخیره کلاینت‌های متصل


def handle_client(conn, addr):
    print(f"اتصال جدید از {addr}")
    username = conn.recv(1024).decode('utf-8')
    clients[username] = conn

    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break

            # ارسال پیام به همه کاربران
            for user, client_conn in clients.items():
                if user != username:
                    client_conn.send(f"{username}: {message}".encode('utf-8'))
        except:
            break

    del clients[username]
    conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"سرور روشن شد روی {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()