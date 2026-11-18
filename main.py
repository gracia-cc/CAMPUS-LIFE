import tkinter as tk
import database
from login import LoginPage
from signup import SignupPage
from tkinter import messagebox

class CampusLifeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CampusLife")
        self.geometry("500x650")
        self.resizable(False, False)
        self.configure(bg="#F4F6FA")
        database.buat_tabel()
        self.tampilkan_login()

    def bersihkan_halaman(self):
        for widget in self.winfo_children():
            widget.destroy()

    def tampilkan_login(self):
        self.bersihkan_halaman()
        halaman=LoginPage(self, on_signup=self.tampilkan_signup, on_login=self.login_berhasil)
        halaman.pack(fill="both", expand=True)

    def tampilkan_signup(self):
            self.bersihkan_halaman()
            halaman=SignupPage(self, on_login=self.tampilkan_login)
            halaman.pack(fill="both", expand=True)

    def login_berhasil(self, username):
        self.bersihkan_halaman()

        tk.Label(self, text="Welcome to CampusLife!", font=("Arial", 22, "bold"), bg="white", fg="#263B63").pack(pady=(180, 15))
        tk.Label(self, text=f"Hello, {username}!", font=("Arial", 14), bg="#F4F6FA").pack()
        tk.Label(self, text="Login berhasil!", font=("Arial", 11), bg="white", fg="#777777").pack(pady=20)
        tk.Button(self, text="Logout", bg="#365B9D", fg="white", relief="flat", command=self.tampilkan_login).pack(ipadx=25, ipady=8)

if __name__ == "__main__":
     aplikasi = CampusLifeApp()
     aplikasi.mainloop()

print("PROGRAM BERJALAN")
print("PROGRAM SELESAI")