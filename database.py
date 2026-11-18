import sqlite3

def koneksi_database():
    koneksi = sqlite3.connect("database.db")
    return koneksi

def buat_tabel():
    koneksi = koneksi_database()
    cursor = koneksi.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)""")

    koneksi.commit()
    koneksi.close()

def daftar_akun(username, password):
    koneksi = koneksi_database()
    cursor = koneksi.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    data = cursor.fetchone()

    if data:
        koneksi.close()
        return False
    
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",(username, password))
    koneksi.commit()
    koneksi.close()
    return True

def login_akun(username, password):
    koneksi = koneksi_database()
    cursor = koneksi.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username, password))
    data = cursor.fetchone()
    koneksi.close()

    if data:
        return True
    else:
        return False
