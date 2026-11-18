import sqlite3
import hashlib
import os
def koneksi_database():
    return sqlite3.connect("campuslife.db")

def buat_tabel():
    conn = koneksi_database()
    cursor = conn.cursor()
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL,salt TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256",password.encode(), salt.encode(), 10000).hex()

def daftar_akun(username, password):
    conn = koneksi_database()
    cursor = conn.cursor()
    salt=os.urandom(16).hex()
    password_hash = hash_password(password, salt)
    try:
        cursor.execute("INSERT INTO users(username, password, salt) VALUES (?,?,?)",(username, password_hash, salt))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
     conn.close()
def login_akun(username, password):
    conn = koneksi_database()
    cursor = conn.cursor()
    cursor.execute("select password, salt from users where username =?",(username,))
    data=cursor.close()
    conn.close()

    if data:
        password_hash, salt = data
        password_input = hash_password(password, salt)
        if password_input==password_hash:
           return True
    else:
        return False