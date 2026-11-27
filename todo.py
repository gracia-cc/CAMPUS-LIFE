import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import calendar
from datetime import datetime, timedelta

JADWAL_AWAL = [
    ("PD_SENIN", "Pemrograman Dasar", 3, "2026", "E2.01.04", "Senin", "13:00", "15:30"),
    ("PD_KAMIS", "Pemrograman Dasar", 3, "2026", "E2.01.04", "Kamis", "13:00", "14:40"),
    ("MD_SEL", "Matematika Diskrit", 3, "2026", "E2.01.02", "Selasa", "07:00", "09:30"),
    ("AKSO_JUMAT", "Arsitektur Komputer dan Sistem Operasi", 3, "2026C", "E2.01.09", "Jumat", "07:00", "09:30"),
    ("AM_RABU", "Aljabar Matriks", 3, "2026", "E2.01.08", "Rabu", "13:00", "15:30"),
    ("MTK_KAMIS", "Matematika Dasar", 3, "2026", "E2.01.06", "Kamis", "15:30", "18:00"),
    ("ING_SEL", "Bahasa Inggris", 2, "2026", "VIRTUAL", "Selasa", "14:40", "16:10"),
    ("AGAMA_SENIN", "Agama Islam", 2, "2026", "VIRTUAL", "Senin", "16:20", "18:00"),
]

DAFTAR_HARI = [
    "Senin", "Selasa", "Rabu", "Kamis",
    "Jumat", "Sabtu", "Minggu"
]

NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April",
    "Mei", "Juni", "Juli", "Agustus",
    "September", "Oktober", "November", "Desember"
]

NAMA_HARI = [
    "Senin", "Selasa", "Rabu", "Kamis",
    "Jumat", "Sabtu", "Minggu"
]


def koneksi_database():
    lokasi_db = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "database.db"   )
    return sqlite3.connect(lokasi_db)

