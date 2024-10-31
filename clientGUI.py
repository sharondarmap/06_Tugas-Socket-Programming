import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

client_socket, login_frame, chat_frame, text_area, message_entry = None, None, None, None, None
server_ip, server_port = None, None

def create_login_frame(window):
    global login_frame, server_ip_entry, server_port_entry, username_entry, password_entry
    login_frame = tk.Frame(window, padx=20, pady=20, bg='#404040')
    login_frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(login_frame, text="┏━━✦❘༻Selamat Datang༺❘✦━━┓", font=("Adobe Garamond Pro Bold", 15, "bold"), bg='#404040', fg='white').grid(row=0, columnspan=2)
    tk.Label(login_frame, text="Di", font=("Adobe Garamond Pro Bold", 10, "bold"), bg='#404040', fg='white').grid(row=1, columnspan=2)
    tk.Label(login_frame, text="LOGIN PAGE (๑'ᵕ'๑)⸝*", font=("Adobe Garamond Pro Bold", 20, "bold"), bg='#404040', fg='white').grid(row=2, columnspan=2, pady=30)

    labels = ["IP Server", "Port Server", "Username", "Password"]
    entries = []
    for i, text in enumerate(labels):
        tk.Label(login_frame, text=text, font=("Arial", 10, "bold"), bg='#404040', fg='white').grid(row=i*2+3, column=0, columnspan=2, pady=(5, 2), sticky='s')
        entry = tk.Entry(login_frame, width=30, show="*" if i == 3 else "")
        entry.grid(row=i*2+4, column=0, columnspan=2, pady=(0, 10))
        entries.append(entry)
    
    server_ip_entry, server_port_entry, username_entry, password_entry = entries

    connect_button = tk.Button(login_frame, text="Connect", width=15, command=lambda: on_connect(server_ip_entry.get(), server_port_entry.get(), username_entry.get(), password_entry.get()))
    connect_button.grid(row=11, column=0, columnspan=2, pady=10)

def create_chat_frame(window):
    global chat_frame, text_area, message_entry
    chat_frame = tk.Frame(window, padx=20, pady=20, bg='#404040')
    chat_frame.pack(expand=True, fill="both")

    tk.Label(chat_frame, text="Anda Berada di", font=("Adobe Garamond Pro Bold", 15, "bold"), fg="white", bg='#404040').pack(pady=(0, 0))    
    tk.Label(chat_frame, text="ꕤ⭒๋࣭ ⭑ROOM CHAT ⋆˚✿˖°", font=("Adobe Garamond Pro Bold", 25, "bold"), fg="white", bg='#404040').pack(pady=(0, 10))

    text_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED, width=100, height=25)
    text_area.pack(expand=True, fill="both", padx=10, pady=(10, 0))

    message_frame = tk.Frame(chat_frame)
    message_frame.pack(fill="x", padx=10, pady=(0, 10))
    message_entry = tk.Entry(message_frame, width=80)
    message_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5), pady=10)
    tk.Button(message_frame, text="Kirim", width=10, command=send_message).pack(side=tk.RIGHT)

def on_connect(ip, port, username, password):
    global client_socket, server_ip, server_port
    if not username or not password:
        messagebox.showwarning("Warning", "Username dan password tidak boleh kosong.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(f"{username}:{password}".encode(), (ip, int(port)))
    response, _ = client_socket.recvfrom(1024)

    if response.decode() == "Terhubung ke chatroom!( ˶ˆᗜˆ˵ )":
        server_ip, server_port = ip, int(port)
        login_frame.destroy()
        create_chat_frame(window)
        threading.Thread(target=receive_messages, daemon=True).start()
        update_chat_area(response.decode())
    else:
        messagebox.showwarning("Warning", response.decode())

def receive_messages():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            message = message.decode()
            if message:
                update_chat_area(message)
        except Exception as e:
            update_chat_area("Koneksi terputus. Silakan coba sambungkan kembali.")
            break

def update_chat_area(message):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, message + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

def send_message():
    message = message_entry.get()
    if message:
        update_chat_area(f"[Anda]: {message}")
        client_socket.sendto(message.encode(), (server_ip, server_port))
        message_entry.delete(0, tk.END)

window = tk.Tk()
window.title("Chatroom Client")
window.geometry("800x600")  
window.configure(bg='#404040')
create_login_frame(window)
window.mainloop()
