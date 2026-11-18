import sqlite3

conn = sqlite3.connect("campuslife.db")
cursor = conn.cursor()

cursor.execute("SELECT id, username FROM users")

akun = cursor.fetchall()

print("\n===== DAFTAR AKUN CAMPUSLIFE =====")

if len(akun) > 0:
    for data in akun:
        print(f"ID       : {data[0]}")
        print(f"Username : {data[1]}")
        print("---------------------------")
else:
    print("Belum ada akun yang terdaftar.")

conn.close()
