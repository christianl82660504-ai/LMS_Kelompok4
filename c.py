import customtkinter as ctk
from tkinter import messagebox

# KONFIGURASI TEMA
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

# DATA (NPM : Password) 
DB_USERS = {
    "2532076": "uib",
    "2532060": "uib",
    "2532057": "uib",
    "2532059": "uib",
    "2532021": "uib",
}

# Nama Mahasiswa
data_mahasiswa = {
    "2532076" : "Christian Lombu",
    "2532060" : "Pieter Nicolaas",
    "2532057" : "Royyan Putra",
    "2532059" : "Agus Suwanto",
    "2532021" : "Steven Kevin",
}

class LMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("LMS Portal Mahasiswa")
        self.geometry("600x450")
        self.state()

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

    def tampilan_dashboard(self, npm):
        for widget in self.container.winfo_children(): widget.destroy()

        sidebar = ctk.CTkFrame(self.container, width=150, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(sidebar, text="MENU LMS", font=("Arial", 16, "bold")).pack(pady=30)
        ctk.CTkButton(sidebar, text="Home", fg_color="transparent", border_width=1).pack(pady=5, padx=10)
        ctk.CTkButton(sidebar, text="Dashboard", fg_color="transparent", border_width=1).pack(pady=5, padx=10)
        ctk.CTkButton(sidebar, text="Logout", fg_color="#FF5555", hover_color="#BA3333", command=self.tampilan_login).pack(side="bottom", pady=20, padx=10)

        main_area = ctk.CTkFrame(self.container, fg_color="transparent")
        main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        nama = data_mahasiswa.get(npm)
        ctk.CTkLabel(main_area, text=f"Halo, {nama}!", font=("Arial", 28, "bold")).pack(anchor="w")
        ctk.CTkLabel(main_area, text="Selamat datang di LMS.", font=("Arial", 14)).pack(anchor="w", pady=5)
        
        info_card = ctk.CTkFrame(main_area, height=100, fg_color="#2B2B2B")
        info_card.pack(fill="x", pady=20)
        ctk.CTkLabel(info_card, text="Status : Online", text_color="white").place(relx=0.5, rely=0.5, anchor="center")

    def cek_login(self):
        npm = self.npm_entry.get()
        pwd = self.pass_entry.get()

        if DB_USERS.get(npm) == pwd:
            self.tampilan_dashboard(npm)
        else:
            messagebox.showerror("Akses Ditolak", "NPM atau Password Anda salah.")

if __name__ == "__main__":
    app = LMSApp()
    app.mainloop()






