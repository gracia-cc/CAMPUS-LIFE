
import tkinter as tk
import database
from login import LoginPage
from signup import SignupPage
from notification import tampilkan_notifikasi
from dashboard import DashboardPage
from todo import TodoPage
from notespage import NotesPage

class CampusLifeApp(tk.Tk):
    def __init__(self):
        super().__init__()
<<<<<<< HEAD
        database.buat_tabel()
        self.tampilkan_login()
        self.title("CampusLife")
=======
        self.title("CAMPUS LIFE")
>>>>>>> 546c5711d7408b175b475257a1659079f6dd7ee6
        self.state("zoomed")
        self.resizable(True, True)
        self.minsize(500, 650)
        self.configure(bg="#F4F6FA")

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
        halaman = DashboardPage(
    self,
    username,
    on_logout=self.tampilkan_login,
    on_todo=lambda: self.tampilkan_todo(username),
    on_notes=lambda: self.tampilkan_notes(username),
)
        halaman.pack(fill="both", expand=True)
<<<<<<< HEAD
        tk.Label(self, text="Welcome to CampusLife!", font=("Arial", 22, "bold"), bg="white", fg="#263B63").pack(pady=(180, 15))
        tk.Label(self, text=f"Hello, {username}!", font=("Arial", 14), bg="#F4F6FA").pack()
        tk.Label(self, text="Login berhasil!", font=("Arial", 11), bg="white", fg="#777777").pack(pady=20)
        tk.Button(self, text="Logout", bg="#365B9D", fg="white", relief="flat", command=self.tampilkan_login).pack(ipadx=25, ipady=8)

        tampilkan_notifikasi("Campus Life",f"Selamat datang, {username}!")
    def tampilkan_dashboard(self, username):
        self.bersihkan_halaman()
        halaman = DashboardPage(self.username,on_logout=self.tampilkan_login,on_todo=lambda: self.tampilkan_todo(username),on_notes=lambda: self.tampilkan_notes(username),)
        halaman.pack(fill="both", expand=True)
    def tampilkan_todo(self, username):
        self.bersihkan_halaman()
        halaman = TodoPage(self, username, on_back=lambda: self.login_berhasil(username))
        halaman.pack(fill="both", expand=True)
    def tampilkan_notes(self, username):
        self.bersihkan_halaman()
        halaman = NotesPage(self.username,on_back=lambda: self.tampilkan_dashboard(username),)
        halaman.pack(fill="both", expand=True)
=======
        tampilkan_notifikasi("Campus Life", f"Selamat datang, {username}!")
>>>>>>> 546c5711d7408b175b475257a1659079f6dd7ee6

if __name__ == "__main__":
    aplikasi = CampusLifeApp()
    aplikasi.mainloop()
