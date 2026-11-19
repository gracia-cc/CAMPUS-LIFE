
import vlc
import os

print("1. Mengecek library VLC...")

try:
    instance = vlc.Instance()
    
    if instance is None:
        print("VLC gagal dijalankan!")
    else:
        print("VLC berhasil dijalankan!")

        player = instance.media_player_new()
        print("Media Player berhasil dibuat!")

        player.release()
        instance.release()

except Exception as e:
    print("Terjadi kesalahan:", repr(e))
