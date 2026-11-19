
import tkinter as tk
from tkinter import messagebox

class DashboardPage(tk.Frame):
    def __init__(self, master, username, on_logout):
        super().__init__(master, bg="#F4F6FA")
        self.username = username
        self.on_logout = on_logout

        header = tk.Frame(self, bg="#365B9D", height=180)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="CAMPUS LIFE", font=("Arial", 22, "bold"), bg="#365B9D", fg="white").pack(pady=(30, 10))
        tk.Label(header, text=f"Welcome back, {username}!", font=("Arial", 14), bg="#365B9D", fg="white").pack()
        tk.Label(header, text="Your campus life starts here.", font=("Arial", 10), bg="#365B9D", fg="white").pack(pady=8)

        tk.Label(self, text="Dashboard", font=("Arial", 20, "bold"), bg="#F4F6FA", fg="#263B63").pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self, text="Pilih fitur yang ingin kamu gunakan.", font=("Arial", 10), bg="#F4F6FA", fg="#777777").pack(anchor="w", padx=25, pady=(0, 20))

        menu = tk.Frame(self, bg="#F4F6FA")
        menu.pack(fill="both", expand=True, padx=25)

        self.buat_menu(menu, "📝  Notes", "Catat materi dan ide kuliah", self.belum_tersedia)
        self.buat_menu(menu, "✅  To-Do List", "Atur tugas dan deadline", self.belum_tersedia)
        self.buat_menu(menu, "📅  Jadwal Kuliah", "Lihat jadwal perkuliahan", self.belum_tersedia)
        self.buat_menu(menu, "👤  Profil", "Informasi akun pengguna", self.belum_tersedia)

        tombol_logout = tk.Button(self, text="LOGOUT", font=("Arial", 11, "bold"), bg="#E74C3C", fg="white", relief="flat", cursor="hand2", command=self.on_logout)
        tombol_logout.pack(fill="x", padx=25, pady=20, ipady=10)

    def buat_menu(self, parent, judul, deskripsi, perintah):
        kartu = tk.Frame(parent, bg="white", padx=15, pady=12)
        kartu.pack(fill="x", pady=7)

        tk.Label(kartu, text=judul, font=("Arial", 13, "bold"), bg="white", fg="#263B63").pack(anchor="w")
        tk.Label(kartu, text=deskripsi, font=("Arial", 9), bg="white", fg="#777777").pack(anchor="w", pady=(5, 8))

        tk.Button(kartu, text="Buka Fitur", font=("Arial", 9, "bold"), bg="#365B9D", fg="white", relief="flat", cursor="hand2", command=perintah).pack(anchor="e")

    def belum_tersedia(self):
        messagebox.showinfo("Informasi", "Fitur ini akan segera tersedia!")