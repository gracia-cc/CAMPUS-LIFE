import tkinter as tk
from tkinter import messagebox
import database

class LoginPage(tk.Frame):
    def __init__(self, master, on_signup, on_login):
        super().__init__(master, bg="#F4F6FA")
        self.on_login = on_login
        self.on_signup = on_signup

        judul = tk.Label(self, text="CampusLife", font=("Arial", 20, "bold"), bg="#F4F6FA", fg="#263B63")
        judul.pack(pady=(45, 5))

        subjudul = tk.Label(self, text="Everything you need, All in one place", font=("Arial", 10), bg="#F4F6FA", fg="#777777")
        subjudul.pack(pady=(0, 30))

        kotak = tk.Frame(self, bg="white", padx=30, pady=25)
        kotak.pack(padx=35, fill="x")

        tk.Label(kotak, text="Welcome Back!", font=("Arial", 18, "bold"), bg="white", fg="#263B63").pack(pady=(0, 20))
        tk.Label(kotak, text="Username", bg="white", anchor="w").pack(fill="x")

        self.username = tk.Entry(kotak, font=("Arial", 11), relief="solid", bd=1)
        self.username.pack(fill="x", ipady=8, pady=(5, 15))

        tk.Label(kotak, text="Password", bg="white", anchor="w").pack(fill="x")
        
        self.password = tk.Entry(kotak, font=("Arial", 11), show="*", relief="solid", bd=1)
        self.password.pack(fill="x", ipady=8, pady=(5, 20))

        tk.Button(kotak, text="LOGIN", font=("Arial", 11, "bold"), bg="#365B9D", fg="white", relief="flat", cursor="hand2", command=self.proses_login).pack(fill="x", ipady=8)
        tk.Label(kotak, text="Dont have an account?", bg="white", fg="#777777").pack(pady=(20, 5))
        tk.Button(kotak, text="Sign Up", bg="white", fg="#365B9D", relief="flat", cursor="hand2", command=self.on_signup).pack()

    def proses_login(self):
        username=self.username.get().strip()
        password=self.password.get()

        if username == "" or password =="":
            messagebox.showwarning("Peringatan", "username dan password tidak boleh kosong!")
            return
        if database.login_akun(username, password):
            self.on_login(username)
        else:
            messagebox.showerror("Login Gagal", "username atau password salah!")