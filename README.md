import customtkinter as ctk
from tkinter import messagebox, ttk


DB_USERS = {
    "2532076": "uib",
    "2532060": "uib",
    "2532057": "uib",
    "2532059": "uib",
    "2532021": "uib",
}

data_mahasiswa = {
    "2532076": "Christian Lombu",
    "2532060": "Pieter Nicolaas",
    "2532057": "Royyan Putra",
    "2532059": "Agus Suwanto",
    "2532021": "Steven Kevin",
}

tabel_users = [
    ["2532076", "Christian Lombu", "uib"],
    ["2532060", "Pieter Nicolaas", "uib"],
    ["2532057", "Royyan Putra", "uib"],
]

tabel_mk = [
    ["25001", "Pengantar Teknologi Informasi", 3],
    ["25002", "Teknik Pemograman", 3],
    ["25003", "Bahasa Inggris", 2],
    ["25004", "Agama", 2],
    ["25004", "Bahasa Indonesia", 2],
    ["25005", "Kalkulus dan Aljabar Linier", 3],
    ["25006", "Lab.Teknik Pemograman", 1],
    ["25007", "Arsitektur dan Organisasi Komputer", 3]
]

tabel_nilai = []


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class LMSApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("LMS Portal Mahasiswa")
        self.geometry("900x600")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.tampilan_login()

    def tampilan_login(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.container, width=350, height=350, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="LMS LOGIN", font=("Century Gothic", 24, "bold")).pack(pady=(40, 20))

        self.npm_entry = ctk.CTkEntry(frame, placeholder_text="Masukkan NPM", width=220, height=40)
        self.npm_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=220, height=40)
        self.pass_entry.pack(pady=10)

        btn_login = ctk.CTkButton(frame, text="MASUK SEKARANG", command=self.cek_login, width=220, height=40)
        btn_login.pack(pady=30)

    def cek_login(self):
        npm = self.npm_entry.get()
        pwd = self.pass_entry.get()

        if DB_USERS.get(npm) == pwd:
            nama = data_mahasiswa.get(npm, "Mahasiswa")
            self.tampilan_main(nama)
        else:
            messagebox.showerror("Akses Ditolak", "NPM atau Password salah.")

    def tampilan_main(self, nama):
        for widget in self.container.winfo_children():
            widget.destroy()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.container, width=180)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="MENU", font=("Arial", 16, "bold")).pack(pady=20)

        # Tombol navigasi
        ctk.CTkButton(self.sidebar, text="Dashboard", command=self.page_dashboard).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Users", command=self.page_users).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Mata Kuliah", command=self.page_mk).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Nilai", command=self.page_nilai).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Setting", command=self.page_setting).pack(pady=5)

        ctk.CTkButton(self.sidebar, text="Logout", fg_color="#FF5555", hover_color="#BB3333",
                      command=self.tampilan_login).pack(side="bottom", pady=20)

        # Area utama
        self.main_area = ctk.CTkFrame(self.container, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True)

        self.nama_login = nama
        self.page_dashboard()

    def page_dashboard(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text=f"Halo, {self.nama_login}", font=("Arial", 28, "bold")).pack(anchor="w")
        ctk.CTkLabel(self.main_area, text="Selamat datang di Dashboard LMS", font=("Arial", 14)).pack(anchor="w")

        # Statistik
        card = ctk.CTkFrame(self.main_area)
        card.pack(fill="x", pady=20)

        total_mhs = len(tabel_users)
        total_mk = len(tabel_mk)
        total_nilai = len(tabel_nilai)

        ctk.CTkLabel(card, text=f"Total Mahasiswa: {total_mhs}", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(card, text=f"Total Mata Kuliah: {total_mk}", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(card, text=f"Total Nilai Input: {total_nilai}", font=("Arial", 16)).pack(pady=5)

    def page_users(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Manajemen Users", font=("Arial", 22, "bold")).pack()

        table = ttk.Treeview(self.main_area, columns=("npm", "nama", "pass"), show="headings")
        table.heading("npm", text="NPM")
        table.heading("nama", text="Nama")
        table.heading("pass", text="Password")
        table.pack(fill="x", padx=10, pady=10)

        for row in tabel_users:
            table.insert("", "end", values=row)

        # Form Tambah User
        form = ctk.CTkFrame(self.main_area)
        form.pack(fill="x", pady=10)

        npm_e = ctk.CTkEntry(form, placeholder_text="NPM")
        nama_e = ctk.CTkEntry(form, placeholder_text="Nama")
        pass_e = ctk.CTkEntry(form, placeholder_text="Password")

        npm_e.pack(side="left", padx=5)
        nama_e.pack(side="left", padx=5)
        pass_e.pack(side="left", padx=5)

        def tambah_user():
            npm = npm_e.get()
            nama = nama_e.get()
            ps = pass_e.get()
            if npm and nama and ps:
                tabel_users.append([npm, nama, ps])
                self.page_users()

        ctk.CTkButton(form, text="Tambah", command=tambah_user).pack(side="left", padx=10)

    def page_mk(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Daftar Mata Kuliah", font=("Arial", 22, "bold")).pack()

        table = ttk.Treeview(self.main_area, columns=("kode", "nama", "sks"), show="headings")
        table.heading("kode", text="Kode")
        table.heading("nama", text="Nama Mata Kuliah")
        table.heading("sks", text="SKS")
        table.pack(fill="x", padx=10, pady=10)

        for mk in tabel_mk:
            table.insert("", "end", values=mk)

        # Form tambah MK
        form = ctk.CTkFrame(self.main_area)
        form.pack()

        k_e = ctk.CTkEntry(form, placeholder_text="Kode MK")
        n_e = ctk.CTkEntry(form, placeholder_text="Nama MK")
        s_e = ctk.CTkEntry(form, placeholder_text="SKS")

        k_e.pack(side="left", padx=5)
        n_e.pack(side="left", padx=5)
        s_e.pack(side="left", padx=5)

        def tambah_mk():
            tabel_mk.append([k_e.get(), n_e.get(), int(s_e.get())])
            self.page_mk()

        ctk.CTkButton(form, text="Tambah", command=tambah_mk).pack(side="left", padx=10)

    def page_nilai(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Input Nilai Mahasiswa", font=("Arial", 22, "bold")).pack()

        form = ctk.CTkFrame(self.main_area)
        form.pack(pady=10)

        npm_e = ctk.CTkEntry(form, placeholder_text="NPM")
        mk_e = ctk.CTkEntry(form, placeholder_text="Mata Kuliah")
        nilai_e = ctk.CTkEntry(form, placeholder_text="Nilai")

        npm_e.pack(side="left", padx=5)
        mk_e.pack(side="left", padx=5)
        nilai_e.pack(side="left", padx=5)

        def input_nilai():
            tabel_nilai.append([npm_e.get(), mk_e.get(), nilai_e.get()])
            messagebox.showinfo("Sukses", "Nilai berhasil ditambahkan.")

        ctk.CTkButton(form, text="Simpan", command=input_nilai).pack(side="left", padx=10)

    def page_setting(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Pengaturan Aplikasi", font=("Arial", 22, "bold")).pack()
        ctk.CTkLabel(self.main_area, text="Tidak ada pengaturan spesifik.", font=("Arial", 14)).pack()

if __name__ == "__main__":
    app = LMSApp()
    app.mainloop()
