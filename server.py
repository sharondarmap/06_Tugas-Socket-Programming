import socket
import threading

# Konfigurasi server
IP = "0.0.0.0"  # Menerima koneksi dari semua interface
PORT = int(input("Masukkan port untuk server : "))
PASSWORD = input("Masukkan password rahasia untuk chatroom : ")

# Inisialisasi socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((IP, PORT))

print(f"Server berjalan di {IP}:{PORT}")

clients = {}  # {alamat: [username, sequence_number]}

def send_with_ack(message, addr, sequence_number):
    """Mengirim pesan dengan nomor urut dan menunggu ACK."""
    attempts = 0
    while attempts < 5:
        try:
            # Tambahkan nomor urut ke pesan
            packet = f"{sequence_number}:{message}"
            server_socket.sendto(packet.encode(), addr)

            # Tunggu ACK dari client
            server_socket.settimeout(2)
            ack, _ = server_socket.recvfrom(1024)
            ack_num = int(ack.decode())

            # Jika ACK sesuai dengan nomor urut, kirim berhasil
            if ack_num == sequence_number:
                server_socket.settimeout(None)
                return True
        except (socket.timeout, ValueError):
            attempts += 1
            print(f"Timeout, mengirim ulang pesan ke {addr} (Percobaan {attempts}/5)")
    
    server_socket.settimeout(None)
    return True

def broadcast(message, source_addr, sequence_number):
    """Meneruskan pesan ke semua client kecuali pengirim dengan menggunakan ACK."""
    for addr in clients:
        if addr != source_addr:
            send_with_ack(message, addr, sequence_number)
            
def handle_client_reg(data, addr):
    username, password = data.split(":", 1)
    
    if password != PASSWORD:
        server_socket.sendto("Password salah, silakan coba lagi.".encode(), addr)
    elif username in [user[0] for user in clients.values()]:
        server_socket.sendto("Username telah digunakan, silakan coba lagi.".encode(), addr)
    else:
        clients[addr] = [username, 1]
        server_socket.sendto("Selamat Anda telah terhubung ke chatroom.".encode(), addr)
        print(f"{username} bergabung dari {addr}")

while True:
    server_socket.settimeout(None)
    data, addr = server_socket.recvfrom(1024)
    msg = data.decode()

    if addr not in clients:
        handle_client_reg(msg, addr)
    else:
        # Menerima dan meneruskan pesan ke client lain
        username, sequence_number = clients[addr]
        try:
            packet_seq, msg_text = msg.split(":", 1)
            packet_seq = int(packet_seq)
        except ValueError:
            print("Received malformed packet; discarding.")
            continue
        
        if packet_seq == sequence_number:
            print(f"[{username}] {msg_text}")
            
            # Kirim ACK ke pengirim
            server_socket.sendto(str(packet_seq).encode(), addr)
            clients[addr][1] += 1  # Increment the sequence number for the next message
            broadcast(f"[{username}] {msg_text}", addr, sequence_number)
        else:
            print(f"Received out-of-order packet from {username} at {addr}, discarding.")
