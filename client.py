import socket
import threading

SERVER_IP = input("Enter server IP: ")
SERVER_PORT = int(input("Enter server port: "))
PASSWORD = "secret123"  # Password hardcoded

BUFFER_SIZE = 1024

def receive_messages(client_socket):
    while True:
        try:
            message, _ = client_socket.recvfrom(BUFFER_SIZE)
            print(message.decode())
        except:
            print("Connection error.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Meminta password dari pengguna
    password = input("Enter chatroom password: ")
    if password != PASSWORD:
        print("Incorrect password. Access denied.")
        return

    username = input("Enter your username: ")

    # Mengirim pesan JOIN ke server
    join_message = f"JOIN:{username}"
    client_socket.sendto(join_message.encode(), (SERVER_IP, SERVER_PORT))

    # Membuat thread untuk menerima pesan dari server
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("You have joined the chat. Type your messages below.")

    while True:
        message = input()
        if message.lower() == "quit":
            print("Exiting chat...")
            break

        # Mengirim pesan ke server
        full_message = f"{username}: {message}"
        client_socket.sendto(full_message.encode(), (SERVER_IP, SERVER_PORT))

    client_socket.close()

if __name__ == "__main__":
    start_client()
