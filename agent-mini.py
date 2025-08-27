# agent-mini.py
import time
import requests
import psutil
from datetime import datetime
import os
from ai.local_ai import AnomalyDetector, TextClassifier

# 🔧 Konfigurasi
HIVE_URL = "https://sentinel-core-production.up.railway.app/alert"  # GANTI DENGAN HIVE-MU
AGENT_ID = f"railway-agent-{os.getenv('RAILWAY_RELEASE_ID', 'local')}"
SCAN_INTERVAL = 10

# 🔍 AI lokal
ai_detector = AnomalyDetector()
ai_classifier = TextClassifier()

def report(alert, level="info"):
    try:
        data = {
            "node": AGENT_ID,
            "alert": alert,
            "level": level,
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "timestamp": datetime.now().isoformat()
        }
        response = requests.post(HIVE_URL, json=data, timeout=10)
        if response.status_code == 200:
            print(f"🟢 Laporan dikirim: {alert}")
        else:
            print(f"🟡 Gagal kirim: {response.status_code}")
    except Exception as e:
        print(f"🔴 Error: {e}")

if __name__ == "__main__":
    print(f"🤖 Agent aktif: {AGENT_ID}")
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent

            # 🧠 AI: Deteksi anomali
            anomaly = ai_detector.detect(cpu, ram)
            if anomaly:
                report(anomaly, "critical")

            # 📢 Laporan rutin
            report(f"📊 CPU={cpu}%, RAM={ram}%")

        except Exception as e:
            print(f"⚠️ Error: {e}")

        time.sleep(SCAN_INTERVAL)