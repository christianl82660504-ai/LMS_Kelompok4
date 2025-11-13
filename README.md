import customtkinter
from tkinter import messagebox

# Mengatur tema default (bisa 'System', 'Dark', atau 'Light')
customtkinter.set_appearance_mode("System")  
# Mengatur skema warna default (misalnya 'blue', 'green', 'dark-blue')
customtkinter.set_default_color_theme("blue")  

# --- Fungsi Aksi Tombol ---

def lihat_kursus():
    """Menampilkan pesan saat tombol 'Lihat Kursus' ditekan."""
    messagebox.showinfo("Aksi", "Anda mengklik Lihat Kursus! (Tampilan modern berfungsi!)")

def keluar_aplikasi():
    """Menutup jendela aplikasi."""
    if messagebox.askyesno("Keluar", "Apakah Anda yakin ingin keluar dari LMS?"):
        app.quit()

# --- Setup Jendela Utama (App Class) ---

# Menggunakan CTk (CustomTkinter) untuk Jendela
app = customtkinter.CTk()
app.title("Sistem Manajemen Pembelajaran (LMS) - Modern UI")
app.geometry("500x350")
app.resizable(False, False) 

# --- Membuat Widget UI ---

# 1. Judul Aplikasi (CTkLabel)
judul_label = customtkinter.CTkLabel(app, 
                                     text="LMS", 
                                     font=customtkinter.CTkFont(size=24, weight="bold"))
judul_label.pack(pady=(30, 10)) # pady atas 30, bawah 10

# 2. Pesan Selamat Datang (CTkLabel)
pesan_label = customtkinter.CTkLabel(app, 
                                     text="Platform Pembelajaran Anda. Siap untuk belajar hari ini?",
                                     font=customtkinter.CTkFont(size=14))
pesan_label.pack(pady=5)

# --- Frame untuk Menyatukan Tombol (Optional, tapi membuat tata letak lebih rapi) ---
button_frame = customtkinter.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=20, padx=20)

# 3. Tombol 'Lihat Kursus' (CTkButton) - Tombol Primer
kursus_button = customtkinter.CTkButton(button_frame, 
                                        text="Lihat Kursus 📚", 
                                        command=lihat_kursus,
                                        width=250,
                                        height=40,
                                        fg_color="#1F538D", # Warna tombol utama
                                        hover_color="#4C7FBC")
kursus_button.pack(pady=10)

# 4. Tombol 'Keluar' (CTkButton) - Tombol Sekunder
keluar_button = customtkinter.CTkButton(button_frame, 
                                        text="Keluar", 
                                        command=keluar_aplikasi,
                                        width=250,
                                        height=40,
                                        fg_color="gray50", # Warna tombol sekunder
                                        hover_color="gray40")
keluar_button.pack(pady=10)

# 5. Menjalankan main loop
app.mainloop()
