# agent/core/sentinel.py
import time
import psutil
from datetime import datetime
from modules.monitor import SystemMonitor
from modules.firewall import Firewall
from utils.logger import log
from core.ethics import EthicsEngine
from ai.predictive import ThreatPredictor
from ghost.counter_strike import CounterStrike

class Sentinel:
    def __init__(self):
        self.id = f"sentinel-{hash(datetime.now()) % 10000}"
        self.monitor = SystemMonitor()
        self.firewall = Firewall()
        self.ethics = EthicsEngine()
        self.predictor = ThreatPredictor()
        log(f"🛡️  The Watcher Agent aktif: {self.id}")

    def scan(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        threats = self.monitor.get_threats()

        prediction = self.predictor.predict(cpu, ram, threats)
        if prediction:
            if self.ethics.is_allowed("alert"):
                log(f"🚨 {prediction}")
                if "critical" in prediction and self.ethics.is_allowed("retaliate"):
                    cs = CounterStrike("85.23.12.9")
                    cs.execute()

    def run(self):
        while True:
            self.scan()
            time.sleep(5)