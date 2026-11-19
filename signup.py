
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database
import os

class SignupPage(tk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.on_login = on_login
        lokasi = os.path.dirname(os.path.abspath(__file__))
        gambar_path = os.path.join(lokasi, "assets", "background.png")
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg="#087CF0")
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_image = None

        try:
            self.bg_original = Image.open(gambar_path)
        except (FileNotFoundError, OSError) as e:
            self.bg_original = None
            print("Background tidak dapat dibuka:", e)

        def atur_background(event):
            if event.width < 2 or event.height < 2:
                return

            self.canvas.delete("all")

            if self.bg_original is not None:
                gambar = self.bg_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(gambar)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

            self.canvas.create_text(event.width // 2, int(event.height * 0.11), text="CAMPUS LIFE", font=("Arial", 30, "bold"), fill="white")
            self.canvas.create_text(event.width // 2, int(event.height * 0.17), text="Everything you need, All in one place", font=("Arial", 12), fill="white")

        self.canvas.bind("<Configure>", atur_background)

        kotak = tk.Frame(self, bg="white", padx=35, pady=25)
        kotak.place(relx=0.5, rely=0.245, anchor="n", relwidth=0.89)

        tk.Label(kotak, text="Create Your Account", font=("Arial", 20, "bold"), bg="white", fg="#263B63").pack(pady=(5, 20))

        tk.Label(kotak, text="Username", font=("Arial", 11), bg="white", fg="#333333", anchor="w").pack(fill="x")
        self.username = tk.Entry(kotak, font=("Arial", 12), relief="solid", bd=1)
        self.username.pack(fill="x", ipady=8, pady=(7, 16))

        tk.Label(kotak, text="Password", font=("Arial", 11), bg="white", fg="#333333", anchor="w").pack(fill="x")
        self.password = tk.Entry(kotak, font=("Arial", 12), show="*", relief="solid", bd=1)
        self.password.pack(fill="x", ipady=8, pady=(7, 16))

        tk.Label(kotak, text="Confirm Password", font=("Arial", 11), bg="white", fg="#333333", anchor="w").pack(fill="x")
        self.confirm_password = tk.Entry(kotak, font=("Arial", 12), show="*", relief="solid", bd=1)
        self.confirm_password.pack(fill="x", ipady=8, pady=(7, 22))

        tombol_signup = tk.Button(kotak, text="SIGN UP", font=("Arial", 12, "bold"), bg="#365B9D", fg="white", activebackground="#263B63", activeforeground="white", relief="flat", cursor="hand2", command=self.proses_signup)
        tombol_signup.pack(fill="x", ipady=10)

        tk.Label(kotak, text="Already have an account?", font=("Arial", 10), bg="white", fg="#777777").pack(pady=(20, 5))

        tombol_login = tk.Button(kotak, text="Back to Login", font=("Arial", 11, "bold"), bg="white", fg="#365B9D", activebackground="white", activeforeground="#263B63", relief="flat", cursor="hand2", command=self.on_login)
        tombol_login.pack(pady=(0, 5))

    def proses_signup(self):
        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm_password.get()

        if username == "" or password == "" or confirm == "":
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return

        if password != confirm:
            messagebox.showwarning("Pendaftaran Gagal", "Password dan konfirmasi password tidak sama!")
            return

        try:
            berhasil = database.daftar_akun(username, password)

            if berhasil:
                messagebox.showinfo("Pendaftaran Berhasil", "Akun berhasil dibuat! Silakan login.")
                self.on_login()
            else:
                messagebox.showerror("Pendaftaran Gagal", "Username sudah digunakan!")

        except Exception as e:
            messagebox.showerror("Database Error", f"Terjadi kesalahan: {e}")
