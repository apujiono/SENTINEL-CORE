# agent/modules/monitor.py
import psutil

class SystemMonitor:
    SUSPICIOUS_NAMES = ["keylog", "miner", "virus", "hack", "rat", "trojan"]
    SUSPICIOUS_IPS = ["185", "45", "103", "91", "194"]

    def get_suspicious_processes(self):
        suspicious = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name'].lower()
                if any(s in name for s in self.SUSPICIOUS_NAMES):
                    suspicious.append(f"💀 {name} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return suspicious

    def get_suspicious_connections(self):
        suspicious = []
        for conn in psutil.net_connections():
            if conn.raddr and conn.raddr.ip:
                ip = conn.raddr.ip
                if any(ip.startswith(p) for p in self.SUSPICIOUS_IPS):
                    suspicious.append(f"🌐 Suspicious IP: {ip}:{conn.raddr.port}")
        return suspicious