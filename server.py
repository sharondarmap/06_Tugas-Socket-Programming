import socket

SERVER_IP = "0.0.0.0"  # Menerima koneksi dari semua IP
SERVER_PORT = 12345
BUFFER_SIZE = 1024

clients = {}  # Menyimpan alamat client dan username-nya

def start_server():
    # Membuat socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f"Server running on {SERVER_IP}:{SERVER_PORT}")

    while True:
        # Menerima pesan dari client
        message, client_address = server_socket.recvfrom(BUFFER_SIZE)
        decoded_message = message.decode()
        print(f"Received from {client_address}: {decoded_message}")

        # Parsing username dan pesan
        if decoded_message.startswith("JOIN:"):
            username = decoded_message.split(":")[1]
            clients[client_address] = username
            print(f"{username} joined the chat")
            continue

        # Meneruskan pesan ke semua client kecuali pengirim
        for addr, user in clients.items():
            if addr != client_address:
                server_socket.sendto(message, addr)

if __name__ == "__main__":
    start_server()
