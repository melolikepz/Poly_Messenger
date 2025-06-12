import socket
import threading

HOST = '0.0.0.0'
PORT = 1234

client_handlers = []
handlers_lock = threading.Lock()

class ClientHandler(threading.Thread):
    def __init__(self, conn: socket.socket, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.name = None
        self.reader = conn.makefile('r', encoding='utf-8')
        self.writer = conn.makefile('w', encoding='utf-8')

    def run(self):
        try:
            # get username
            self.name = self.reader.readline().strip()
            if not self.name:
                return

            with handlers_lock:
                client_handlers.append(self)

            self.broadcast_message(f"🔵 {self.name} has joined the chat.")

            while True:
                line = self.reader.readline()
                if not line:
                    break
                message = line.strip()
                if message:
                    self.broadcast_message(f"[{self.name}] {message}")

        except Exception as e:
            print(f"[ERROR] {self.addr}: {e}")
        finally:
            self.remove_handler_and_close()

    def broadcast_message(self, message: str):
        with handlers_lock:
            for handler in client_handlers.copy():
                try:
                    handler.writer.write(message + "\n")
                    handler.writer.flush()
                except:
                    handler.remove_handler_and_close()

    def remove_handler_and_close(self):
        with handlers_lock:
            if self in client_handlers:
                client_handlers.remove(self)

        try:
            self.reader.close()
            self.writer.close()
            self.conn.close()
        except:
            pass

        if self.name:
            self.broadcast_message(f"🔴 {self.name} has left the chat.")
        print(f"[INFO] Closed connection: {self.addr} ({self.name})")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        try:
            server_sock.bind((HOST, PORT))
            server_sock.listen()
            print(f"[✅ SERVER] Group chat server is running on {HOST}:{PORT}...")
        except OSError as e:
            print(f"[❌ ERROR] Could not bind to port {PORT}: {e}")
            return

        try:
            while True:
                conn, addr = server_sock.accept()
                print(f"[NEW] Connection from {addr}")
                handler = ClientHandler(conn, addr)
                handler.start()
        except KeyboardInterrupt:
            print("\n[⛔️ SERVER] Shutdown requested.")
        finally:
            with handlers_lock:
                for handler in client_handlers.copy():
                    handler.remove_handler_and_close()
            print("[SERVER] All connections closed.")


if __name__ == '__main__':
    start_server()