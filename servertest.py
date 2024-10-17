import socket
import threading

HOST = '0.0.0.0'  # Mendengarkan semua interface
PORT = 12345  # Port yang digunakan

clients = []
nicknames = []
passwords = ['password123']  # Contoh password, sesuaikan

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        try:
            data, address = server.recvfrom(1024)
            message = f"{address[0]}:{address[1]}: {data.decode('ascii')}"  # Include sender info
            broadcast(message.encode('ascii'))
        except:
            pass  # Handle exceptions appropriately
        
print("Server is listening...")
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

receive()