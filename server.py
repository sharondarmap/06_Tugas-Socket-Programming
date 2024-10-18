import socket

# Konfigurasi server
IP = "0.0.0.0"  # Menerima koneksi dari semua interface
PORT = int(input("Masukkan port untuk server: "))
PASSWORD = input("Masukkan password untuk chatroom: ")

# Inisialisasi socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((IP, PORT))

print(f"Server berjalan di {IP}:{PORT}")

clients = {}  # {alamat: username}

def broadcast(message, source_addr):
    """Meneruskan pesan ke semua client kecuali pengirim."""
    for addr in clients:
        if addr != source_addr:
            server_socket.sendto(message.encode(), addr)

while True:
    data, addr = server_socket.recvfrom(1024)
    msg = data.decode()

    if addr not in clients:
        # Memproses pesan registrasi
        username, password = msg.split(":", 1)
        if password != PASSWORD:
            server_socket.sendto("Password salah.".encode(), addr)
        elif username in clients.values():
            server_socket.sendto("Username sudah digunakan.".encode(), addr)
        else:
            clients[addr] = username
            server_socket.sendto("Terhubung ke chatroom!".encode(), addr)
            print(f"{username} bergabung dari {addr}")
    else:
        # Menerima dan meneruskan pesan ke client lain
        username = clients[addr]
        print(f"[{username}] {msg}")
        broadcast(f"[{username}] {msg}", addr)
