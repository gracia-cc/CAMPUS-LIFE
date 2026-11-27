import sqlite3
import tkinter as tk
from tkinter import messagebox,ttk
import os

class NotesPage(tk.Frame):
    def __init__(self, master, username, on_back = None):
        super().__init__(master, bg ="white")
        self.username=username
        self.on_back=on_back
        self.note_id=None
        self.buat_tabel()
        self.buat_tampilan()
        self.tampilkan_catatan()
    def koneksi_database():
        lokasi_db = os.path.join(os.path.dirname(os.path.abspath(__file__)),"database.db"   )
        return sqlite3.connect(lokasi_db)
    def buat_tabel(self):
        conn=self.koneksi_database()
        conn.execute(""" CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL,judul TEXT NOT NULL,isi TEXT NOT NULL) """)
        conn.commit()
        conn.close()
    def buat_tampilan(self):
        header = tk.Frame(self, bg="#365B9D", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Button(
            header,
            text="← Kembali",
            command=self.kembali,
            bg="#263B63",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Arial", 10, "bold"),
            padx=14,
            pady=6,
        ).pack(side="left", padx=20, pady=14)

        tk.Label(
            header,
            text="CampusLife | Notes",
            font=("Arial", 16, "bold"),
            bg="#365B9D",
            fg="white",
        ).pack(side="left")

        area = tk.Frame(self, bg="#F4F6FA")
        area.pack(fill="both", expand=True, padx=20, pady=20)

        daftar_frame = tk.Frame(area, bg="white", padx=12, pady=12)
        daftar_frame.pack(side="left", fill="y", padx=(0, 12))

        tk.Label(
            daftar_frame,
            text="Catatan Saya",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#263B63",
        ).pack(anchor="w", pady=(0, 10))

        self.daftar_catatan = tk.Listbox(
            daftar_frame,
            width=28,
            font=("Arial", 10),
            activestyle="none",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#D9E0EA",
        )
        self.daftar_catatan.pack(fill="y", expand=True)
        self.daftar_catatan.bind(
            "<<ListboxSelect>>",
            self.pilih_catatan,
        )

        editor = tk.Frame(area, bg="white", padx=18, pady=16)
        editor.pack(side="left", fill="both", expand=True)

        tk.Label(
            editor,
            text="Judul catatan",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#263B63",
        ).pack(anchor="w")

        self.input_judul = ttk.Entry(editor, font=("Arial", 11))
        self.input_judul.pack(fill="x", pady=(5, 12))

        tk.Label(
            editor,
            text="Isi catatan",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#263B63",
        ).pack(anchor="w")

        self.input_isi = tk.Text(
            editor,
            wrap="word",
            font=("Arial", 11),
            height=20,
            relief="solid",
            borderwidth=1,
        )
        self.input_isi.pack(fill="both", expand=True, pady=(5, 12))

        tombol = tk.Frame(editor, bg="white")
        tombol.pack(fill="x")

        tk.Button(
            tombol,
            text="+ Catatan Baru",
            command=self.catatan_baru,
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7,
        ).pack(side="left")

        tk.Button(
            tombol,
            text="Simpan",
            command=self.simpan_catatan,
            bg="#16A34A",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=7,
        ).pack(side="left", padx=8)

        tk.Button(
            tombol,
            text="Hapus",
            command=self.hapus_catatan,
            bg="#DC2626",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=7,
        ).pack(side="left")
    def tampilkan_catatan(self):
        self.daftar_catatan.delete(0, tk.END)

        conn = self.koneksi_database()
        rows = conn.execute(
            "SELECT id, judul FROM notes WHERE username = ? ORDER BY id DESC",
            (self.username,),
        ).fetchall()
        conn.close()

        self.catatan_ids = []
        for note_id, judul in rows:
            self.catatan_ids.append(note_id)
            self.daftar_catatan.insert(tk.END, judul)
    def pilih_catatan(self, event=None):
        pilihan = self.daftar_catatan.curselection()
        if not pilihan:
            return

        index = pilihan[0]
        self.note_id = self.catatan_ids[index]

        conn = self.koneksi_database()
        row = conn.execute(
            "SELECT judul, isi FROM notes WHERE id = ? AND username = ?",
            (self.note_id, self.username),
        ).fetchone()
        conn.close()

        if row:
            self.input_judul.delete(0, tk.END)
            self.input_judul.insert(0, row[0])

            self.input_isi.delete("1.0", tk.END)
            self.input_isi.insert("1.0", row[1])
    def catatan_baru(self):
        self.note_id = None
        self.daftar_catatan.selection_clear(0, tk.END)
        self.input_judul.delete(0, tk.END)
        self.input_isi.delete("1.0", tk.END)
        self.input_judul.focus_set()
    def simpan_catatan(self):
        judul = self.input_judul.get().strip()
        isi = self.input_isi.get("1.0", tk.END).strip()

        if not judul:
            messagebox.showwarning(
                "Judul kosong",
                "Isi judul catatan terlebih dahulu.",
                parent=self,
            )
            return

        conn = self.koneksi_database()

        if self.note_id is None:
            cursor = conn.execute(
                "INSERT INTO notes (username, judul, isi) VALUES (?, ?, ?)",
                (self.username, judul, isi),
            )
            self.note_id = cursor.lastrowid
        else:
            conn.execute(
                """
                UPDATE notes
                SET judul = ?, isi = ?
                WHERE id = ? AND username = ?
                """,
                (judul, isi, self.note_id, self.username),
            )

        conn.commit()
        conn.close()

        self.tampilkan_catatan()
        messagebox.showinfo(
            "Berhasil",
            "Catatan berhasil disimpan.",
            parent=self,
        )
    def hapus_catatan(self):
        if self.note_id is None:
            messagebox.showinfo(
                "Pilih catatan",
                "Pilih catatan yang ingin dihapus terlebih dahulu.",
                parent=self,
            )
            return

        if not messagebox.askyesno(
            "Konfirmasi",
            "Hapus catatan ini?",
            parent=self,
        ):
            return

        conn = self.koneksi_database()
        conn.execute(
            "DELETE FROM notes WHERE id = ? AND username = ?",
            (self.note_id, self.username),
        )
        conn.commit()
        conn.close()

        self.catatan_baru()
        self.tampilkan_catatan()
    def kembali(self):
        if self.on_back:
            self.on_back()
        else:
            self.destroy()