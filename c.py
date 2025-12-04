import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

# KONFIGURASI TEMA
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",      # Sesuaikan user XAMPP 
                database="db_akademi_pti"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Database Terhubung!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error Database", f"Gagal konek ke database: {err}")

class LMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LMS Mahasiswa")
        self.geometry("600x450")
        try:
            self.state("zoomed")
        except Exception:
            pass

        # track current logged-in NPM
        self.current_npm = None

        self.container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.tampilan_login()

    def tampilan_login(self):
        for widget in self.container.winfo_children(): widget.destroy()

        frame = ctk.CTkFrame(self.container, width=350, height=350, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="LMS LOGIN", font=("Century Gothic", 24, "bold")).pack(pady=(40, 20))

        self.npm_entry = ctk.CTkEntry(frame, placeholder_text="Masukkan NPM", width=220, height=40)
        self.npm_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=220, height=40)
        self.pass_entry.pack(pady=10)

        btn_login = ctk.CTkButton(frame, text="MASUK SEKARANG", command=self.cek_login, width=220, height=40)
        btn_login.pack(pady=30)

    def tampilan_dashboard(self, npm=None):
        for widget in self.container.winfo_children(): widget.destroy()

        sidebar = ctk.CTkFrame(self.container, width=150, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(sidebar, text="MENU LMS", font=("Arial", 16, "bold")).pack(pady=30)
        ctk.CTkButton(sidebar, text="Home", fg_color="transparent", border_width=1, command=self.tampilan_home).pack(pady=5, padx=10)
        ctk.CTkButton(sidebar, text="Dashboard", fg_color="transparent", border_width=1, command=lambda: self.tampilan_dashboard(self.current_npm)).pack(pady=5, padx=10)
        ctk.CTkButton(sidebar, text="Logout", fg_color="#FF5555", hover_color="#BA3333", command=self.logout).pack(side="bottom", pady=20, padx=10)

        main_area = ctk.CTkFrame(self.container, fg_color="transparent")
        main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # resolve npm: param takes precedence, otherwise use current_npm
        npm = npm or self.current_npm
        if npm is None:
            # no user to show; redirect to login
            messagebox.showinfo("Info", "Silakan login terlebih dahulu.")
            self.tampilan_login()
            return

        nama = data_mahasiswa.get(npm, npm)
        ctk.CTkLabel(main_area, text=f"Halo, {nama}!", font=("Arial", 28, "bold")).pack(anchor="w")
        ctk.CTkLabel(main_area, text="Selamat datang di LMS.", font=("Arial", 14)).pack(anchor="w", pady=5)
        
        info_card = ctk.CTkFrame(main_area, height=100, fg_color="#2B2B2B")
        info_card.pack(fill="x", pady=20)
        ctk.CTkLabel(info_card, text="Status : Online", text_color="white").place(relx=0.5, rely=0.5, anchor="center")

    def cek_login(self):
        npm = self.npm_entry.get()
        pwd = self.pass_entry.get()
        # basic validation
        if not npm or not pwd:
            messagebox.showwarning("Input Required", "Masukkan NPM dan Password.")
            return

        # verify user exists
        if npm not in DB_USERS:
            messagebox.showerror("Akses Ditolak", "NPM tidak terdaftar.")
            return

        if DB_USERS.get(npm) == pwd:
            # successful login: store current user and show dashboard
            self.current_npm = npm
            self.tampilan_dashboard(npm)
        else:
            messagebox.showerror("Akses Ditolak", "NPM atau Password Anda salah.")

    def tampilan_home(self):
        # show a simple home/overview for the logged-in user
        for widget in self.container.winfo_children(): widget.destroy()

        # ensure user is logged in
        if not self.current_npm:
            messagebox.showinfo("Info", "Silakan login terlebih dahulu.")
            self.tampilan_login()
            return

        frame = ctk.CTkFrame(self.container, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        nama = data_mahasiswa.get(self.current_npm, self.current_npm)
        ctk.CTkLabel(frame, text=f"Beranda - {nama}", font=("Arial", 20, "bold")).pack(anchor="w", pady=(0,10))

        # basic overview cards
        card1 = ctk.CTkFrame(frame, fg_color="#2B2B2B", height=80)
        card1.pack(fill="x", pady=5)
        ctk.CTkLabel(card1, text="Status: Online", text_color="white").place(relx=0.01, rely=0.5, anchor="w")

        card2 = ctk.CTkFrame(frame, fg_color="#2B2B2B", height=80)
        card2.pack(fill="x", pady=5)
        ctk.CTkLabel(card2, text="Notifikasi: Tidak ada pemberitahuan baru", text_color="white").place(relx=0.01, rely=0.5, anchor="w")

        # quick actions
        actions = ctk.CTkFrame(frame, fg_color="transparent")
        actions.pack(fill="x", pady=10)
        ctk.CTkButton(actions, text="Buka Dashboard", command=lambda: self.tampilan_dashboard(self.current_npm)).pack(side="left", padx=5)
        ctk.CTkButton(actions, text="Logout", fg_color="#FF5555", hover_color="#BA3333", command=self.logout).pack(side="left", padx=5)

    def logout(self):
        # clear state and return to login
        self.current_npm = None
        self.tampilan_login()

if __name__ == "__main__":
    app = LMSApp()
    app.mainloop()






