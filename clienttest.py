import socket

HOST = '192.168.0.226'  # Ganti dengan IP server
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(1)

nickname = input("Choose a nickname: ")
password = input("Enter password: ")

try:
    client.send(nickname.encode('ascii'))
    response = client.recv(1024).decode('ascii')

    if response == 'TAKEN':
        print("Nickname already taken!")
        exit()

    client.send(password.encode('ascii'))
    response = client.recv(1024).decode('ascii')

    if response == 'INV':
        print("Invalid password!")
        exit()

    print("Connected to server!")

    while True:
        message = f'{nickname}: {input("")}'
        client.sendto(message.encode('ascii'), (HOST, PORT))
        try:
            data, addr = client.recvfrom(1024)
            print(data.decode('ascii'))
        except:
            pass
except:
    print("Unable to connect to the server")