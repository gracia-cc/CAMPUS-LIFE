import os

print("1. Mengecek library VLC...")
folder_vlc = r"C:\Program Files\VideoLAN\VLC"

try:
     if not os.path.isfile(os.path.join(folder_vlc, "libvlc.dll")):
        raise FileNotFoundError(
            f"libvlc.dll tidak ditemukan di: {folder_vlc}")
    dll_directory = os.add_dll_directory(folder_vlc)
    os.environ["VLC_PLUGIN_PATH"] = os.path.join(folder_vlc, "plugins")

    import vlc
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