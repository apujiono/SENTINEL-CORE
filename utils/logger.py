# utils/logger.py
import datetime

def log(msg):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {msg}")