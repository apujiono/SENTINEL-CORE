# surveillance/cctv_tracker.py
import requests

def find_public_cctv(city="Jakarta"):
    feeds = {
        "Jakarta": "http://cctv.jakarta.go.id/feed1.m3u8",
        "Bandung": "http://cctv.bandungkota.go.id/live"
    }
    return feeds.get(city, None)

def check_cctv(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False