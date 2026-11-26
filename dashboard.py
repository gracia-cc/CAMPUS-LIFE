
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageEnhance
import os, json

class DashboardPage(tk.Frame):
    def __init__(self, master, username, on_logout):
        super().__init__(master, bg="#F4F6FA")
        self.username, self.on_logout = username, on_logout
        self.language, self.music_on, self.volume = "Indonesia", False, 50
        self.vlc_instance, self.vlc_player, self.vlc_media = None, None, None
        lokasi = os.path.dirname(os.path.abspath(__file__))
        self.music_path = os.path.join(lokasi, "assets", "music.mp3")
        self.settings_path = os.path.join(lokasi, "settings.json")
        gambar_default = os.path.join(lokasi, "assets", "background.png")
        self.bg_label = tk.Label(self, bg="#F4F6FA")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()
        self.bg_original, self.bg_photo = None, None
        bg_path = self.load_background_setting()
        gambar_path = bg_path if bg_path and os.path.exists(bg_path) else gambar_default
        try:
            self.bg_original = Image.open(gambar_path).convert("RGB")
        except (FileNotFoundError, OSError) as e:
            print("Background tidak ditemukan:", e)
        self.bind("<Configure>", self.atur_background)
        self.after_idle(self.atur_background)
        header = tk.Frame(self, bg="#365B9D", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="CAMPUS LIFE", font=("Arial", 20, "bold"),
                 bg="#365B9D", fg="white").pack(side="left", padx=25)
        self.btn_profil = tk.Menubutton(
            header, text=f"👤 {username}  ▼", font=("Arial", 10, "bold"),
            bg="#263B63", fg="white", activebackground="#1E2F4F",
            activeforeground="white", relief="flat", cursor="hand2",
            padx=12, pady=6)
        self.btn_profil.pack(side="right", padx=(5, 20), pady=20)
        menu_profil = tk.Menu(self.btn_profil, tearoff=0, font=("Arial", 10))
        menu_profil.add_command(label="👤  Profil Saya", command=self.tampilkan_profil)
        menu_profil.add_command(label="⚙️  Pengaturan", command=self.tampilkan_pengaturan)
        menu_profil.add_separator()
        menu_profil.add_command(label="🚪  Logout", command=self.logout)
        self.btn_profil.configure(menu=menu_profil)
        judul_card = tk.Frame(self, bg="white", padx=20, pady=15)
        judul_card.pack(fill="x", padx=30, pady=(20, 10))
        self.lbl_dashboard = tk.Label(judul_card, text="Beranda", font=("Arial", 24, "bold"),bg="white", fg="#263B63")
        self.lbl_dashboard.pack(anchor="w")
        self.lbl_subtitle = tk.Label(judul_card, text=f"Selamat datang kembali, {username}!",font=("Arial", 12), bg="white", fg="#777777")
        self.lbl_subtitle.pack(anchor="w", pady=(2, 0))
        ringkasan = tk.Frame(self, bg="#F4F6FA")
        ringkasan.pack(fill="x", padx=30, pady=(0, 10))
        self.buat_mini_card(ringkasan, "Tugas Belum Selesai", "2")
        self.buat_mini_card(ringkasan, "Total Catatan", "5")
        self.buat_mini_card(ringkasan, "Jadwal Berikutnya", "10.00")
        tk.Label(self, text="Menu Fitur", font=("Arial", 13, "bold"),bg="#F4F6FA", fg="#263B63").pack(anchor="w", padx=30, pady=(5, 5))
        menu = tk.Frame(self, bg="#F4F6FA")
        menu.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        menu.grid_columnconfigure(0, weight=1)
        menu.grid_columnconfigure(1, weight=1)
        menu.grid_rowconfigure(0, weight=1)
        menu.grid_rowconfigure(1, weight=1)
        self.menu_widgets = []
        self.buat_menu(menu, "📝", "Notes", "Catat materi dan ide kuliah", self.belum_tersedia, 0, 0)
        self.buat_menu(menu, "✅", "To-Do List", "Atur tugas dan deadline", self.belum_tersedia, 0, 1)
        self.buat_menu(menu, "🥗", "Food Court", "Pilih menu dan lihat biaya", self.belum_tersedia, 1, 0)
        self.buat_menu(menu, "🩺", "Kesehatan", "Cek kesehatan", self.belum_tersedia, 1, 1)
    def buat_mini_card(self, parent, judul, angka):
        f = tk.Frame(parent, bg="white", relief="flat", padx=12, pady=10)
        f.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(f, text=judul, font=("Arial", 10), bg="white", fg="#777777").pack(anchor="w")
        tk.Label(f, text=str(angka), font=("Arial", 20, "bold"), bg="white", fg="#263B63").pack(anchor="w", pady=(2, 0))
    def atur_background(self, event=None):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10 or self.bg_original is None:
            return
        if getattr(self, "_last_bg_size", None) == (w, h):
            return
        self._last_bg_size = (w, h)
        gambar = self.bg_original.resize((w, h), Image.Resampling.LANCZOS)
        gambar = ImageEnhance.Brightness(gambar).enhance(0.6)
        self.bg_photo = ImageTk.PhotoImage(gambar)
        self.bg_label.configure(image=self.bg_photo)
        self.bg_label.lower()
    def buat_menu(self, parent, icon, judul, deskripsi, perintah, row, col):
        warna = "#FFFFFF"
        card = tk.Frame(parent, bg=warna, relief="solid", bd=1, cursor="hand2")
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        lbl_icon = tk.Label(card, text=icon, font=("Segoe UI Emoji", 32), bg=warna, fg="#263B63")
        lbl_icon.pack(pady=(12, 3))
        lbl_judul = tk.Label(card, text=judul, font=("Arial", 14, "bold"), bg=warna, fg="#263B63")
        lbl_judul.pack(pady=(2, 4))
        lbl_desk = tk.Label(card, text=deskripsi, font=("Arial", 7),bg=warna, fg="#666666", wraplength=350, justify="center",anchor="center")
        lbl_desk.pack(pady=(2, 12))
        widgets = [card, lbl_icon, lbl_judul, lbl_desk]
        for widget in widgets:
            widget.bind("<Button-1>", lambda e: perintah())
        self.menu_widgets.append((lbl_judul, lbl_desk))
    def load_background_setting(self):
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    return json.load(f).get("background")
        except Exception as e:
            print("Gagal membaca pengaturan:", e)
        return None
    def save_background_setting(self, path):
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump({"background": path}, f, indent=4)
        except Exception as e:
            print("Gagal simpan settings:", e)
    def tampilkan_profil(self):
        profil = tk.Toplevel(self)
        profil.title("Profil Pengguna")
        profil.geometry("350x250")
        profil.resizable(False, False)
        profil.configure(bg="white")
        tk.Label(profil, text="👤 Profil Pengguna", font=("Arial", 18, "bold"),bg="white", fg="#263B63").pack(pady=25)
        tk.Label(profil, text=f"Username: {self.username}",font=("Arial", 12), bg="white").pack(pady=10)
        tk.Button(profil, text="Tutup", bg="#365B9D", fg="white",relief="flat", command=profil.destroy).pack(pady=20)
    def tampilkan_pengaturan(self):
        pengaturan = tk.Toplevel(self)
        pengaturan.title("Pengaturan CAMPUS LIFE")
        pengaturan.geometry("420x480")
        pengaturan.resizable(False, False)
        pengaturan.configure(bg="white")
        tk.Label(pengaturan, text="⚙ Pengaturan", font=("Arial", 20, "bold"),bg="white", fg="#263B63").pack(pady=20)
        tk.Label(pengaturan, text="Musik Latar", font=("Arial", 11, "bold"),bg="white").pack(anchor="w", padx=30, pady=(15, 5))
        musik = tk.BooleanVar(value=self.music_on)
        tk.Checkbutton(pengaturan, text="Aktifkan musik", variable=musik,bg="white", command=lambda: self.toggle_musik(musik)).pack(anchor="w", padx=30)
        tk.Label(pengaturan, text="Volume Musik", font=("Arial", 11, "bold"),bg="white").pack(anchor="w", padx=30, pady=(15, 5))
        volume = tk.Scale(pengaturan, from_=0, to=100, orient="horizontal",bg="white", highlightthickness=0, command=self.ubah_volume)
        volume.set(self.volume)
        volume.pack(fill="x", padx=30)
        tk.Label(pengaturan, text="Latar Belakang", font=("Arial", 11, "bold"),bg="white").pack(anchor="w", padx=30, pady=(15, 5))
        tk.Button(pengaturan, text="Pilih Background dari Laptop",bg="#365B9D", fg="white", relief="flat", cursor="hand2",command=self.ganti_background).pack(fill="x", padx=30, pady=8)
        tk.Button(pengaturan, text="Kembalikan ke Default",bg="white", fg="#365B9D", relief="flat",cursor="hand2", command=self.reset_background).pack(fill="x", padx=30, pady=4)
        tk.Button(pengaturan, text="Tutup", bg="#777777", fg="white",relief="flat", command=pengaturan.destroy).pack(pady=20)
    def toggle_musik(self, musik):
        if musik.get():
            if not os.path.exists(self.music_path):
                messagebox.showwarning("Musik Tidak Ditemukan", "File music.mp3 tidak ditemukan di folder assets.")
                musik.set(False)
                return
            try:
                import vlc
                if self.vlc_instance is None:
                    self.vlc_instance = vlc.Instance("--no-video", "--quiet")
                if self.vlc_instance is None:
                    raise RuntimeError("VLC gagal dijalankan.")
                self.vlc_player = self.vlc_instance.media_player_new()
                self.vlc_media = self.vlc_instance.media_new(self.music_path)
                self.vlc_media.add_option(":input-repeat=-1")
                self.vlc_player.set_media(self.vlc_media)
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
                messagebox.showerror("Musik Error", f"Gagal memutar musik:\n{e}")
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
        file_gambar = filedialog.askopenfilename(title="Pilih gambar background",filetypes=[("File gambar", "*.png *.jpg *.jpeg")])
        if file_gambar:
            try:
                gambar_baru = Image.open(file_gambar).convert("RGB")
                self.bg_original = gambar_baru
                self.save_background_setting(file_gambar)
                self._last_bg_size = None
                self.atur_background()
                messagebox.showinfo("Berhasil", "Background berhasil diganti dan tersimpan!")
            except Exception as e:
                messagebox.showerror("Gagal", f"Gambar tidak dapat dibuka:\n{e}")
    def reset_background(self):
        lokasi = os.path.dirname(os.path.abspath(__file__))
        default = os.path.join(lokasi, "assets", "background.png")
        try:
            self.bg_original = Image.open(default).convert("RGB")
            self.save_background_setting(default)
            self._last_bg_size = None
            self.atur_background()
            messagebox.showinfo("Berhasil", "Background dikembalikan ke default!")
        except Exception as e:
            messagebox.showerror("Gagal", f"{e}")
    def logout(self):
        self.music_on = False
        self.hentikan_musik()
        if self.vlc_instance is not None:
            self.vlc_instance.release()
            self.vlc_instance = None
        self.on_logout()
    def belum_tersedia(self):
        messagebox.showinfo("Informasi", "Fitur ini akan segera tersedia!")
