import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import secrets
from datetime import datetime

# KONFIGURASI TEMA
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

#DATABASE MANAGER
class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",     
                password="",      
                database="db_akademi_pti"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Database Terhubung!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error Database", f"Gagal konek ke database: {err}")

    def login_user(self, nomor_induk, password):
        # Cek user di database
        sql = "SELECT * FROM users WHERE nomor_induk = %s AND password = %s"
        self.cursor.execute(sql, (nomor_induk, password))
        user = self.cursor.fetchone()
        
        if user:
            token = secrets.token_hex(16)
            return user, token
        return None, None

    # Admin: Tambah Matkul
    def tambah_matkul(self, kode, nama, sks, semester):
        try:
            sql = "INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, semester) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (kode, nama, sks, semester))
            self.conn.commit()
            return True
        except mysql.connector.Error:
            return False

    # Mahasiswa: Ambil Data KRS/Materi
    def get_krs_mahasiswa(self, mhs_id):
        sql = """
            SELECT mk.kode_mk, mk.nama_mk, mk.sks, mk.semester 
            FROM krs 
            JOIN mata_kuliah mk ON krs.matkul_id = mk.id 
            WHERE krs.mahasiswa_id = %s
        """
        self.cursor.execute(sql, (mhs_id,))
        return self.cursor.fetchall()

    def get_semua_matkul(self):
        self.cursor.execute("SELECT * FROM mata_kuliah")
        return self.cursor.fetchall()

    def ambil_krs(self, mhs_id, matkul_id):
        try:
            sql = "INSERT INTO krs (mahasiswa_id, matkul_id, tahun_ajaran) VALUES (%s, %s, '2024/2025')"
            self.cursor.execute(sql, (mhs_id, matkul_id))
            self.conn.commit()
            return True, "Berhasil ambil KRS"
        except mysql.connector.Error as e:
            return False, str(e)

