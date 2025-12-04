import customtkinter as ctk
from tkinter import messagebox, ttk

# Database (in-memory)
DB_USERS = {
    "Admin1": {"password": "qwerty", "role": "Admin"},
    "2532076": {"password": "uib", "role": "mahasiswa"},
    "2532060": {"password": "uib", "role": "mahasiswa"},
    "2532057": {"password": "uib", "role": "mahasiswa"},
    "2532059": {"password": "uib", "role": "mahasiswa"},
    "2532021": {"password": "uib", "role": "mahasiswa"},
}

data_mahasiswa = {
    "Admin1": "Ko Patrick",
    "2532076": "Christian Lombu",
    "2532060": "Pieter Nicolaas",
    "2532057": "Royyan Putra",
    "2532059": "Agus Suwanto",
    "2532021": "Steven Kevin",
}

tabel_users = [
    ["Admin1", "Ko Patrick", "Admin"],
    ["2532076", "Christian Lombu", "uib"],
    ["2532060", "Pieter Nicolaas", "uib"],
    ["2532057", "Royyan Putra", "uib"],
    ["2532059", "Agus Suwanto", "uib"],
    ["2532021", "Steven Kevin", "uib"]
]

tabel_mk = [
    ["25001", "Pengantar Teknologi Informasi", 3],
    ["25002", "Teknik Pemograman", 3],
    ["25003", "Bahasa Inggris", 2],
    ["25004", "Agama", 2],
    ["25005", "Bahasa Indonesia", 2],
    ["25006", "Kalkulus dan Aljabar Linier", 3],
    ["25007", "Lab.Teknik Pemograman", 1],
    ["25008", "Arsitektur dan Organisasi Komputer", 3]
]

