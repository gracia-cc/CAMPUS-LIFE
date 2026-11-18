
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database
import os

class LoginPage(tk.Frame):
    def __init__(self, master, on_signup, on_login):
        super().__init__(master)
        self.on_signup = on_signup
        self.on_login = on_login
        lokasi = os.path.dirname(os.path.abspath(__file__))
        gambar_path = os.path.join( lokasi, "assets", "background.png")
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg="#087CF0")
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        try:
            self.bg_original = Image.open(gambar_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "File background.png tidak ditemukan!")
            self.bg_original = None
        self.bg_image = None
        def atur_background(event):
            if event.width < 2 or event.height < 2:
                return
            if self.bg_original is not None:
                gambar = self.bg_original.resize((event.width, event.height),Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(gambar)
                self.canvas.delete("all")
                self.canvas.create_image(0,0,image=self.bg_image,anchor="nw")
            else:
                self.canvas.configure(bg="#087CF0")
            self.canvas.create_text(event.width // 2,int(event.height * 0.13), text="CAMPUS LIFE", font=("Arial", 30, "bold"), fill="white")

            self.canvas.create_text(event.width // 2,int(event.height * 0.19),text="Everything you need, All in one place",font=("Arial", 12), fill="white")
        self.canvas.bind("<Configure>", atur_background)

        kotak = tk.Frame(self, bg="white", padx=35, pady=30)
        kotak.place(relx=0.5, rely=0.285, anchor="n", relwidth=0.89)

        tk.Label(kotak, text="Welcome Back!", font=("Arial", 22, "bold"), bg="white", fg="#263B63").pack(pady=(5, 25))
        tk.Label(kotak, text="Username", font=("Arial", 11), bg="white", fg="#333333", anchor="w").pack(fill="x")

        self.username = tk.Entry(kotak, font=("Arial", 12), relief="solid", bd=1)
        self.username.pack(fill="x", ipady=9, pady=(8, 22))

        tk.Label(kotak, text="Password", font=("Arial", 11), bg="white", fg="#333333", anchor="w").pack(fill="x")

        self.password = tk.Entry(kotak, font=("Arial", 12), show="*", relief="solid", bd=1)
        self.password.pack(fill="x", ipady=9, pady=(8, 25))

        tombol_login = tk.Button( kotak, text="LOGIN", font=("Arial", 12, "bold"), bg="#365B9D", fg="white", activebackground="#263B63", activeforeground="white", relief="flat", cursor="hand2", command=self.proses_login)
        tombol_login.pack(fill="x", ipady=10)
        tk.Label( kotak, text="Don't have an account?", font=("Arial", 10), bg="white", fg="#777777").pack(pady=(25, 5))
        tombol_signup = tk.Button( kotak, text="Sign Up", font=("Arial", 11, "bold"), bg="white", fg="#365B9D", activebackground="white", activeforeground="#263B63", relief="flat", cursor="hand2", command=self.on_signup)
        tombol_signup.pack(pady=(0, 5))

    def proses_login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if username == "" or password == "":
            messagebox.showwarning("Peringatan", "Username dan password tidak boleh kosong!")
            return
        try:
            hasil = database.login_akun(username, password)
            if hasil:
                messagebox.showinfo(
                    "Login Berhasil", "Selamat datang di CAMPUS LIFE!")
                self.on_login(username)
            else:
                messagebox.showerror("Login Gagal", "Username atau password salah!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Terjadi kesalahan: {e}")
