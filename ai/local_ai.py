# ai/local_ai.py
import numpy as np
from collections import deque

class AnomalyDetector:
    def __init__(self, window_size=10):
        self.cpu_window = deque(maxlen=window_size)
        self.ram_window = deque(maxlen=window_size)

    def detect(self, cpu, ram):
        self.cpu_window.append(cpu)
        self.ram_window.append(ram)

        if len(self.cpu_window) == self.cpu_window.maxlen:
            cpu_mean = np.mean(self.cpu_window)
            cpu_std = np.std(self.cpu_window)
            if cpu > cpu_mean + 2 * cpu_std:
                return f"🚨 Anomali CPU: {cpu}% (normal ~{cpu_mean:.1f}%)"
        return None

class TextClassifier:
    def __init__(self):
        self.phishing_words = ["klik", "verifikasi", "segera", "pemenang", "hadiah", "otp", "akun", "login"]
        self.disinfo_patterns = ["human shields", "fake news", "hoax", "no casualties", "justified response"]

    def classify(self, text):
        text = text.lower()
        if any(w in text for w in self.phishing_words):
            return "phishing"
        if any(p in text for p in self.disinfo_patterns):
            return "disinfo"
        return "normal"