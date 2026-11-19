
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

class DashboardPage(tk.Frame):
    def __init__(self, master, username, on_logout):
        super().__init__(master, bg="#F4F6FA")
        self.username = username
        self.on_logout = on_logout
        self.language = "Indonesia"
        self.music_on = False
        self.volume = 50
        self.vlc_instance = None
        self.vlc_player = None
        self.vlc_media = None
        lokasi = os.path.dirname(os.path.abspath(__file__))
        self.music_path = os.path.join(lokasi, "assets", "music.mp3")
        gambar_path = os.path.join(lokasi, "assets", "background.png")
        self.bg_original = None
        self.bg_photo = None
        self.bg_label = tk.Label(self, bg="#F4F6FA")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        try:
            self.bg_original = Image.open(gambar_path)
        except (FileNotFoundError, OSError) as e:
            print("Background tidak ditemukan:", e)
        self.bind("<Configure>", self.atur_background)
        header = tk.Frame(self, bg="#365B9D", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="CAMPUS LIFE", font=("Arial", 20, "bold"), bg="#365B9D", fg="white").pack(side="left", padx=25)
        tk.Button(header, text="Logout", font=("Arial", 10, "bold"), bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white", relief="flat", cursor="hand2", command=self.logout).pack(side="right", padx=(5, 20), pady=20)
        tk.Button(header,text="⚙️ Pengaturan",font=("Segoe UI Emoji", 10, "bold"),bg="#263B63",fg="white",relief="flat",cursor="hand2",command=self.tampilkan_pengaturan).pack(side="right", padx=5, pady=20)
        tk.Button(header,text=f"👤 {username}",font=("Arial", 10, "bold"),bg="#263B63",fg="white",relief="flat",cursor="hand2",command=self.tampilkan_profil).pack(side="right", padx=5, pady=20)
        self.lbl_dashboard = tk.Label(self,text="Dashboard",font=("Arial", 24, "bold"),bg="#F4F6FA",fg="#263B63")
        self.lbl_dashboard.pack(anchor="w",padx=30,pady=(30, 5))
        self.lbl_subtitle = tk.Label(self,text=f"Selamat datang kembali, {username}!",font=("Arial", 12), bg="#F4F6FA",fg="#777777")
        self.lbl_subtitle.pack(anchor="w",padx=30,pady=(0, 20))
        menu = tk.Frame(self,bg="#F4F6FA")
        menu.pack(fill="both",expand=True,padx=30,pady=(0, 20))
        self.menu_widgets = []
        self.buat_menu(menu,"📝 Notes","Catat materi dan ide kuliah",self.belum_tersedia)
        self.buat_menu(menu,"✅ To-Do List","Atur tugas dan deadline",self.belum_tersedia)
        self.buat_menu(menu,"🥗 Food Court","pilih menu di foodcourt dan lihat berapa biaya yang dikeluarkan",self.belum_tersedia)
        self.buat_menu(menu,"🩺 Kesehatan","Cek kesehatan",self.belum_tersedia)
    def atur_background(self, event):
        if event.width < 2 or event.height < 2:
            return
        if self.bg_original is not None:
            gambar = self.bg_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(gambar)
            self.bg_label.configure(image=self.bg_photo)
    def buat_menu(self, parent, judul, deskripsi, perintah):
        kartu = tk.Frame(parent, bg="white", padx=15,pady=10)
        kartu.pack(fill="x",pady=6)
        label_judul = tk.Label(kartu,text=judul,font=("Segoe UI Emoji", 13, "bold"),bg="white",fg="#263B63")
        label_judul.pack(anchor="w")
        label_deskripsi = tk.Label(kartu,text=deskripsi,font=("Arial", 9), bg="white",fg="#777777")
        label_deskripsi.pack(anchor="w",pady=(4, 5))
        tombol = tk.Button(kartu, text="Buka Fitur",font=("Arial", 9, "bold"),bg="#365B9D",fg="white",relief="flat", cursor="hand2",command=perintah)
        tombol.pack(anchor="e")
        self.menu_widgets.append((label_judul, label_deskripsi, tombol))
    def tampilkan_profil(self):
        profil = tk.Toplevel(self)
        profil.title("Profil Pengguna")
        profil.geometry("350x250")
        profil.resizable(False, False)
        profil.configure(bg="white")
        tk.Label(profil,text="👤 Profil Pengguna",font=("Arial", 18, "bold"),bg="white",fg="#263B63").pack(pady=25)
        tk.Label(profil,text=f"Username: {self.username}",font=("Arial", 12),bg="white").pack(pady=10)
        tk.Button(profil,text="Tutup",bg="#365B9D",fg="white",relief="flat",command=profil.destroy).pack(pady=20)
    def tampilkan_pengaturan(self):
        pengaturan = tk.Toplevel(self)
        pengaturan.title("Pengaturan CAMPUS LIFE")
        pengaturan.geometry("420x480")
        pengaturan.resizable(False, False)
        pengaturan.configure(bg="white")
        tk.Label(pengaturan, text="⚙ Pengaturan",font=("Arial", 20, "bold"),bg="white",fg="#263B63").pack(pady=20)
        tk.Label(pengaturan,text="Bahasa Aplikasi",font=("Arial", 11, "bold"),bg="white").pack(anchor="w", padx=30)
        bahasa = tk.StringVar(value=self.language)
        tk.OptionMenu(pengaturan,bahasa,"Indonesia","English",command=self.ubah_bahasa).pack(fill="x", padx=30, pady=8)
        tk.Label(pengaturan,text="Musik Latar",font=("Arial", 11, "bold"), bg="white").pack(anchor="w",padx=30,pady=(15, 5))
        musik = tk.BooleanVar(value=self.music_on)
        tk.Checkbutton(pengaturan, text="Aktifkan musik", variable=musik, bg="white",command=lambda: self.toggle_musik(musik)).pack(anchor="w", padx=30)
        tk.Label(pengaturan,text="Volume Musik",font=("Arial", 11, "bold"),bg="white").pack(anchor="w",padx=30,pady=(15, 5))
        volume = tk.Scale( pengaturan,from_=0,to=100, orient="horizontal",bg="white",highlightthickness=0,command=self.ubah_volume)
        volume.set(self.volume)
        volume.pack(fill="x", padx=30)
        tk.Label(pengaturan, text="Latar Belakang",font=("Arial", 11, "bold"),bg="white").pack(anchor="w",padx=30,pady=(15, 5))
        tk.Button(pengaturan,text="Pilih Background dari Laptop",bg="#365B9D",fg="white", relief="flat", cursor="hand2",command=self.ganti_background).pack(fill="x", padx=30,pady=8)
        tk.Button(pengaturan,text="Tutup",bg="#777777",fg="white",relief="flat",command=pengaturan.destroy).pack(pady=20)
    def ubah_bahasa(self, bahasa):
        self.language = bahasa
        if bahasa == "Indonesia":
            self.lbl_dashboard.config(text="Dashboard")
            self.lbl_subtitle.config(text=f"Selamat datang kembali, {self.username}!")
            daftar = [("📝 Notes", "Catat materi dan ide kuliah", "Buka Fitur"),("✅ To-Do List", "Atur tugas dan deadline", "Buka Fitur"),("🥗Food Court","pilih menu di foodcourt dan lihat berapa biaya yang dikeluarkan" "Buka Fitur"),("🩺 Kesehatan","Cek kesehatan", "Buka Fitur")]
        else:
            self.lbl_dashboard.config(text="Dashboard")
            self.lbl_subtitle.config(text=f"Welcome back, {self.username}!")
            daftar = [("📝 Notes", "Write down your lecture notes", "Open Feature"),("✅ To-Do List", "Manage tasks and deadlines", "Open Feature"),("🥗Food Court", "Choose items from the menu at the food court and see how much it costs.", "Open Feature"),("🩺 Health","Health check", "Open Feature")]
        for widgets, teks in zip(self.menu_widgets, daftar):
            widgets[0].config(text=teks[0])
            widgets[1].config(text=teks[1])
            widgets[2].config(text=teks[2])
    def toggle_musik(self, musik):
        if musik.get():
            if not os.path.exists(self.music_path):
                messagebox.showwarning("Musik Tidak Ditemukan","File music.mp3 tidak ditemukan di folder assets.")
                musik.set(False)
                return
            try:
                import vlc
                if self.vlc_instance is None:
                    self.vlc_instance = vlc.Instance("--no-video","--quiet")
                if self.vlc_instance is None:
                    raise RuntimeError("VLC gagal dijalankan.")
                self.vlc_player = self.vlc_instance.media_player_new()
                self.vlc_media = self.vlc_instance.media_new(self.music_path)
                self.vlc_media.add_option(":input-repeat=-1")
                self.vlc_player.set_media( self.vlc_media)
                self.vlc_player.audio_set_volume(self.volume)
                hasil = self.vlc_player.play()
                if hasil == -1:
                    raise RuntimeError("VLC gagal memulai pemutaran musik.")
                self.music_on = True
                print("Musik berhasil diputar menggunakan VLC.")
            except Exception as e:
                self.music_on = False
                musik.set(False)
                self.hentikan_musik()
                messagebox.showerror("Musik Error",f"Gagal memutar musik:\n{e}")
        else:
            self.music_on = False
            self.hentikan_musik()
    def hentikan_musik(self):
        if self.vlc_player is not None:
            self.vlc_player.stop()
            self.vlc_player.release()
            self.vlc_player = None
        if self.vlc_media is not None:
            self.vlc_media.release()
            self.vlc_media = None
    def ubah_volume(self, nilai):
        self.volume = int(float(nilai))
        if self.vlc_player is not None:
            self.vlc_player.audio_set_volume(self.volume)
    def ganti_background(self):
        file_gambar = filedialog.askopenfilename(title="Pilih gambar background", filetypes=[("File gambar", "*.png *.jpg *.jpeg")])
        if file_gambar:
            try:
                gambar_baru = Image.open(file_gambar).convert("RGB")
                self.bg_original = gambar_baru
                self.update_idletasks()
                event = type("Event", (), {"width": self.winfo_width(), "height": self.winfo_height()})()
                self.atur_background(event)
                messagebox.showinfo("Berhasil", "Background berhasil diganti!")
            except Exception as e:
                messagebox.showerror("Gagal", f"Gambar tidak dapat dibuka:\n{e}")
    def logout(self):
        self.music_on = False
        self.hentikan_musik()
        if self.vlc_instance is not None:
            self.vlc_instance.release()
            self.vlc_instance = None
        self.on_logout()
    def belum_tersedia(self):
        messagebox.showinfo("Informasi","Fitur ini akan segera tersedia!")
