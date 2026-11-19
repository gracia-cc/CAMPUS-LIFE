from plyer import notification

def tampilkan_notifikasi(judul, pesan):
    try:
        notification.notify(
            title=judul,
            message=pesan,
            app_name="Campus Life",
            timeout=10
        )
    except Exception as error:
        print("Notifikasi gagal:", error)