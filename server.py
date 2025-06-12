# server.py
import socket
import threading
import json
import shutil
import os
from database import create_connection

def get_user_id(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def handle_signup(data):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM users WHERE username=? OR phone=?", (data['username'], data['phone']))
        if c.fetchone():
            return "User already exists."

        profile_path = ""
        if data['profile_pic']:
            profile_path = os.path.join("profiles", os.path.basename(data['profile_pic']))
            os.makedirs("profiles", exist_ok=True)
            shutil.copyfile(data['profile_pic'], profile_path)

        c.execute("INSERT INTO users (username, phone, password, profile_pic) VALUES (?, ?, ?, ?)",
                  (data['username'], data['phone'], data['password'], profile_path))
        conn.commit()
        return "User registered successfully."
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

def handle_signin(data):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (data['username'], data['password']))
        user = c.fetchone()
        if user:
            return "Login successful"
        else:
            return "Invalid username or password"
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

def handle_get_users(data):
    conn = create_connection()
    c = conn.cursor()
    try:
        current_username = data['username']
        c.execute("SELECT username FROM users WHERE username != ?", (current_username,))
        users = [row[0] for row in c.fetchall()]
        return users
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def handle_send_message(data):
    conn = create_connection()
    c = conn.cursor()
    try:
        sender_id = get_user_id(data['from'])
        receiver_id = get_user_id(data['to'])

        c.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
                  (sender_id, receiver_id, data['message']))
        conn.commit()
        return "Message sent"
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

def handle_receive_messages(data):
    conn = create_connection()
    c = conn.cursor()
    try:
        sender_id = get_user_id(data['from'])
        receiver_id = get_user_id(data['to'])

        c.execute('''
            SELECT u.username, m.message
            FROM messages m
            JOIN users u ON u.id = m.sender_id
            WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
            ORDER BY timestamp ASC
        ''', (sender_id, receiver_id, receiver_id, sender_id))

        rows = c.fetchall()
        messages = [{"sender": row[0], "text": row[1]} for row in rows]
        return messages
    except Exception as e:
        return [{"sender": "System", "text": f"Error: {e}"}]
    finally:
        conn.close()

def handle_client(conn, addr):
    data = conn.recv(4096).decode()
    if not data:
        return
    request = json.loads(data)

    if request.get("type") == "signup":
        response = handle_signup(request)
        conn.send(response.encode())
    elif request.get("type") == "signin":
        response = handle_signin(request)
        conn.send(response.encode())
    elif request.get("type") == "get_users":
        response = handle_get_users(request)
        conn.send(json.dumps(response).encode())
    elif request.get("type") == "send_message":
        response = handle_send_message(request)
        conn.send(response.encode())
    elif request.get("type") == "receive_messages":
        response = handle_receive_messages(request)
        conn.send(json.dumps(response).encode())

    conn.close()

def start_server():
    s = socket.socket()
    s.bind(("localhost", 12345))
    s.listen()
    print("Server is running...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()