# surveillance/whatsapp_tracker.py
def track_whatsapp():
    try:
        # Di Termux: baca notifikasi
        import os
        result = os.popen("termux-notification-list | grep 'WhatsApp'").read()
        messages = []
        for line in result.splitlines():
            if "text" in line:
                msg = line.split('"text": "')[1].split('"')[0]
                messages.append(msg)
                if "kata sandi" in msg or "OTP" in msg:
                    print(f"🔐 WhatsApp: Kode OTP diterima")
                if "klik" in msg and "bit.ly" in msg:
                    print(f"🚨 WhatsApp: Phishing terdeteksi!")
        return messages
    except:
        return []