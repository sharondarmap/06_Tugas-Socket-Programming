import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import csv
import os

class ClientChatRoom:

    # ------- Menginisialisasi variabel dan menampilkan frame awal -------#
    def __init__(self, window):
        self.client_socket = None
        self.server_ip = None
        self.server_port = None
        self.window = window
        self.text_area = None
        self.message_entry = None
        self.create_start_frame()
 
    # ------- Menampilkan menu awal dengan opsi login dan registrasi -------#
    def create_start_frame(self):
        start_frame = tk.Frame(self.window, padx=20, pady=20, bg='#404040')
        start_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(start_frame, text="┏━━✦❘༻Selamat Datang༺❘✦━━┓", font=("Adobe Garamond Pro Bold", 15, "bold"), bg='#404040', fg='white').grid(row=0, columnspan=2, pady=(0, 10))
        tk.Button(start_frame, text="Login", width=15, command=self.create_login_frame).grid(row=1, column=0, pady=10)
        tk.Button(start_frame, text="Register", width=15, command=self.create_register_frame).grid(row=1, column=1, pady=10)

    # ------- Menampilkan form registrasi pengguna baru -------#
    def create_register_frame(self):
        register_frame = tk.Frame(self.window, padx=20, pady=20, bg='#404040')
        register_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(register_frame, text="Register", font=("Adobe Garamond Pro Bold", 20, "bold"), bg='#404040', fg='white').grid(row=0, columnspan=2, pady=(0, 20))

        labels = ["Username", "Password"]
        entries = []
        for i, text in enumerate(labels):
            tk.Label(register_frame, text=text, font=("Adobe Garamond Pro Bold", 10, "bold"), bg='#404040', fg='white').grid(row=i + 1, column=0, pady=(5, 2), sticky='s')
            entry = tk.Entry(register_frame, width=30, show="*" if i == 1 else "")
            entry.grid(row=i + 1, column=1, pady=(5, 10))
            entries.append(entry)

        self.username_entry, self.password_entry = entries
        tk.Button(register_frame, text="Register", width=15, command=self.register_user).grid(row=3, columnspan=2, pady=10)

    # ------- Memvalidasi dan menyimpan kredensial pengguna baru ke CSV -------#
    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("OooHHH NoOOOooo", "Username dan password tidak boleh kosong yaaa(੭˃ᴗ˂)੭.")
            return
        if os.path.exists('users.csv'):
            with open('users.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username:
                        messagebox.showwarning("OooHHH NoOOOooo", "Username sudah terdaftar. silakan gunakan username lain yaaa(∩˃o˂∩)")
                        return
        with open('users.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

        messagebox.showinfo("Info", "Registrasi berhasil! Silakan login.")
        self.create_login_frame()

    # ------- Menampilkan form login untuk menghubungkan ke server -------#
    def create_login_frame(self):
        login_frame = tk.Frame(self.window, padx=20, pady=20, bg='#404040')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(login_frame, text="LOGIN PAGE (๑'ᵕ'๑)⸝*", font=("Adobe Garamond Pro Bold", 20, "bold"), bg='#404040', fg='white').grid(row=0, columnspan=2, pady=(0, 20))

        labels = ["IP Server", "Port Server", "Username", "Password", "Port Password"]
        entries = []
        for i, text in enumerate(labels):
            tk.Label(login_frame, text=text, font=("Adobe Garamond Pro Bold", 10, "bold"), bg='#404040', fg='white').grid(row=i + 1, column=0, pady=(5, 2), sticky='s')
            entry = tk.Entry(login_frame, width=30, show="*" if i in (3, 4) else "")
            entry.grid(row=i + 1, column=1, pady=(5, 10))
            entries.append(entry)

        self.server_ip_entry, self.server_port_entry, self.username_entry, self.password_entry, self.port_password_entry = entries
        tk.Button(login_frame, text="Connect", width=15, command=self.on_connect).grid(row=6, columnspan=2, pady=10)

    # ------- Memvalidasi login dan menghubungkan ke server jika kredensial benar -------#
    def on_connect(self):
        ip = self.server_ip_entry.get()
        port = self.server_port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        port_password = self.port_password_entry.get()

        if not username or not password or not port_password:
            messagebox.showwarning("OooHHH NoOOOooo", "Username, password, atau port password tidak boleh kosong yaaa (╥﹏╥)")
            return
        if os.path.exists('users.csv'):
            with open('users.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                if not any(row[0] == username and row[1] == password for row in reader):
                    messagebox.showwarning("OooHHH NoOOOooo", "Username atau password kamu masih salah (ᗒᗣᗕ)՞")
                    return
        else:
            messagebox.showwarning("OooHHH NoOOOooo", "Akun kamu belum terdaftar, ayoo registrasi dulu ( •̯́ ^ •̯̀)")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.sendto(f"{username}:{password}:{port_password}".encode(), (ip, int(port))) 
        response, _ = self.client_socket.recvfrom(1024)

        if response.decode() == "Terhubung ke chatroom!( ˶ˆᗜˆ˵ )":
            self.server_ip, self.server_port = ip, int(port)
            self.create_chat_frame()
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.update_chat_area(response.decode())
        else:
            messagebox.showwarning("OooHHH NoOOOooo", response.decode())

    # ------- Menampilkan antarmuka utama chat dengan area pesan dan kolom entri -------#
    def create_chat_frame(self):
        # Main chat frame
        chat_frame = tk.Frame(self.window, padx=20, pady=20, bg='#404040')
        chat_frame.pack(expand=True, fill="both")

        tk.Label(chat_frame, text="Anda Berada di", font=("Adobe Garamond Pro Bold", 15, "bold"), fg="white", bg='#404040').pack(pady=(0, 0))    
        tk.Label(chat_frame, text="ꕤ⭒๋࣭ ⭑ROOM CHAT ⋆˚✿˖°", font=("Adobe Garamond Pro Bold", 25, "bold"), fg="white", bg='#404040').pack(pady=(0, 10))
   
        self.text_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED, width=100, height=25)
        self.text_area.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        message_frame = tk.Frame(chat_frame)
        message_frame.pack(fill="x", padx=10, pady=(0, 10))
    
        self.message_entry = tk.Entry(message_frame, width=80)
        self.message_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5), pady=10)
        self.message_entry.bind("<Return>", lambda event: self.send_message())  
        tk.Button(message_frame, text="Kirim", width=10, command=self.send_message).pack(side=tk.RIGHT)

    # ------- Mengirim pesan ke server dan memperbarui tampilan chat -------#
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.update_chat_area(f"[Anda]: {message}")
            self.client_socket.sendto(message.encode(), (self.server_ip, self.server_port))
            self.message_entry.delete(0, tk.END)

    # ------- Mendengarkan pesan dari server dan menampilkannya di area chat -------#
    def receive_messages(self):
        while True:
            try:
                message, _ = self.client_socket.recvfrom(1024)
                self.update_chat_area(message.decode())
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    # ------- Menambahkan pesan baru ke area tampilan chat -------#
    def update_chat_area(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)

    # ------- Memulai loop GUI Tkinter dan menangani penutupan aplikasi -------#
    def startchat(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  
        self.window.mainloop()

    # ------- Menutup koneksi dan aplikasi saat jendela ditutup -------#
    def on_closing(self):
        print("Bye, See U(っᵔ◡ᵔ)っ")
        if self.client_socket:
            self.client_socket.close()
        self.window.destroy()

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Chatroom Client")
    window.geometry("800x600")
    window.configure(bg='#404040')

    app = ClientChatRoom(window)
    app.startchat()