# APLIKASI UTAMA (UI)
class LMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.db = DatabaseManager() 
        self.user_login = None 
        self.token_akses = None

        self.title("LMS Portal Akademik")
        self.geometry("800x600")

        self.container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.tampilan_login()

    #HALAMAN LOGIN
    def tampilan_login(self):
        for widget in self.container.winfo_children(): widget.destroy()

        frame = ctk.CTkFrame(self.container, width=350, height=400, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Login LMS", font=("Century Gothic", 24, "bold")).pack(pady=(40, 20))

        self.npm_entry = ctk.CTkEntry(frame, placeholder_text="NPM", width=220, height=40)
        self.npm_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=220, height=40)
        self.pass_entry.pack(pady=10)

        btn_login = ctk.CTkButton(frame, text="MASUK", command=self.cek_login, width=220, height=40)
        btn_login.pack(pady=30)

    def cek_login(self):
        nomor = self.npm_entry.get()
        pwd = self.pass_entry.get()

        user, token = self.db.login_user(nomor, pwd)

        if user:
            self.user_login = user
            self.token_akses = token
            messagebox.showinfo("Login Sukses", f"Selamat datang, {user['nama_lengkap']}!")
            self.tampilan_dashboard()
        else:
            messagebox.showerror("Gagal", "NPM / Tidak ada di Database.")

    # Dashboard
    def tampilan_dashboard(self):
        for widget in self.container.winfo_children(): widget.destroy()

        # Sidebar Menu
        sidebar = ctk.CTkFrame(self.container, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(sidebar, text="MENU UTAMA", font=("Arial", 18, "bold")).pack(pady=30)
        ctk.CTkLabel(sidebar, text=f"Role: {self.user_login['role'].upper()}", font=("Arial", 12)).pack(pady=5)
        
        ctk.CTkButton(sidebar, text="Logout", fg_color="#FF5555", hover_color="#BA3333", command=self.tampilan_login).pack(side="bottom", pady=20, padx=10)

        # Area Utama
        main_area = ctk.CTkFrame(self.container, fg_color="transparent")
        main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(main_area, text=f"Halo, {self.user_login['nama_lengkap']}", font=("Arial", 28, "bold")).pack(anchor="w")
        ctk.CTkLabel(main_area, text=f"Token Sesi: {self.token_akses[:15]}...", font=("Consolas", 12), text_color="gray").pack(anchor="w")

        # Tab View untuk Konten
        self.tabview = ctk.CTkTabview(main_area)
        self.tabview.pack(fill="both", expand=True, pady=20)

        if self.user_login['role'] == 'admin':
            self.setup_admin_tabs()
        else:
            self.setup_mahasiswa_tabs()

    # UI ADMIN
    def setup_admin_tabs(self):
        self.tabview.add("Input Matkul")
        self.tabview.add("Input Materi")

        # Tab Input Matkul
        tab_mk = self.tabview.tab("Input Matkul")
        
        ctk.CTkLabel(tab_mk, text="Tambah Mata Kuliah Baru", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.entry_kode = ctk.CTkEntry(tab_mk, placeholder_text="Kode MK (Cth: PTI001)")
        self.entry_kode.pack(pady=5)
        self.entry_nama = ctk.CTkEntry(tab_mk, placeholder_text="Nama Mata Kuliah")
        self.entry_nama.pack(pady=5)
        self.entry_sks = ctk.CTkEntry(tab_mk, placeholder_text="SKS")
        self.entry_sks.pack(pady=5)
        self.entry_smt = ctk.CTkEntry(tab_mk, placeholder_text="Semester")
        self.entry_smt.pack(pady=5)

        ctk.CTkButton(tab_mk, text="Simpan Matkul", command=self.aksi_simpan_matkul).pack(pady=20)

    def aksi_simpan_matkul(self):
        if self.db.tambah_matkul(self.entry_kode.get(), self.entry_nama.get(), self.entry_sks.get(), self.entry_smt.get()):
            messagebox.showinfo("Sukses", "Mata kuliah berhasil ditambahkan!")
        else:
            messagebox.showerror("Gagal", "Kode MK mungkin sudah ada atau input salah.")

    #UI MAHASISWA
    def setup_mahasiswa_tabs(self):
        self.tabview.add("KRS Saya")
        self.tabview.add("Ambil KRS")
        self.tabview.add("LMS & Materi")

        # Tab KRS Saya (Read Only)
        tab_krs = self.tabview.tab("KRS Saya")
        data_krs = self.db.get_krs_mahasiswa(self.user_login['id'])
        
        if not data_krs:
            ctk.CTkLabel(tab_krs, text="Belum ada mata kuliah diambil.").pack(pady=20)
        else:
            # Header Tabel
            header = ctk.CTkFrame(tab_krs, height=30)
            header.pack(fill="x", pady=5)
            ctk.CTkLabel(header, text="KODE", width=80).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="MATA KULIAH", width=200).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="SKS", width=50).pack(side="left", padx=5)

            # Data Tabel
            for mk in data_krs:
                row = ctk.CTkFrame(tab_krs, height=30)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=mk['kode_mk'], width=80).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=mk['nama_mk'], width=200).pack(side="left", padx=5)
                ctk.CTkLabel(row, text=str(mk['sks']), width=50).pack(side="left", padx=5)

        # Tab Ambil KRS (Action)
        tab_ambil = self.tabview.tab("Ambil KRS")
        ctk.CTkLabel(tab_ambil, text="Pilih Mata Kuliah untuk Diambil:").pack(pady=10)
        
        all_matkul = self.db.get_semua_matkul()
        self.combo_matkul = ctk.CTkOptionMenu(tab_ambil, values=[f"{m['id']} - {m['nama_mk']}" for m in all_matkul])
        self.combo_matkul.pack(pady=10)
        
        ctk.CTkButton(tab_ambil, text="Ambil Mata Kuliah Ini", command=self.aksi_ambil_krs).pack(pady=10)

        # Tab LMS
        tab_lms = self.tabview.tab("LMS & Materi")
        ctk.CTkLabel(tab_lms, text="Materi Pembelajaran Tersedia", font=("Arial", 16)).pack(pady=20)
        ctk.CTkLabel(tab_lms, text="(Fitur download materi akan muncul sesuai matkul yg diambil)", text_color="gray").pack()

    def aksi_ambil_krs(self):
        pilihan = self.combo_matkul.get()
        if not pilihan: return
        
        id_matkul = pilihan.split(" - ")[0] # 
        sukses, pesan = self.db.ambil_krs(self.user_login['id'], id_matkul)
        
        if sukses:
            messagebox.showinfo("Sukses", pesan)
            self.tampilan_dashboard()
        else:
            messagebox.showerror("Gagal", "Anda mungkin sudah mengambil matkul ini.")

if __name__ == "__main__":
    app = LMSApp()
    app.mainloop()