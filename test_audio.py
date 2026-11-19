
import vlc
import os
import time

lokasi = os.path.dirname(os.path.abspath(__file__))
file_musik = os.path.join(lokasi, "assets", "music.mp3")

print("1. Memeriksa file musik...")

if not os.path.exists(file_musik):
    print("File musik tidak ditemukan!")
    raise SystemExit

print("File musik ditemukan!")

print("2. Menyiapkan VLC...")

instance = vlc.Instance("--no-video")
player = instance.media_player_new()

media = instance.media_new(file_musik)
player.set_media(media)

print("3. Memulai musik...")
player.audio_set_volume(50)

hasil = player.play()
print("Hasil play:", hasil)

time.sleep(3)

print("Status pemutar:", player.get_state())

input("Tekan Enter untuk menghentikan musik...")

player.stop()
player.release()
instance.release()

print("Tes selesai!")