tabel_nilai = []

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class LMSApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("LMS Portal Mahasiswa")
        self.geometry("900x600")

        # session
        self.current_user = None
        self.role = None
        self.nama_login = None

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.tampilan_login()

    # Login Screen
    def tampilan_login(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.container, width=500, height=500, corner_radius=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Universitas Internasional Batam", font=("Bookman Old Style", 30, "bold")).pack(pady=(0, 10))
        ctk.CTkLabel(frame, text="LMS LOGIN", font=("Century Gothic", 24, "bold")).pack(pady=(40, 20))

        self.npm_entry = ctk.CTkEntry(frame, placeholder_text="USER ID", width=300, height=40)
        self.npm_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300, height=40)
        self.pass_entry.pack(pady=10)

        btn_login = ctk.CTkButton(frame, text="Login", command=self.cek_login, width=300, height=40)
        btn_login.pack(pady=30)


    def cek_login(self):
        npm = self.npm_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        akun = DB_USERS.get(npm)
        if akun and akun["password"] == pwd:
            self.current_user = npm
            self.role = akun["role"]
            self.nama_login = data_mahasiswa.get(npm, "Mahasiswa")
            self.tampilan_main(self.nama_login)
        else:
            messagebox.showerror("Access Denied", "Wrong NPM or Password!! Please Try Again.")

    # Main Layout
    def tampilan_main(self, nama):
        for widget in self.container.winfo_children():
            widget.destroy()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.container, width=180)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="MENU", font=("Arial", 16, "bold")).pack(pady=20)

        # Always show Dashboard
        ctk.CTkButton(self.sidebar, text="Dashboard", command=self.page_dashboard).pack(pady=5)

        if self.role == "Admin":
            ctk.CTkButton(self.sidebar, text="Users", command=self.page_users).pack(pady=5)
            ctk.CTkButton(self.sidebar, text="Mata Kuliah", command=self.page_mk).pack(pady=5)
            ctk.CTkButton(self.sidebar, text="Nilai", command=self.page_nilai).pack(pady=5)
            ctk.CTkButton(self.sidebar, text="Setting", command=self.page_setting).pack(pady=5)
        else:
            ctk.CTkLabel(self.sidebar, text="Akses: Mahasiswa", font=("Arial", 12)).pack(pady=10)
            ctk.CTkLabel(self.sidebar, text="(Hubungi admin untuk perubahan)", font=("Arial", 10)).pack(pady=5)

        ctk.CTkButton(self.sidebar, text="Logout", fg_color="#FF5555", hover_color="#BB3333",
                      command=self.logout).pack(side="bottom", pady=20)

        # Area utama
        self.main_area = ctk.CTkFrame(self.container, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True)

        self.page_dashboard()

    def logout(self):
        self.current_user = None
        self.role = None
        self.nama_login = None
        self.tampilan_login()

    # Pages
    def page_dashboard(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text=f"Halo, {self.nama_login}", font=("Arial", 28, "bold")).pack(anchor="w")
        ctk.CTkLabel(self.main_area, text="Selamat datang di Dashboard LMS", font=("Arial", 14)).pack(anchor="w")

        # Statistik
        card = ctk.CTkFrame(self.main_area)
        card.pack(fill="x", pady=20, padx=10)

        total_mhs = len([u for u in tabel_users if u[2] != "Admin"]) 
        total_mk = len(tabel_mk)
        total_nilai = len(tabel_nilai)

        ctk.CTkLabel(card, text=f"Total Mahasiswa: {total_mhs}", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(card, text=f"Total Mata Kuliah: {total_mk}", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(card, text=f"Total Nilai Input: {total_nilai}", font=("Arial", 16)).pack(pady=5)

        # Jika mahasiswa, tampil pesan terbatas
        if self.role != "Admin":
            ctk.CTkLabel(self.main_area, text="Anda memiliki akses terbatas. Hanya admin yang dapat mengedit data.",
                         font=("Arial", 12)).pack(pady=(10, 0), anchor="w")

    # Users (Admin only)
    def page_users(self):
        if self.role != "Admin":
            messagebox.showwarning("Akses Ditolak", "Hanya Admin yang boleh membuka menu ini.")
            return

        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Manajemen Users", font=("Arial", 22, "bold")).pack(pady=(0, 10))

        table = ttk.Treeview(self.main_area, columns=("npm", "nama", "pass"), show="headings", height=8)
        table.heading("npm", text="NPM")
        table.heading("nama", text="Nama")
        table.heading("pass", text="Password/Role")
        table.pack(fill="x", padx=10, pady=10)

        # Clear and insert current rows
        for item in table.get_children():
            table.delete(item)
        for row in tabel_users:
            table.insert("", "end", values=row)

        # Form Tambah User
        form = ctk.CTkFrame(self.main_area)
        form.pack(fill="x", pady=10, padx=10)

        npm_e = ctk.CTkEntry(form, placeholder_text="NPM")
        nama_e = ctk.CTkEntry(form, placeholder_text="Nama")
        pass_e = ctk.CTkEntry(form, placeholder_text="Password")
        role_var = ctk.CTkComboBox(form, values=["mahasiswa", "Admin"])
        role_var.set("mahasiswa")

        npm_e.pack(side="left", padx=5)
        nama_e.pack(side="left", padx=5)
        pass_e.pack(side="left", padx=5)
        role_var.pack(side="left", padx=5)

        def tambah_user():
            npm = npm_e.get().strip()
            nama = nama_e.get().strip()
            ps = pass_e.get().strip()
            role = role_var.get().strip()
            if not (npm and nama and ps and role):
                messagebox.showwarning("Input Kosong", "Semua field harus diisi.")
                return

            # tambahkan ke struktur data
            DB_USERS[npm] = {"password": ps, "role": role}
            data_mahasiswa[npm] = nama
            tabel_users.append([npm, nama, ps if role == "mahasiswa" else role]) 
            self.page_users()  # refresh

        def hapus_user():
            selected = table.selection()
            if not selected:
                messagebox.showwarning("Pilih User", "Pilih user terlebih dahulu.")
                return
            item = table.item(selected[0])["values"]
            npm = item[0]
            if npm == "Admin1":
                messagebox.showwarning("Tidak diizinkan", "Admin default tidak boleh dihapus.")
                return
            confirm = messagebox.askyesno("Konfirmasi", f"Hapus user {npm}?")
            if confirm:
                # remove from all structures
                DB_USERS.pop(npm, None)
                data_mahasiswa.pop(npm, None)
                for i, row in enumerate(tabel_users):
                    if row[0] == npm:
                        tabel_users.pop(i)
                        break
                self.page_users()

        ctk.CTkButton(form, text="Tambah", command=tambah_user).pack(side="left", padx=5)
        ctk.CTkButton(form, text="Hapus Terpilih", command=hapus_user).pack(side="left", padx=5)

    # Mata Kuliah (Admin only)
    def page_mk(self):
        if self.role != "Admin":
            messagebox.showwarning("Akses Ditolak", "Hanya Admin yang boleh membuka menu ini.")
            return

        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Daftar Mata Kuliah", font=("Arial", 22, "bold")).pack(pady=(0, 10))

        table = ttk.Treeview(self.main_area, columns=("kode", "nama", "sks"), show="headings", height=8)
        table.heading("kode", text="Kode")
        table.heading("nama", text="Nama Mata Kuliah")
        table.heading("sks", text="SKS")
        table.pack(fill="x", padx=10, pady=10)

        for mk in tabel_mk:
            table.insert("", "end", values=mk)

        # Form tambah MK
        form = ctk.CTkFrame(self.main_area)
        form.pack(fill="x", pady=10, padx=10)

        k_e = ctk.CTkEntry(form, placeholder_text="Kode MK")
        n_e = ctk.CTkEntry(form, placeholder_text="Nama MK")
        s_e = ctk.CTkEntry(form, placeholder_text="SKS")

        k_e.pack(side="left", padx=5)
        n_e.pack(side="left", padx=5)
        s_e.pack(side="left", padx=5)

        def tambah_mk():
            kode = k_e.get().strip()
            nama = n_e.get().strip()
            sks = s_e.get().strip()
            if not (kode and nama and sks):
                messagebox.showwarning("Input Kosong", "Semua field harus diisi.")
                return
            try:
                sks_i = int(sks)
            except ValueError:
                messagebox.showwarning("Input Salah", "SKS harus berupa angka.")
                return
            tabel_mk.append([kode, nama, sks_i])
            self.page_mk()

        def hapus_mk():
            selected = table.selection()
            if not selected:
                messagebox.showwarning("Pilih MK", "Pilih mata kuliah terlebih dahulu.")
                return
            item = table.item(selected[0])["values"]
            kode = item[0]
            confirm = messagebox.askyesno("Konfirmasi", f"Hapus MK {kode}?")
            if confirm:
                for i, row in enumerate(tabel_mk):
                    if row[0] == kode:
                        tabel_mk.pop(i)
                        break
                self.page_mk()

        ctk.CTkButton(form, text="Tambah", command=tambah_mk).pack(side="left", padx=5)
        ctk.CTkButton(form, text="Hapus Terpilih", command=hapus_mk).pack(side="left", padx=5)

    # Nilai (Admin only to edit)
    def page_nilai(self):
        if self.role != "Admin":
            for widget in self.main_area.winfo_children():
                widget.destroy()
            ctk.CTkLabel(self.main_area, text="Lihat Nilai (Mahasiswa)", font=("Arial", 22, "bold")).pack(pady=(0, 10))
            table = ttk.Treeview(self.main_area, columns=("npm", "mk", "nilai"), show="headings", height=8)
            table.heading("npm", text="NPM")
            table.heading("mk", text="Mata Kuliah")
            table.heading("nilai", text="Nilai")
            table.pack(fill="x", padx=10, pady=10)
            for row in tabel_nilai:
                if row[0] == self.current_user:
                    table.insert("", "end", values=row)
            return

        # Admin: input dan lihat semua nilai
        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Input Nilai Mahasiswa", font=("Arial", 22, "bold")).pack(pady=(0, 10))

        form = ctk.CTkFrame(self.main_area)
        form.pack(pady=10, padx=10)

        npm_e = ctk.CTkEntry(form, placeholder_text="NPM")
        mk_e = ctk.CTkEntry(form, placeholder_text="Mata Kuliah")
        nilai_e = ctk.CTkEntry(form, placeholder_text="Nilai")

        npm_e.pack(side="left", padx=5)
        mk_e.pack(side="left", padx=5)
        nilai_e.pack(side="left", padx=5)

        def input_nilai():
            npm = npm_e.get().strip()
            mk = mk_e.get().strip()
            nilai = nilai_e.get().strip()
            if not (npm and mk and nilai):
                messagebox.showwarning("Input Kosong", "Semua field harus diisi.")
                return
            tabel_nilai.append([npm, mk, nilai])
            messagebox.showinfo("Sukses", "Nilai berhasil ditambahkan.")
            self.page_nilai()

        ctk.CTkButton(form, text="Simpan", command=input_nilai).pack(side="left", padx=5)

        # Tampilkan semua nilai
        table = ttk.Treeview(self.main_area, columns=("npm", "mk", "nilai"), show="headings", height=8)
        table.heading("npm", text="NPM")
        table.heading("mk", text="Mata Kuliah")
        table.heading("nilai", text="Nilai")
        table.pack(fill="x", padx=10, pady=10)

        for row in tabel_nilai:
            table.insert("", "end", values=row)

        def hapus_nilai():
            selected = table.selection()
            if not selected:
                messagebox.showwarning("Pilih Nilai", "Pilih baris nilai terlebih dahulu.")
                return
            item = table.item(selected[0])["values"]
            confirm = messagebox.askyesno("Konfirmasi", f"Hapus nilai {item}?")
            if confirm:
                for i, row in enumerate(tabel_nilai):
                    if row == item:
                        tabel_nilai.pop(i)
                        break
                self.page_nilai()

        ctk.CTkButton(self.main_area, text="Hapus Nilai Terpilih", command=hapus_nilai).pack(pady=5)

    # Setting
    def page_setting(self):
        if self.role != "Admin":
            messagebox.showwarning("Akses Ditolak", "Hanya admin yang boleh membuka menu ini.")
            return

        for widget in self.main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_area, text="Pengaturan Aplikasi", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkLabel(self.main_area, text="Tidak ada pengaturan spesifik.", font=("Arial", 14)).pack(pady=10)

# Run App
if __name__ == "__main__":
    app = LMSApp()
    app.mainloop()
