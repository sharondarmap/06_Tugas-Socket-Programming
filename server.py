import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

IP = "0.0.0.0"
server_socket, clients = None, {}

# ------- Memulai server untuk menerima pesan dan menangani klien baru -------#
def run_server(port, port_password):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, port))
    log_message(f"Server berjalan di {IP}:{port} ◝(ᵔᗜᵔ)◜")

    while True:
        try:
            msg, addr = server_socket.recvfrom(1024)
            msg = msg.decode()
            if addr not in clients:
                handle_new_client(msg, addr, port_password)
            else:
                broadcast(f"[{clients[addr]}] {msg}", addr)
        except Exception as e:
            log_message(f"Error menerima pesan: {e} ( ˶ˆᗜˆ˵ )")

# ------- Memproses koneksi klien baru dan memverifikasi password port -------#
def handle_new_client(msg, addr, port_password):
    try:
        username, password, client_password = msg.split(":")
        if client_password != port_password:
            server_socket.sendto("Password port salah, ayo coba lagi!!!(ง'̀-'́)ง".encode(), addr)
        else:
            clients[addr] = username  # Store the username with the client's address
            server_socket.sendto("Terhubung ke chatroom!( ˶ˆᗜˆ˵ )".encode(), addr)
            log_message(f"{username} telah terhubung (๑ᵔ⤙ᵔ๑)")
    except ValueError:
        server_socket.sendto("Format pesan tidak valid.".encode(), addr)

# ------- Mengirim pesan ke semua klien kecuali pengirim -------#
def broadcast(message, source_addr):
    for addr in clients:
        if addr != source_addr:
            try:
                server_socket.sendto(message.encode(), addr)
                log_message(f"Pesan dikirim ke {clients[addr]} di {addr}")
            except Exception as e:
                log_message(f"Gagal mengirim pesan ke {addr}: {e} (｡╯︵╰｡)")

# ------- Menambahkan pesan log ke area log GUI -------#
def log_message(message):
    log_area.config(state='normal')
    log_area.insert(tk.END, message + '\n')
    log_area.config(state='disabled')
    log_area.yview(tk.END)

# ------- Memulai thread server dengan port dan password yang diinputkan pengguna -------#
def start_server():
    try:
        threading.Thread(target=run_server, args=(int(port_entry.get()), password_entry.get()), daemon=True).start()
        start_button.config(state=tk.DISABLED)
    except Exception as e:
        log_message(f"Error memulai server: {e}")

window = tk.Tk()
window.title("Chatroom Server")
window.geometry("800x600")
window.configure(bg='#404040')

frame = tk.Frame(window, bg='#404040')
frame.pack(expand=True)

tk.Label(frame, text="┏━━✦❘༻Selamat Datang༺❘✦━━┓", font=("Adobe Garamond Pro Bold", 15, "bold"), bg='#404040', fg='white').grid(row=0, columnspan=2)
tk.Label(frame, text="Di", font=("Adobe Garamond Pro Bold", 10, "bold"), bg='#404040', fg='white').grid(row=1, columnspan=2)
tk.Label(frame, text="ˏˋ°•*⁀➷SERVER PAGE ༊*·˚", font=("Adobe Garamond Pro Bold", 20, "bold"), bg='#404040', fg='white').grid(row=2, columnspan=2, pady=(0,20))
tk.Label(frame, text="Port:", bg='#404040', fg='white').grid(row=3, column=0)
port_entry = tk.Entry(frame, bg='#b8b8b8', fg='black')
port_entry.grid(row=3, column=1)

tk.Label(frame, text="Password:", bg='#404040', fg='white').grid(row=4, column=0)
password_entry = tk.Entry(frame, show="*", bg='#b8b8b8', fg='black')
password_entry.grid(row=4, column=1)

start_button = tk.Button(frame, text="Start Server", command=start_server, bg='#a1b384', fg='black')
start_button.grid(row=5, columnspan=2, pady=10)

log_area = scrolledtext.ScrolledText(frame, width=80, height=20, state='disabled', bg='#404040', fg='white')
log_area.grid(row=6, columnspan=2, pady=10)

window.mainloop()