def buat_tabel_todo():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            nama_tugas TEXT NOT NULL,
            mata_kuliah TEXT NOT NULL,
            deadline TEXT NOT NULL,
            selesai INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Pastikan kolom selesai tersedia jika database dibuat sebelum pembaruan ini
    kolom_ada = [row[1] for row in cursor.execute("PRAGMA table_info(tugas)").fetchall()]
    if "selesai" not in kolom_ada:
        cursor.execute("ALTER TABLE tugas ADD COLUMN selesai INTEGER NOT NULL DEFAULT 0")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jadwal_kuliah (
            id_jadwal TEXT NOT NULL,
            username TEXT NOT NULL,
            mata_kuliah TEXT NOT NULL,
            sks INTEGER NOT NULL,
            kelas TEXT NOT NULL,
            ruangan TEXT NOT NULL,
            hari TEXT NOT NULL,
            jam_mulai TEXT NOT NULL,
            jam_selesai TEXT NOT NULL,
            PRIMARY KEY (id_jadwal, username)
        )
    """)

    conn.commit()
    conn.close()


class TodoPage(tk.Frame):

    def __init__(self, master, username, on_back=None, notifikasi_aktif=True):
        super().__init__(master, bg="#F4F6FA")

        self.username = username
        self.on_back = on_back
        self.notifikasi_aktif = notifikasi_aktif

        buat_tabel_todo()
        self.siapkan_jadwal_awal()

        self.sudah_diberi_notifikasi = set()
        self.after_jam = None
        self.after_notifikasi = None
        self.jadwal_terpilih_id = None
        self.peta_tugas_row = {}
        self.toast_aktif = None

        sekarang = datetime.now()
        self.bulan_kalender = sekarang.month
        self.tahun_kalender = sekarang.year
        self.tanggal_terpilih = sekarang.strftime("%Y-%m-%d")

        self.tampilkan_selesai_var = tk.BooleanVar(value=False)

        self.buat_tampilan()
        self.tampilkan_jadwal()
        self.tampilkan_tugas()
        self.tampilkan_kalender()
        self.perbarui_jam()

        self.bind("<Destroy>", self.bersihkan_timer)
        self.after_notifikasi = self.after(1200, self.cek_notifikasi)

    def bersihkan_timer(self, event=None):
        if event is not None and event.widget is not self:
            return
        if self.after_jam is not None:
            try:
                self.after_cancel(self.after_jam)
            except tk.TclError:
                pass
            self.after_jam = None
        if self.after_notifikasi is not None:
            try:
                self.after_cancel(self.after_notifikasi)
            except tk.TclError:
                pass
            self.after_notifikasi = None
        if self.toast_aktif is not None and self.toast_aktif.winfo_exists():
            try:
                self.toast_aktif.destroy()
            except tk.TclError:
                pass

    def siapkan_jadwal_awal(self):
        conn = koneksi_database()
        cursor = conn.cursor()
        jumlah = cursor.execute(
            "SELECT COUNT(*) FROM jadwal_kuliah WHERE username = ?",
            (self.username,)
        ).fetchone()[0]
        if jumlah == 0:
            for item in JADWAL_AWAL:
                cursor.execute("""
                    INSERT OR IGNORE INTO jadwal_kuliah
                    (id_jadwal, username, mata_kuliah, sks, kelas, ruangan, hari, jam_mulai, jam_selesai)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (item[0], self.username, item[1], item[2], item[3], item[4], item[5], item[6], item[7]))
            conn.commit()
        conn.close()

    def kembali(self):
        if self.on_back:
            self.on_back()
        else:
            self.destroy()

    def buat_tampilan(self):
        self.bagian_atas = tk.Frame(self, bg="#365B9D", height=64)
        self.bagian_atas.pack(fill="x")
        self.bagian_atas.pack_propagate(False)

        tk.Button(
            self.bagian_atas,
            text="← Kembali",
            command=self.kembali,
            bg="#263B63",
            fg="white",
            activebackground="#1E2F4F",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2"
        ).pack(side="left", padx=(20, 12), pady=14)

        tk.Label(
            self.bagian_atas,
            text="CampusLife | To-Do List & Jadwal Kuliah",
            font=("Arial", 16, "bold"),
            bg="#365B9D",
            fg="white"
        ).pack(side="left")

        self.label_ringkasan = tk.Label(
            self.bagian_atas,
            text="",
            font=("Arial", 9, "bold"),
            bg="#263B63",
            fg="white",
            padx=12,
            pady=6
        )
        self.label_ringkasan.pack(side="right", padx=20)

        # Banner notifikasi di dalam aplikasi (tampil otomatis saat ada deadline dekat/terlewat)
        self.banner_notif = tk.Frame(
            self,
            bg="#FEF3C7",
            highlightbackground="#F59E0B",
            highlightthickness=1
        )
        self.label_banner_notif = tk.Label(
            self.banner_notif,
            text="",
            bg="#FEF3C7",
            fg="#92400E",
            font=("Arial", 10, "bold"),
            anchor="w",
            justify="left"
        )
        self.label_banner_notif.pack(side="left", fill="x", expand=True, padx=14, pady=8)
        tk.Button(
            self.banner_notif,
            text="✕",
            command=lambda: self.banner_notif.pack_forget(),
            bg="#FEF3C7",
            fg="#92400E",
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="right", padx=10)

        # Area utama yang dapat di-scroll
        wadah_scroll = tk.Frame(self, bg="#F4F6FA")
        wadah_scroll.pack(fill="both", expand=True)

        self.canvas_scroll = tk.Canvas(wadah_scroll, bg="#F4F6FA", highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(wadah_scroll, orient="vertical", command=self.canvas_scroll.yview)
        self.canvas_scroll.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_y.pack(side="right", fill="y")
        self.canvas_scroll.pack(side="left", fill="both", expand=True)

        self.frame_scroll = tk.Frame(self.canvas_scroll, bg="#F4F6FA")
        self.window_scroll = self.canvas_scroll.create_window((0, 0), window=self.frame_scroll, anchor="nw")

        self.frame_scroll.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))
        )
        self.canvas_scroll.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.itemconfigure(self.window_scroll, width=e.width)
        )

        def _on_mousewheel(event):
            if self.canvas_scroll.winfo_exists():
                self.canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas_scroll.bind("<Enter>", lambda e: self.canvas_scroll.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas_scroll.bind("<Leave>", lambda e: self.canvas_scroll.unbind_all("<MouseWheel>"))

        # Panel Jam Real-time & Kalender Interaktif
        panel_waktu = tk.Frame(
            self.frame_scroll,
            bg="white",
            highlightbackground="#E1E7EF",
            highlightthickness=1
        )
        panel_waktu.pack(fill="x", padx=20, pady=12)

        panel_jam = tk.Frame(panel_waktu, bg="white")
        panel_jam.pack(side="left", fill="y", padx=22, pady=15)

        tk.Label(
            panel_jam,
            text="WAKTU REAL-TIME SEKARANG",
            bg="white",
            fg="#718096",
            font=("Arial", 9, "bold")
        ).pack(anchor="w")

        self.label_jam = tk.Label(
            panel_jam,
            text="00:00:00",
            bg="white",
            fg="#243247",
            font=("Arial", 30, "bold")
        )
        self.label_jam.pack(anchor="w", pady=(4, 0))

        self.label_tanggal = tk.Label(
            panel_jam,
            text="",
            bg="white",
            fg="#64748B",
            font=("Arial", 10)
        )
        self.label_tanggal.pack(anchor="w", pady=(3, 10))

        self.label_info_kalender = tk.Label(
            panel_jam,
            text=f"Tanggal deadline terpilih: {self.tanggal_terpilih}",
            bg="#EFF6FF",
            fg="#1D4ED8",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5
        )
        self.label_info_kalender.pack(anchor="w")

        tk.Label(
            panel_jam,
            text="Klik tanggal pada kalender untuk mengisi deadline otomatis.\nTanda • menandakan ada tugas aktif pada tanggal tersebut.",
            bg="white",
            fg="#64748B",
            font=("Arial", 8),
            justify="left"
        ).pack(anchor="w", pady=(8, 0))

        ttk.Separator(panel_waktu, orient="vertical").pack(side="left", fill="y", padx=8, pady=12)

        panel_kalender = tk.Frame(panel_waktu, bg="white")
        panel_kalender.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        navigasi = tk.Frame(panel_kalender, bg="white")
        navigasi.pack(fill="x")

        tk.Button(
            navigasi,
            text="‹",
            command=self.bulan_sebelumnya,
            bg="#F1F5F9",
            fg="#243247",
            relief="flat",
            font=("Arial", 13, "bold"),
            width=3,
            cursor="hand2"
        ).pack(side="left")

        self.label_bulan = tk.Label(
            navigasi,
            text="",
            bg="white",
            fg="#243247",
            font=("Arial", 11, "bold"),
            width=18
        )
        self.label_bulan.pack(side="left", padx=8)

        tk.Button(
            navigasi,
            text="›",
            command=self.bulan_berikutnya,
            bg="#F1F5F9",
            fg="#243247",
            relief="flat",
            font=("Arial", 13, "bold"),
            width=3,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            navigasi,
            text="Hari Ini",
            command=self.lompat_hari_ini,
            bg="#E0E7FF",
            fg="#1E40AF",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=3,
            cursor="hand2"
        ).pack(side="right")

        self.frame_kalender = tk.Frame(panel_kalender, bg="white")
        self.frame_kalender.pack(pady=(8, 0), anchor="w")

        # Konten Utama (Tugas & Jadwal)
        konten = tk.Frame(self.frame_scroll, bg="#F4F6FA")
        konten.pack(fill="both", expand=True, padx=20, pady=5)

        panel_tugas = tk.LabelFrame(
            konten,
            text="  TO-DO LIST / DAFTAR TUGAS  ",
            bg="white",
            fg="#243247",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=10
        )
        panel_tugas.pack(fill="x", pady=(0, 12))

        form = tk.Frame(panel_tugas, bg="white")
        form.pack(fill="x")

        tk.Label(form, text="Nama tugas", bg="white", font=("Arial", 9, "bold")).grid(
            row=0, column=0, sticky="w", padx=5, pady=4
        )
        self.input_tugas = ttk.Entry(form, width=28)
        self.input_tugas.grid(row=1, column=0, padx=5, pady=3, sticky="ew")

        tk.Label(form, text="Mata kuliah", bg="white", font=("Arial", 9, "bold")).grid(
            row=0, column=1, sticky="w", padx=5, pady=4
        )
        self.pilihan_matkul = ttk.Combobox(form, width=32, state="readonly")
        self.pilihan_matkul.grid(row=1, column=1, padx=5, pady=3, sticky="ew")

        tk.Label(form, text="Tanggal deadline (YYYY-MM-DD)", bg="white", font=("Arial", 9, "bold")).grid(
            row=0, column=2, sticky="w", padx=5, pady=4
        )
        self.input_tanggal = ttk.Entry(form, width=18)
        self.input_tanggal.grid(row=1, column=2, padx=5, pady=3, sticky="ew")
        self.input_tanggal.insert(0, self.tanggal_terpilih)

        tk.Label(form, text="Jam deadline (HH:MM)", bg="white", font=("Arial", 9, "bold")).grid(
            row=0, column=3, sticky="w", padx=5, pady=4
        )
        frame_jam = tk.Frame(form, bg="white")
        frame_jam.grid(row=1, column=3, padx=5, pady=3, sticky="ew")

        self.input_jam = ttk.Entry(frame_jam, width=8)
        self.input_jam.pack(side="left")
        self.input_jam.insert(0, "23:59")

        for preset in ("09:00", "13:00", "18:00", "23:59"):
            tk.Button(
                frame_jam,
                text=preset,
                command=lambda p=preset: self.atur_jam_cepat(p),
                bg="#F1F5F9",
                fg="#334155",
                relief="flat",
                font=("Arial", 8),
                padx=4,
                pady=2,
                cursor="hand2"
            ).pack(side="left", padx=(3, 0))

        for kolom in range(4):
            form.grid_columnconfigure(kolom, weight=1)

        tombol_tugas = tk.Frame(panel_tugas, bg="white")
        tombol_tugas.pack(fill="x", pady=10)

        tk.Button(
            tombol_tugas,
            text="+ Tambah Tugas",
            command=self.tambah_tugas,
            bg="#2563EB",
            fg="white",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            tombol_tugas,
            text="✓ Centang / Selesaikan Tugas",
            command=self.selesaikan_tugas_terpilih,
            bg="#16A34A",
            fg="white",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="left", padx=8)

        tk.Button(
            tombol_tugas,
            text="🗑 Hapus Tugas",
            command=self.hapus_tugas,
            bg="#DC2626",
            fg="white",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="left")

        tk.Checkbutton(
            tombol_tugas,
            text="Tampilkan tugas yang sudah dicentang",
            variable=self.tampilkan_selesai_var,
            command=self.tampilkan_tugas,
            bg="white",
            fg="#475569",
            font=("Arial", 9),
            cursor="hand2"
        ).pack(side="right")

        tk.Label(
            panel_tugas,
            text="Tip: Klik kolom kotak centang (☐) di sebelah kiri nama tugas untuk menandai selesai — tugas yang dicentang otomatis hilang dari daftar aktif.",
            bg="white",
            fg="#64748B",
            font=("Arial", 8)
        ).pack(anchor="w", pady=(0, 6))

        kolom_tugas = ("cek", "nama", "matkul", "deadline", "status")
        self.tabel_tugas = ttk.Treeview(
            panel_tugas,
            columns=kolom_tugas,
            show="headings",
            height=7
        )

        self.tabel_tugas.heading("cek", text="Centang")
        self.tabel_tugas.heading("nama", text="Nama Tugas")
        self.tabel_tugas.heading("matkul", text="Mata Kuliah")
        self.tabel_tugas.heading("deadline", text="Deadline")
        self.tabel_tugas.heading("status", text="Status & Sisa Waktu")

        self.tabel_tugas.column("cek", width=70, anchor="center", stretch=False)
        self.tabel_tugas.column("nama", width=220)
        self.tabel_tugas.column("matkul", width=210)
        self.tabel_tugas.column("deadline", width=135, anchor="center")
        self.tabel_tugas.column("status", width=260)

        self.tabel_tugas.pack(fill="x", pady=(2, 0))

        self.tabel_tugas.bind("<ButtonRelease-1>", self.klik_tabel_tugas)
        self.tabel_tugas.bind("<Double-1>", self.double_klik_tugas)

        self.tabel_tugas.tag_configure("terlambat", foreground="#B91C1C", background="#FEE2E2")
        self.tabel_tugas.tag_configure("mendesak", foreground="#C2410C", background="#FFEDD5")
        self.tabel_tugas.tag_configure("dekat", foreground="#B45309", background="#FEF3C7")
        self.tabel_tugas.tag_configure("segera", foreground="#854D0E", background="#FEFCE8")
        self.tabel_tugas.tag_configure("aman", foreground="#15803D", background="white")
        self.tabel_tugas.tag_configure("selesai", foreground="#64748B", background="#F1F5F9")

        # Panel Jadwal Kuliah
        panel_jadwal = tk.LabelFrame(
            konten,
            text="  JADWAL KULIAH  ",
            bg="white",
            fg="#243247",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=10
        )
        panel_jadwal.pack(fill="both", expand=True, pady=(0, 15))

        tk.Label(
            panel_jadwal,
            text="Mata kuliah, SKS, dan kelas tidak dapat diubah. Pilih jadwal untuk mengubah ruangan, hari, atau jam.",
            bg="white",
            fg="#64748B",
            font=("Arial", 9)
        ).pack(anchor="w", pady=(0, 7))

        kolom_jadwal = ("matkul", "sks", "kelas", "ruangan", "hari", "waktu")
        self.tabel_jadwal = ttk.Treeview(
            panel_jadwal,
            columns=kolom_jadwal,
            show="headings",
            height=7
        )

        judul = {
            "matkul": "Mata Kuliah",
            "sks": "SKS",
            "kelas": "Kelas",
            "ruangan": "Ruangan",
            "hari": "Hari",
            "waktu": "Jam Kuliah"
        }

        lebar = {
            "matkul": 300,
            "sks": 55,
            "kelas": 75,
            "ruangan": 105,
            "hari": 95,
            "waktu": 130
        }

        for kolom in kolom_jadwal:
            self.tabel_jadwal.heading(kolom, text=judul[kolom])
            self.tabel_jadwal.column(
                kolom,
                width=lebar[kolom],
                anchor="center" if kolom != "matkul" else "w"
            )

        self.tabel_jadwal.pack(fill="both", expand=True)
        self.tabel_jadwal.bind("<<TreeviewSelect>>", self.pilih_jadwal)

        editor = tk.Frame(panel_jadwal, bg="white")
        editor.pack(fill="x", pady=(10, 0))

        tk.Label(editor, text="Ruangan", bg="white").grid(row=0, column=0, padx=5, sticky="w")
        self.edit_ruangan = ttk.Entry(editor, width=18)
        self.edit_ruangan.grid(row=1, column=0, padx=5, pady=4)

        tk.Label(editor, text="Hari", bg="white").grid(row=0, column=1, padx=5, sticky="w")
        self.edit_hari = ttk.Combobox(editor, values=DAFTAR_HARI, state="readonly", width=15)
        self.edit_hari.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(editor, text="Jam mulai (HH:MM)", bg="white").grid(row=0, column=2, padx=5, sticky="w")
        self.edit_mulai = ttk.Entry(editor, width=15)
        self.edit_mulai.grid(row=1, column=2, padx=5, pady=4)

        tk.Label(editor, text="Jam selesai (HH:MM)", bg="white").grid(row=0, column=3, padx=5, sticky="w")
        self.edit_selesai = ttk.Entry(editor, width=15)
        self.edit_selesai.grid(row=1, column=3, padx=5, pady=4)

        tk.Button(
            editor,
            text="Simpan Perubahan Jadwal",
            command=self.simpan_perubahan_jadwal,
            bg="#0F766E",
            fg="white",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=7,
            cursor="hand2"
        ).grid(row=1, column=4, padx=10)

        self.label_pesan_jadwal = tk.Label(
            panel_jadwal,
            text="Pilih salah satu baris jadwal untuk mengedit.",
            bg="white",
            fg="#64748B",
            font=("Arial", 9)
        )
        self.label_pesan_jadwal.pack(anchor="w", pady=(5, 0))

    def atur_jam_cepat(self, jam_str):
        self.input_jam.delete(0, tk.END)
        self.input_jam.insert(0, jam_str)

    def perbarui_jam(self):
        if not self.winfo_exists():
            return
        sekarang = datetime.now()
        self.label_jam.config(text=sekarang.strftime("%H:%M:%S"))
        hari = NAMA_HARI[sekarang.weekday()]
        bulan = NAMA_BULAN[sekarang.month - 1]
        self.label_tanggal.config(text=f"{hari}, {sekarang.day} {bulan} {sekarang.year}")

        # Refresh status tabel setiap pergantian menit agar status deadline tetap real-time
        if sekarang.second == 0:
            self.tampilkan_tugas()

        self.after_jam = self.after(1000, self.perbarui_jam)

    def ambil_tanggal_bertugas(self):
        conn = koneksi_database()
        rows = conn.execute(
            "SELECT deadline FROM tugas WHERE username = ? AND COALESCE(selesai, 0) = 0",
            (self.username,)
        ).fetchall()
        conn.close()
        hasil = {}
        sekarang = datetime.now()
        for (dl_str,) in rows:
            try:
                dl_dt = datetime.strptime(dl_str, "%Y-%m-%d %H:%M")
                tgl = dl_dt.strftime("%Y-%m-%d")
                if dl_dt < sekarang:
                    hasil[tgl] = "terlambat"
                elif dl_dt - sekarang <= timedelta(hours=24):
                    if hasil.get(tgl) != "terlambat":
                        hasil[tgl] = "dekat"
                else:
                    if tgl not in hasil:
                        hasil[tgl] = "aman"
            except ValueError:
                pass
        return hasil

    def tampilkan_kalender(self):
        for widget in self.frame_kalender.winfo_children():
            widget.destroy()

        nama_bulan = NAMA_BULAN[self.bulan_kalender - 1]
        self.label_bulan.config(text=f"{nama_bulan} {self.tahun_kalender}")

        header_hari = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
        for col, nama in enumerate(header_hari):
            fg = "#DC2626" if col == 6 else "#475569"
            tk.Label(
                self.frame_kalender,
                text=nama,
                bg="white",
                fg=fg,
                font=("Arial", 8, "bold"),
                width=5
            ).grid(row=0, column=col, padx=1, pady=2)

        sekarang_str = datetime.now().strftime("%Y-%m-%d")
        peta_deadline = self.ambil_tanggal_bertugas()
        kalender_bulan = calendar.monthcalendar(self.tahun_kalender, self.bulan_kalender)

        for r, minggu in enumerate(kalender_bulan, start=1):
            for c, tgl in enumerate(minggu):
                if tgl == 0:
                    tk.Label(self.frame_kalender, text="", bg="white", width=5).grid(row=r, column=c, padx=1, pady=1)
                    continue

                tgl_str = f"{self.tahun_kalender:04d}-{self.bulan_kalender:02d}-{tgl:02d}"
                status_dl = peta_deadline.get(tgl_str)
                teks = f"{tgl}•" if status_dl else str(tgl)

                if tgl_str == self.tanggal_terpilih:
                    bg, fg = "#0F766E", "white"
                elif tgl_str == sekarang_str:
                    bg, fg = "#2563EB", "white"
                elif status_dl == "terlambat":
                    bg, fg = "#FEE2E2", "#B91C1C"
                elif status_dl == "dekat":
                    bg, fg = "#FEF3C7", "#B45309"
                elif status_dl == "aman":
                    bg, fg = "#DCFCE7", "#15803D"
                else:
                    bg = "#F8FAFC"
                    fg = "#DC2626" if c == 6 else "#1E293B"

                btn = tk.Button(
                    self.frame_kalender,
                    text=teks,
                    width=5,
                    bg=bg,
                    fg=fg,
                    relief="flat",
                    font=("Arial", 8, "bold" if (tgl_str in (sekarang_str, self.tanggal_terpilih) or status_dl) else "normal"),
                    cursor="hand2",
                    command=lambda s=tgl_str: self.pilih_tanggal_kalender(s)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)

    def pilih_tanggal_kalender(self, tanggal_str):
        self.tanggal_terpilih = tanggal_str
        self.input_tanggal.delete(0, tk.END)
        self.input_tanggal.insert(0, tanggal_str)
        self.label_info_kalender.config(text=f"Tanggal deadline terpilih: {tanggal_str}")
        self.tampilkan_kalender()

    def lompat_hari_ini(self):
        sekarang = datetime.now()
        self.bulan_kalender = sekarang.month
        self.tahun_kalender = sekarang.year
        self.pilih_tanggal_kalender(sekarang.strftime("%Y-%m-%d"))

    def bulan_sebelumnya(self):
        if self.bulan_kalender == 1:
            self.bulan_kalender = 12
            self.tahun_kalender -= 1
        else:
            self.bulan_kalender -= 1
        self.tampilkan_kalender()

    def bulan_berikutnya(self):
        if self.bulan_kalender == 12:
            self.bulan_kalender = 1
            self.tahun_kalender += 1
        else:
            self.bulan_kalender += 1
        self.tampilkan_kalender()

    def format_sisa_waktu(self, selisih):
        total_detik = int(abs(selisih.total_seconds()))
        hari = total_detik // 86400
        jam = (total_detik % 86400) // 3600
        menit = (total_detik % 3600) // 60
        if hari > 0:
            return f"{hari} hari {jam} jam"
        if jam > 0:
            return f"{jam} jam {menit} mnt"
        return f"{max(1, menit)} menit"

    def evaluasi_status_tugas(self, deadline_str, selesai, sekarang):
        if selesai:
            return "selesai", "✔ Selesai"
        try:
            dl_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return "aman", "Format deadline tidak standar"

        selisih = dl_dt - sekarang
        detik = selisih.total_seconds()
        teks_durasi = self.format_sisa_waktu(selisih)

        if detik < 0:
            return "terlambat", f"⛔ MELEBIHI DEADLINE (terlambat {teks_durasi})"
        if detik <= 3 * 3600:
            return "mendesak", f"🔥 MENDEKATI DEADLINE! ({teks_durasi} lagi)"
        if detik <= 24 * 3600:
            return "dekat", f"⚠ MENDEKATI DEADLINE ({teks_durasi} lagi)"
        if detik <= 72 * 3600:
            return "segera", f"🟡 Segera ({teks_durasi} lagi)"
        return "aman", f"🟢 Aman ({teks_durasi} lagi)"

    def tampilkan_tugas(self):
        for item in self.tabel_tugas.get_children():
            self.tabel_tugas.delete(item)
        self.peta_tugas_row.clear()

        conn = koneksi_database()
        tampilkan_selesai = self.tampilkan_selesai_var.get()
        if tampilkan_selesai:
            rows = conn.execute("""
                SELECT id, nama_tugas, mata_kuliah, deadline, COALESCE(selesai, 0)
                FROM tugas
                WHERE username = ?
                ORDER BY COALESCE(selesai, 0) ASC, deadline ASC
            """, (self.username,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT id, nama_tugas, mata_kuliah, deadline, COALESCE(selesai, 0)
                FROM tugas
                WHERE username = ? AND COALESCE(selesai, 0) = 0
                ORDER BY deadline ASC
            """, (self.username,)).fetchall()

        aktif_rows = conn.execute("""
            SELECT id, nama_tugas, mata_kuliah, deadline
            FROM tugas
            WHERE username = ? AND COALESCE(selesai, 0) = 0
            ORDER BY deadline ASC
        """, (self.username,)).fetchall()
        conn.close()

        sekarang = datetime.now()
        for tid, nama, matkul, deadline_str, selesai in rows:
            tag, status_teks = self.evaluasi_status_tugas(deadline_str, selesai, sekarang)
            ikon_cek = "☑" if selesai else "☐"
            iid = self.tabel_tugas.insert(
                "",
                "end",
                values=(ikon_cek, nama, matkul, deadline_str, status_teks),
                tags=(tag,)
            )
            self.peta_tugas_row[iid] = {
                "id": tid,
                "nama": nama,
                "matkul": matkul,
                "deadline": deadline_str,
                "selesai": selesai
            }

        # Hitung ringkasan aktif
        jml_aktif = len(aktif_rows)
        jml_dekat = 0
        jml_terlambat = 0
        for _, _, _, dl_str in aktif_rows:
            tag, _ = self.evaluasi_status_tugas(dl_str, 0, sekarang)
            if tag == "terlambat":
                jml_terlambat += 1
            elif tag in ("mendesak", "dekat"):
                jml_dekat += 1

        self.label_ringkasan.config(
            text=f"Aktif: {jml_aktif}  |  Mendekati: {jml_dekat}  |  Terlewat: {jml_terlambat}"
        )

        # Update banner peringatan real-time
        if jml_terlambat > 0 or jml_dekat > 0:
            bagian = []
            if jml_terlambat > 0:
                bagian.append(f"⛔ {jml_terlambat} tugas MELEBIHI DEADLINE")
            if jml_dekat > 0:
                bagian.append(f"⚠ {jml_dekat} tugas MENDEKATI DEADLINE (< 24 jam)")
            self.label_banner_notif.config(
                text="PENGINGAT DEADLINE: " + "  •  ".join(bagian) + " — Segera selesaikan atau centang jika sudah selesai!"
            )
            if not self.banner_notif.winfo_ismapped():
                self.banner_notif.pack(fill="x", before=self.banner_notif.master.winfo_children()[2])
        else:
            if self.banner_notif.winfo_ismapped():
                self.banner_notif.pack_forget()

    def tambah_tugas(self):
        nama = self.input_tugas.get().strip()
        matkul = self.pilihan_matkul.get().strip() or "Umum / Lainnya"
        tgl = self.input_tanggal.get().strip()
        jam = self.input_jam.get().strip()

        if not nama:
            messagebox.showwarning("Input Kurang", "Nama tugas tidak boleh kosong!")
            return

        deadline_str = f"{tgl} {jam}"
        try:
            datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showwarning(
                "Format Salah",
                "Format tanggal harus YYYY-MM-DD (contoh 2026-11-28) dan jam HH:MM (contoh 23:59)."
            )
            return

        conn = koneksi_database()
        conn.execute("""
            INSERT INTO tugas (username, nama_tugas, mata_kuliah, deadline, selesai)
            VALUES (?, ?, ?, ?, 0)
        """, (self.username, nama, matkul, deadline_str))
        conn.commit()
        conn.close()

        self.input_tugas.delete(0, tk.END)
        self.tampilkan_tugas()
        self.tampilkan_kalender()
        self.cek_notifikasi(paksa_satu_kali=True)

    def klik_tabel_tugas(self, event):
        region = self.tabel_tugas.identify_region(event.x, event.y)
        col = self.tabel_tugas.identify_column(event.x)
        row_id = self.tabel_tugas.identify_row(event.y)
        if region == "cell" and col == "#1" and row_id:
            self.toggle_selesai_by_iid(row_id)

    def double_klik_tugas(self, event):
        row_id = self.tabel_tugas.identify_row(event.y)
        if row_id:
            self.toggle_selesai_by_iid(row_id)

    def toggle_selesai_by_iid(self, iid):
        info = self.peta_tugas_row.get(iid)
        if not info:
            return
        status_baru = 0 if info["selesai"] else 1
        conn = koneksi_database()
        conn.execute(
            "UPDATE tugas SET selesai = ? WHERE id = ? AND username = ?",
            (status_baru, info["id"], self.username)
        )
        conn.commit()
        conn.close()

        self.tampilkan_tugas()
        self.tampilkan_kalender()

    def selesaikan_tugas_terpilih(self):
        pilihan = self.tabel_tugas.selection()
        if not pilihan:
            messagebox.showinfo("Info", "Pilih tugas pada daftar terlebih dahulu untuk dicentang/diselesaikan.")
            return
        conn = koneksi_database()
        for iid in pilihan:
            info = self.peta_tugas_row.get(iid)
            if info:
                conn.execute(
                    "UPDATE tugas SET selesai = 1 WHERE id = ? AND username = ?",
                    (info["id"], self.username)
                )
        conn.commit()
        conn.close()
        self.tampilkan_tugas()
        self.tampilkan_kalender()

    def hapus_tugas(self):
        pilihan = self.tabel_tugas.selection()
        if not pilihan:
            messagebox.showinfo("Info", "Pilih tugas yang ingin dihapus terlebih dahulu.")
            return
        if not messagebox.askyesno("Konfirmasi Hapus", "Hapus tugas yang dipilih secara permanen?"):
            return
        conn = koneksi_database()
        for iid in pilihan:
            info = self.peta_tugas_row.get(iid)
            if info:
                conn.execute(
                    "DELETE FROM tugas WHERE id = ? AND username = ?",
                    (info["id"], self.username)
                )
        conn.commit()
        conn.close()
        self.tampilkan_tugas()
        self.tampilkan_kalender()

    def cek_notifikasi(self, paksa_satu_kali=False):
        if not self.winfo_exists():
            return

        if self.notifikasi_aktif:
            conn = koneksi_database()
            rows = conn.execute("""
                SELECT id, nama_tugas, mata_kuliah, deadline
                FROM tugas
                WHERE username = ? AND COALESCE(selesai, 0) = 0
                ORDER BY deadline ASC
            """, (self.username,)).fetchall()
            conn.close()

            sekarang = datetime.now()
            pesan_kritis = []

            for tid, nama, matkul, dl_str in rows:
                tag, status_teks = self.evaluasi_status_tugas(dl_str, 0, sekarang)
                kunci = (tid, tag)
                if tag in ("terlambat", "mendesak", "dekat") and kunci not in self.sudah_diberi_notifikasi:
                    self.sudah_diberi_notifikasi.add(kunci)
                    pesan_kritis.append(f"• {nama} ({matkul})\n  {status_teks}")

            if pesan_kritis:
                self.tampilkan_tugas()
                try:
                    self.bell()
                except tk.TclError:
                    pass
                self.tampilkan_toast_notifikasi("\n".join(pesan_kritis[:4]))

        if not paksa_satu_kali:
            self.after_notifikasi = self.after(30000, self.cek_notifikasi)

    def tampilkan_toast_notifikasi(self, isi_pesan):
        if self.toast_aktif is not None and self.toast_aktif.winfo_exists():
            try:
                self.toast_aktif.destroy()
            except tk.TclError:
                pass

        toast = tk.Toplevel(self)
        self.toast_aktif = toast
        toast.title("Notifikasi Deadline CampusLife")
        toast.configure(bg="#FFFBEB")
        toast.resizable(False, False)
        toast.attributes("-topmost", True)

        # Posisikan di kanan bawah layar
        toast.update_idletasks()
        lebar, tinggi = 400, 210
        x = max(20, toast.winfo_screenwidth() - lebar - 30)
        y = max(20, toast.winfo_screenheight() - tinggi - 70)
        toast.geometry(f"{lebar}x{tinggi}+{x}+{y}")

        header = tk.Frame(toast, bg="#D97706", height=36)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="⏰ Pengingat Deadline Tugas",
            bg="#D97706",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=12)

        tk.Label(
            toast,
            text=isi_pesan,
            bg="#FFFBEB",
            fg="#78350F",
            font=("Arial", 9),
            justify="left",
            anchor="nw",
            wraplength=370
        ).pack(fill="both", expand=True, padx=14, pady=10)

        tk.Button(
            toast,
            text="Mengerti",
            command=toast.destroy,
            bg="#D97706",
            fg="white",
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=14,
            pady=4,
            cursor="hand2"
        ).pack(pady=(0, 10))

        # Tutup otomatis setelah 10 detik jika tidak disentuh
        toast.after(10000, lambda: toast.destroy() if toast.winfo_exists() else None)

    def tampilkan_jadwal(self):
        for item in self.tabel_jadwal.get_children():
            self.tabel_jadwal.delete(item)

        urutan_hari = {h: i for i, h in enumerate(DAFTAR_HARI)}
        conn = koneksi_database()
        rows = conn.execute("""
            SELECT id_jadwal, mata_kuliah, sks, kelas, ruangan, hari, jam_mulai, jam_selesai
            FROM jadwal_kuliah
            WHERE username = ?
        """, (self.username,)).fetchall()
        conn.close()

        rows.sort(key=lambda r: (urutan_hari.get(r[5], 99), r[6]))

        daftar_matkul = []
        for id_j, matkul, sks, kelas, ruangan, hari, mulai, selesai in rows:
            self.tabel_jadwal.insert(
                "",
                "end",
                iid=id_j,
                values=(matkul, sks, kelas, ruangan, hari, f"{mulai} - {selesai}")
            )
            if matkul not in daftar_matkul:
                daftar_matkul.append(matkul)

        daftar_matkul.append("Umum / Lainnya")
        self.pilihan_matkul["values"] = daftar_matkul
        if daftar_matkul and not self.pilihan_matkul.get():
            self.pilihan_matkul.set(daftar_matkul[0])

    def pilih_jadwal(self, event=None):
        pilihan = self.tabel_jadwal.selection()
        if not pilihan:
            return
        id_j = pilihan[0]
        self.jadwal_terpilih_id = id_j

        values = self.tabel_jadwal.item(id_j, "values")
        matkul, _, _, ruangan, hari, waktu = values
        mulai, selesai = [bagian.strip() for bagian in waktu.split("-")]

        self.edit_ruangan.delete(0, tk.END)
        self.edit_ruangan.insert(0, ruangan)
        self.edit_hari.set(hari)
        self.edit_mulai.delete(0, tk.END)
        self.edit_mulai.insert(0, mulai)
        self.edit_selesai.delete(0, tk.END)
        self.edit_selesai.insert(0, selesai)

        self.label_pesan_jadwal.config(
            text=f"Mengedit jadwal: {matkul}",
            fg="#0F766E"
        )

    def simpan_perubahan_jadwal(self):
        if not self.jadwal_terpilih_id:
            messagebox.showinfo("Info", "Pilih baris jadwal kuliah yang ingin diubah terlebih dahulu.")
            return

        ruangan = self.edit_ruangan.get().strip()
        hari = self.edit_hari.get().strip()
        mulai = self.edit_mulai.get().strip()
        selesai = self.edit_selesai.get().strip()

        if not ruangan or not hari or not mulai or not selesai:
            messagebox.showwarning("Peringatan", "Semua kolom edit jadwal harus diisi!")
            return

        try:
            t_mulai = datetime.strptime(mulai, "%H:%M")
            t_selesai = datetime.strptime(selesai, "%H:%M")
            if t_selesai <= t_mulai:
                messagebox.showwarning("Waktu Tidak Valid", "Jam selesai harus lebih besar dari jam mulai!")
                return
        except ValueError:
            messagebox.showwarning("Format Jam Salah", "Gunakan format HH:MM (contoh 13:00).")
            return

        conn = koneksi_database()
        conn.execute("""
            UPDATE jadwal_kuliah
            SET ruangan = ?, hari = ?, jam_mulai = ?, jam_selesai = ?
            WHERE id_jadwal = ? AND username = ?
        """, (ruangan, hari, mulai, selesai, self.jadwal_terpilih_id, self.username))
        conn.commit()
        conn.close()

        self.label_pesan_jadwal.config(text="Perubahan jadwal berhasil disimpan!", fg="#15803D")
        self.tampilkan_jadwal()