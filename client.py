import socket
import threading

def receive_messages(sock):
    """Menerima pesan dari server dan mencetaknya."""
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            print(data.decode())
        except:
            print("Maaf koneksi telah terputus ૮(˶ㅠ︿ㅠ)ა")
            break

# Konfigurasi koneksi
server_ip = input("Masukkan IP Server : ")
server_port = int(input("Masukkan Port Server : "))

# Inisialisasi socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Proses login
while True:
    username = input("Masukkan Username : ")
    password = input("Masukkan Password : ")

    # Kirim username dan password ke server
    client_socket.sendto(f"{username}:{password}".encode(), (server_ip, server_port))

    # Menerima respons dari server
    response, _ = client_socket.recvfrom(1024)
    response_msg = response.decode()
    print(response_msg)

    # Jika terhubung ke chatroom, keluar dari loop
    if response_msg == "Selamat Anda telah terhubung ke chatroom!( ˶ˆᗜˆ˵ )":
        break

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
