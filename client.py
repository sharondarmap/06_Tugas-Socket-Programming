import socket
import threading

def receive_messages(sock):
    """Menerima pesan dari server dan mencetaknya."""
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            print(data.decode())
        except:
            print("Koneksi terputus.")
            break

# Konfigurasi koneksi
server_ip = input("Masukkan IP server: ")
server_port = int(input("Masukkan port server: "))
username = input("Masukkan username: ")
password = input("Masukkan password: ")

# Inisialisasi socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Kirim username dan password ke server
client_socket.sendto(f"{username}:{password}".encode(), (server_ip, server_port))

# Menerima respons dari server
response, _ = client_socket.recvfrom(1024)
print(response.decode())

# Jika password salah atau username tidak valid, keluar
if response.decode() != "Terhubung ke chatroom!":
    client_socket.close()
    exit()

# Jalankan thread untuk menerima pesan
thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.daemon = True
thread.start()

# Kirim pesan ke server
try:
    while True:
        message = input()
        client_socket.sendto(message.encode(), (server_ip, server_port))
except KeyboardInterrupt:
    print("Keluar dari chat.")
finally:
    client_socket.close()
