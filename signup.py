import tkinter as tk
from tkinter import messagebox
import database
class SignupPage(tk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master, bg="#F4F6FA")
        self.on_login = on_login

        tk.Label(self, text="CampusLife", font=("Arial", 26, "bold"), bg="#F4F6FA", fg="#263B63").pack(pady=(35, 5))
        tk.Label(self, text="Create Your Account", font=("Arial", 18, "bold"), bg="#F4F6FA", fg="#263B63").pack(pady=(10, 20))

        kotak = tk.Frame(self, bg="white", padx=30, pady=25)
        kotak.pack(padx=35, fill="x")

        tk.Label(kotak, text="Username", bg="white", anchor="w").pack(fill="x")
        
        self.username = tk.Entry(kotak, font=("Arial", 11), relief="solid", bd=1)
        self.username.pack(fill="x", ipady=8, pady=(5, 15))

        tk.Label(kotak, text="Password", bg="white", anchor="w").pack(fill="x")
                
        self.password = tk.Entry(kotak, font=("Arial", 11), show="*", relief="solid", bd=1)
        self.password.pack(fill="x", ipady=8, pady=(5, 15))

        tk.Label(kotak, text="Confirm Password", bg="white", anchor="w").pack(fill="x")
        
        self.confirm_password = tk.Entry(kotak, font=("Arial", 11), show="*", relief="solid", bd=1)
        self.confirm_password.pack(fill="x", ipady=8, pady=(5, 20))

        tk.Button(kotak, text="SIGN UP", font=("Arial", 11, "bold"), bg="#365B9D", fg="white", relief="flat", cursor="hand2", command=self.proses_signup).pack(fill="x", ipady=8)
        tk.Button(kotak, text="Back to login", bg="white", fg="#365B9D", relief="flat", cursor="hand2", command=self.on_login).pack(pady=(15, 0))

    def proses_signup(self):
        username=self.username.get().strip()
        password=self.password.get()
        confirm=self.confirm_password.get()

        if username == "" or password =="":
            messagebox.showwarning("Peringatan", "semua kolom harus diisi!")
            return
        if password != confirm:
            messagebox.showwarning("Pendaftaran gagal", "password dan konfirmasi password tidak sama!")
            return
        berhasil=database.daftar_akun(username, password)

        if berhasil:
            messagebox.showinfo("Akun berhasil dibuat", "silahkan login!")
            self.on_login()
        else :
            messagebox.showerror("Pendaftaran gagal", "username sudah digunakan!")
