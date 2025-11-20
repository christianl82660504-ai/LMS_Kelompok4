import tkinter as tk
from tkinter import messagebox
import sqlite3

class LMSApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Manajemen Pembelajaran (LMS) Sederhana")
        master.geometry("500x400") # Ukuran default untuk jendela login
        self.master.config(bg="#f0f0f0")

        # Inisialisasi Database
        self.init_db()

        # Tampilkan Layar Login
        self.show_login_screen()

    # --- Bagian Database (SQLite) ---

    def init_db(self):
        """Menghubungkan ke DB dan membuat tabel jika belum ada."""
        self.conn = sqlite3.connect('lms_simple.db')
        self.cursor = self.conn.cursor()

        # Tabel Pengguna (untuk Login)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                npm TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT,
                role TEXT
            )
        ''')

        # Tabel Kursus
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                code TEXT,
                name TEXT
            )
        ''')

        # Memasukkan data dummy jika tabel masih kosong
        self.cursor.execute('SELECT COUNT(*) FROM users')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO users VALUES ('12345', 'uib', 'agus suwanto', 'Mahasiswa UIB')")
            self.cursor.execute("INSERT INTO users VALUES ('67890', 'uib', 'pieter guy', 'Mahasiswa UIB')")
            self.conn.commit()
            
        self.cursor.execute('SELECT COUNT(*) FROM courses')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO courses (code, name) VALUES ('CS101', 'Algoritma dan Struktur Data')")
            self.cursor.execute("INSERT INTO courses (code, name) VALUES ('MA102', 'Matematika Diskrit')")
            self.cursor.execute("INSERT INTO courses (code, name) VALUES ('IS301', 'Sistem Informasi Manajemen')")
            self.conn.commit()

    def check_login(self, npm, password):
        """Memvalidasi NPM dan Password di database."""
        self.cursor.execute(
            'SELECT name, role FROM users WHERE npm = ? AND password = ?', 
            (npm, password)
        )
        user_data = self.cursor.fetchone()
        return user_data # Mengembalikan (name, role) atau None

    def get_all_courses(self):
        """Mengambil semua daftar kursus dari database."""
        self.cursor.execute('SELECT code, name FROM courses')
        return self.cursor.fetchall()

    # --- Bagian UI (Login Screen) ---

    def show_login_screen(self):
        """Menampilkan antarmuka Login."""
        # Menghapus widget sebelumnya (jika ada)
        for widget in self.master.winfo_children():
            widget.destroy()
            
        self.master.geometry("500x400") # Atur ulang ukuran jendela untuk login
        self.master.title("Login LMS")

        # Frame untuk menampung widget
        login_frame = tk.Frame(self.master, padx=20, pady=20, bg="#ffffff", bd=2, relief=tk.RIDGE)
        login_frame.pack(pady=50)

        # Judul
        tk.Label(login_frame, text="LOGIN LMS", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333").grid(row=0, column=0, columnspan=2, pady=10)

        # NPM
        tk.Label(login_frame, text="NPM:", font=("Arial", 10), bg="#ffffff", fg="#555555").grid(row=1, column=0, sticky="w", pady=5)
        self.npm_entry = tk.Entry(login_frame, width=25, font=("Arial", 10), bd=1, relief=tk.SOLID)
        self.npm_entry.grid(row=1, column=1, padx=10, pady=5)
        self.npm_entry.focus_set()

        # Password
        tk.Label(login_frame, text="Password:", font=("Arial", 10), bg="#ffffff", fg="#555555").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(login_frame, width=25, show="*", font=("Arial", 10), bd=1, relief=tk.SOLID)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Tombol Login
        tk.Button(login_frame, text="Login", command=self.attempt_login, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief=tk.RAISED, bd=3).grid(row=3, column=0, columnspan=2, pady=15, ipadx=10)

    def attempt_login(self):
        """Logika saat tombol Login ditekan."""
        npm = self.npm_entry.get()
        password = self.password_entry.get()

        user_info = self.check_login(npm, password)

        if user_info:
            user_name, user_role = user_info
            messagebox.showinfo("Sukses", f"Selamat Datang, {user_name}!\n({user_role})")
            # Pindah ke Layar Utama
            self.show_main_lms_screen(user_name, user_role, npm)
        else:
            messagebox.showerror("Gagal Login", "NPM atau Password salah.")
            self.password_entry.delete(0, tk.END) # Kosongkan password

    # --- Bagian UI (Main LMS Screen) ---

    def show_main_lms_screen(self, user_name, user_role, npm):
        """Menampilkan antarmuka utama LMS setelah login berhasil."""
        # Menghapus widget sebelumnya
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.geometry("600x400") # Ukuran jendela yang lebih besar
        self.master.title(f"Dashboard LMS | {user_name}")
        self.master.config(bg="#e8e8e8")

        # Header Frame
        header_frame = tk.Frame(self.master, bg="#333333", pady=10)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="SISTEM MANAJEMEN PEMBELAJARAN", font=("Arial", 18, "bold"), fg="white", bg="#333333").pack(side=tk.LEFT, padx=15)
        
        # Tombol Logout
        tk.Button(header_frame, text="Logout", command=self.show_login_screen, bg="#d9534f", fg="white", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=15)

        # Content Frame
        content_frame = tk.Frame(self.master, bg="#e8e8e8", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Info Pengguna
        tk.Label(content_frame, text=f"Halo, {user_name} ({npm}) | Peran: {user_role}", font=("Arial", 12), bg="#e8e8e8", fg="#333333", anchor="w").pack(fill=tk.X, pady=(0, 15))

        # Judul Daftar Kursus
        tk.Label(content_frame, text="Daftar Mata Kuliah yang Tersedia:", font=("Arial", 14, "underline"), bg="#e8e8e8", fg="#0056b3", anchor="w").pack(fill=tk.X, pady=(10, 5))

        # Area Teks untuk Menampilkan Kursus
        course_text = tk.Text(content_frame, height=10, width=50, font=("Courier", 11), bd=1, relief=tk.SUNKEN)
        course_text.pack(fill=tk.BOTH, expand=True)

        # Ambil data kursus dari database dan tampilkan
        courses = self.get_all_courses()
        
        if courses:
            course_text.insert(tk.END, "KODE\t\tNAMA MATA KULIAH\n")
            course_text.insert(tk.END, "--------------------------------------------------\n")
            for code, name in courses:
                # Format output agar terlihat rapi
                course_text.insert(tk.END, f"{code}\t\t{name}\n")
        else:
            course_text.insert(tk.END, "Belum ada mata kuliah yang terdaftar.")
            
        course_text.config(state=tk.DISABLED) # Membuat teks menjadi read-only

# Blok Utama untuk Menjalankan Aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = LMSApp(root)
    root.mainloop()
