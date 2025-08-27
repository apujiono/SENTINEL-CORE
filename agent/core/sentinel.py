# agent/core/sentinel.py
import time
import psutil
from datetime import datetime
import requests
import os

# Import lokal
from modules.monitor import SystemMonitor
from modules.firewall import Firewall
from modules.tachikoma import Tachikoma
from utils.logger import log
from core.ethics import EthicsEngine

class Sentinel:
    def __init__(self, config_path="config/config.json"):
        self.config = self.load_config(config_path)
        self.id = self.config["node_id"]
        self.role = self.config["role"]
        self.hive_url = self.config["hive_url"]
        self.monitor = SystemMonitor()
        self.firewall = Firewall()
        self.tachikoma = Tachikoma()
        self.ethics = EthicsEngine()
        self.dsi = 100  # Digital Sanity Index

    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                import json
                return json.load(f)
        except:
            return {
                "node_id": "sentinel-anon",
                "role": "scanner",
                "hive_url": "https://your-hive.up.railway.app/alert",
                "scan_interval": 5
            }

    def update_dsi(self, cpu, ram, threats):
        self.dsi = 100
        self.dsi -= cpu / 2
        self.dsi -= ram / 2
        self.dsi -= len(threats) * 10
        self.dsi = max(0, self.dsi)

    def report(self, alert, level="warning"):
        data = {
            "node": self.id,
            "alert": alert,
            "level": level,
            "dsi": self.dsi,
            "time": datetime.now().isoformat()
        }
        try:
            requests.post(self.hive_url, json=data, timeout=3)
            log(f"🟢 Laporan dikirim: {alert}")
        except Exception as e:
            log(f"🔴 Gagal kirim ke hive: {e}")

    def scan(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        procs = self.monitor.get_suspicious_processes()
        conns = self.monitor.get_suspicious_connections()
        threats = procs + conns

        self.update_dsi(cpu, ram, threats)

        if cpu > 90:
            alert = f"🔥 CPU Tinggi: {cpu}%"
            self.report(alert, "critical")
            if self.dsi < 30 and self.ethics.is_allowed("retaliate"):
                self.tachikoma.speak("Musuh mendekat. Waktunya balas!")
                # Di sini bisa panggil counter_strike

        for threat in threats:
            self.report(threat, "warning")

    def run(self):
        log(f"🛡️  The Watcher Agent aktif: {self.id} | Role: {self.role}")
        while True:
            self.scan()
            time.sleep(self.config["scan_interval"])