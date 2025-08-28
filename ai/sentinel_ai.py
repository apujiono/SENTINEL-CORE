# ai/sentinel_ai.py
import numpy as np
from collections import deque

class ThreatAI:
    def __init__(self):
        self.cpu_history = deque(maxlen=10)
        self.ram_history = deque(maxlen=10)

    def detect_anomaly(self, cpu, ram):
        self.cpu_history.append(cpu)
        self.ram_history.append(ram)

        if len(self.cpu_history) == 10:
            cpu_mean = np.mean(self.cpu_history)
            cpu_std = np.std(self.cpu_history)
            if cpu > cpu_mean + 2 * cpu_std:
                return f"🚨 Anomali CPU: {cpu}% (normal ~{cpu_mean:.1f}%)"
        return None

    def classify_threat(self, message):
        message = message.lower()
        if any(w in message for w in ["klik", "verifikasi", "otp", "hadiah"]):
            return "phishing"
        if any(p in message for p in ["human shields", "fake news", "hoax"]):
            return "disinfo"
        return "normal"

    def predict_attack(self, recent_alerts):
        brute_count = sum(1 for a in recent_alerts if "brute" in a.get('alert', '').lower())
        if brute_count > 3:
            return "Potensi serangan DDoS dalam 1 jam"
        return Non