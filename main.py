
import tkinter as tk
import database
from login import LoginPage
from signup import SignupPage
from notification import tampilkan_notifikasi
from dashboard import DashboardPage

class CampusLifeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CAMPUS LIFE")
        self.state("zoomed")
        self.resizable(True, True)
        self.minsize(500, 650)
        self.configure(bg="#F4F6FA")
        database.buat_tabel()
        self.tampilkan_login()

    def bersihkan_halaman(self):
        for widget in self.winfo_children():
            widget.destroy()

    def tampilkan_login(self):
        self.bersihkan_halaman()
        halaman = LoginPage(self, on_signup=self.tampilkan_signup, on_login=self.login_berhasil)
        halaman.pack(fill="both", expand=True)

    def tampilkan_signup(self):
        self.bersihkan_halaman()
        halaman = SignupPage(self, on_login=self.tampilkan_login)
        halaman.pack(fill="both", expand=True)

    def login_berhasil(self, username):
        self.bersihkan_halaman()
        halaman = DashboardPage(self, username, on_logout=self.tampilkan_login)
        halaman.pack(fill="both", expand=True)
        tampilkan_notifikasi("Campus Life", f"Selamat datang, {username}!")

if __name__ == "__main__":
    aplikasi = CampusLifeApp()
    aplikasi.mainloop()
