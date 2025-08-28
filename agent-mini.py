# agent-mini.py
import time
import requests
import psutil
import os
import subprocess
import socket
from datetime import datetime

# 🔧 KONFIGURASI
HIVE_URL = os.getenv('HIVE_URL', 'https://sentinel-hive.up.railway.app/alert')
DASH_KEY = os.getenv('DASH_KEY', 'watcher123')
AGENT_ID = f"swarm-{os.getenv('RAILWAY_RELEASE_ID', 'local')}-{int(time.time()) % 10000}"
SCAN_INTERVAL = 30
TIMEOUT = 30
MAX_RETRIES = 3

# 🔁 Auto-healing
def self_heal():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    if cpu > 95 or ram > 95:
        print("🔧 Self-healing: Restart agent")
        os.execv(__file__, ['python'] + sys.argv)

# 🌐 Scan jaringan lokal
def scan_network():
    try:
        result = subprocess.run(
            ["nmap", "-sn", "192.168.1.0/24"],
            capture_output=True,
            text=True,
            timeout=30
        )
        hosts = []
        for line in result.stdout.splitlines():
            if "Nmap scan report" in line:
                ip = line.split()[-1]
                if ip != get_local_ip():
                    hosts.append(ip)
        return hosts
    except:
        return []

def get_local_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "127.0.0.1"

# 🔁 Auto-replicate
def deploy_to_target(ip):
    try:
        print(f"🔁 Menyebar ke {ip}")
        # Di dunia nyata: SSH + upload agent-mini.py
        return True
    except:
        return False

# 🤖 AI Sederhana
def detect_anomaly(cpu, ram):
    if cpu > 90:
        return f"🔥 CPU Tinggi: {cpu}%"
    if ram > 85:
        return f"MemoryWarning: {ram}%"
    return None

# 📡 Laporan ke Hive
def report(alert, level="info"):
    data = {
        "node": AGENT_ID,
        "alert": alert,
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "timestamp": datetime.now().isoformat(),
        "platform": "railway"
    }
    for _ in range(MAX_RETRIES):
        try:
            response = requests.post(
                f"{HIVE_URL}?key={DASH_KEY}",
                json=data,
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                print(f"🟢 Laporan dikirim: {alert}")
                return
        except:
            pass
        time.sleep(10)
    print("🔴 Gagal kirim setelah 3 percobaan")

# 🔁 Loop utama
if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        try:
            # Self-heal
            self_heal()

            # Monitor
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent

            # Deteksi anomali
            anomaly = detect_anomaly(cpu, ram)
            if anomaly:
                report(anomaly, "warning")

            # Auto-replicate
            if "192.168" in get_local_ip():
                for host in scan_network():
                    deploy_to_target(host)

            # Laporan rutin
            report(f"📊 CPU={cpu}%, RAM={ram}%")

        except Exception as e:
            print(f"⚠️ Error di loop: {e}")

        time.sleep(SCAN_INTERVAL)