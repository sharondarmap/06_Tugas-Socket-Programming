import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

class ClientChatRoom:
    def __init__(self, window):
        self.client_socket = None
        self.server_ip = None
        self.server_port = None
        self.window = window
        self.text_area = None
        self.message_entry = None
        self.create_login_frame()

    def create_login_frame(self):
        login_frame = tk.Frame(self.window, padx=20, pady=20, bg='#404040')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(login_frame, text="┏━━✦❘༻Selamat Datang༺❘✦━━┓", font=("Adobe Garamond Pro Bold", 15, "bold"), bg='#404040', fg='white').grid(row=0, columnspan=2)
        tk.Label(login_frame, text="Di", font=("Adobe Garamond Pro Bold", 10, "bold"), bg='#404040', fg='white').grid(row=1, columnspan=2)
        tk.Label(login_frame, text="LOGIN PAGE (๑'ᵕ'๑)⸝*", font=("Adobe Garamond Pro Bold", 20, "bold"), bg='#404040', fg='white').grid(row=2, columnspan=2, pady=(0, 20))

        labels = ["IP Server", "Port Server", "Username", "Password"]
        entries = []
        for i, text in enumerate(labels):
            tk.Label(login_frame, text=text, font=("Adobe Garamond Pro Bold", 10, "bold"), bg='#404040', fg='white').grid(row=i*2+3, column=0, columnspan=2, pady=(5, 2), sticky='s')
            entry = tk.Entry(login_frame, width=30, show="*" if i == 3 else "")
            entry.grid(row=i*2+4, column=0, columnspan=2, pady=(0, 10))
            entries.append(entry)
        
        self.server_ip_entry, self.server_port_entry, self.username_entry, self.password_entry = entries
        tk.Button(login_frame, text="Connect", width=15, command=self.on_connect).grid(row=11, column=0, columnspan=2, pady=10)

    def create_chat_frame(self):
        chat_frame = tk.Frame(self.window, padx=20, pady=20, bg='#404040')
        chat_frame.pack(expand=True, fill="both")

        tk.Label(chat_frame, text="Anda Berada di", font=("Adobe Garamond Pro Bold", 15, "bold"), fg="white", bg='#404040').pack(pady=(0, 0))    
        tk.Label(chat_frame, text="ꕤ⭒๋࣭ ⭑ROOM CHAT ⋆˚✿˖°", font=("Adobe Garamond Pro Bold", 25, "bold"), fg="white", bg='#404040').pack(pady=(0, 10))

        self.text_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED, width=100, height=25)
        self.text_area.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        message_frame = tk.Frame(chat_frame)
        message_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.message_entry = tk.Entry(message_frame, width=80)  # Use self.message_entry
        self.message_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5), pady=10)
        self.message_entry.bind("<Return>", lambda event: self.send_message())  
        
        tk.Button(message_frame, text="Kirim", width=10, command=self.send_message).pack(side=tk.RIGHT)

    def on_connect(self):
        ip = self.server_ip_entry.get()
        port = self.server_port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Username dan password tidak boleh kosong.")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.sendto(f"{username}:{password}".encode(), (ip, int(port)))
        response, _ = self.client_socket.recvfrom(1024)

        if response.decode() == "Terhubung ke chatroom!( ˶ˆᗜˆ˵ )":
            self.server_ip, self.server_port = ip, int(port)
            self.create_chat_frame()
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.update_chat_area(response.decode())
        else:
            messagebox.showwarning("Warning", response.decode())

    def receive_messages(self):
        try:
            while True:
                message, _ = self.client_socket.recvfrom(1024)
                message = message.decode()
                if message:
                    self.update_chat_area(message)
        except Exception:
            self.update_chat_area("Koneksi terputus. Silakan coba sambungkan kembali.")

    def update_chat_area(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.update_chat_area(f"[Anda]: {message}")
            self.client_socket.sendto(message.encode(), (self.server_ip, self.server_port))
            self.message_entry.delete(0, tk.END)

    def startchat(self):
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            print("Goodbye.")
            if self.client_socket:
                self.client_socket.close()

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Chatroom Client")
    window.geometry("800x600")  
    window.configure(bg='#404040')

    app = ClientChatRoom(window)
    app.startchat()
