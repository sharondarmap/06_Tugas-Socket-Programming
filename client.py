import socket
import threading


def receive_messages(sock):
    """Menerima pesan dari server dan mencetaknya."""
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            message = data.decode()
            
            if message.isdigit():
                ack_num = int(message)
                print(f"Received ACK for sequence {ack_num}")
                
            else:
                print(message)
        except:
            print("Maaf koneksi telah terputus ૮(˶ㅠ︿ㅠ)ა")
            break

def send_with_ack(sock, message, server_addr, sequence_number):
    """Kirim pesan dengan nomor urut dan tunggu ACK."""
    attempts = 0
    while attempts < 5:
        try:
            packet = f"{sequence_number}:{message}"
            sock.sendto(packet.encode(), server_addr)

            # Tunggu ACK
            sock.settimeout(2)
            ack, _ = sock.recvfrom(1024)
            ack_num = int(ack.decode())
            
            # Jika ACK sesuai dengan nomor urut, kirim berhasil
            if ack_num == sequence_number:
                sock.settimeout(None)
                return True
        except socket.timeout:
            attempts += 1
            print(f"Timeout, mengirim ulang pesan (Percobaan {attempts}/5)")
    return False

# Konfigurasi koneksi
server_ip = input("Masukkan IP Server : ")
server_port = int(input("Masukkan Port Server : "))
server_addr = (server_ip, server_port)

# Inisialisasi socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Proses login
while True:
    username = input("Masukkan Username : ")
    password = input("Masukkan Password : ")

    # Kirim username dan password ke server
    client_socket.sendto(f"{username}:{password}".encode(), server_addr)
    # Menerima respons dari server
    response, _ = client_socket.recvfrom(1024)
    response_msg = response.decode()
    print(response_msg)

    # Jika terhubung ke chatroom, keluar dari loop
    if response_msg == "Selamat Anda telah terhubung ke chatroom.":
        break

sequence_number = 1

# Jalankan thread untuk menerima pesan
thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.daemon = True
thread.start()

# Kirim pesan ke server
try:
    while True:
        message = input()
        if send_with_ack(client_socket, message, server_addr, sequence_number):
            sequence_number += 1  # Increment sequence number after successful send
except KeyboardInterrupt:
    print("Keluar dari chat.")
finally:
    client_socket.close()
