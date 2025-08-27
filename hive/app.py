# hive/app.py
from flask import Flask, render_template, jsonify, request
import os
import subprocess
import sqlite3
from datetime import datetime

# 🔹 Import modul lokal
from database.database import SentinelDB
from ai.local_ai import AnomalyDetector, TextClassifier

app = Flask(__name__)
db = SentinelDB()
ai_detector = AnomalyDetector()
ai_classifier = TextClassifier()

# 🔐 Autentikasi
def check_auth():
    token = request.args.get('key') or (request.json.get('key') if request.is_json else None)
    return token == os.getenv('DASH_KEY', 'watcher123')

# 🏠 Dashboard
@app.route('/')
def dashboard():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    alerts = db.get_alerts(10)
    sightings = db.get_sightings(5)
    zombies = db.get_zombies(5)
    return render_template('dashboard.html', 
        alerts=alerts, 
        sightings=sightings, 
        zombie_results=zombies
    )

# 🌍 Peta
@app.route('/map')
def map():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return render_template('map.html', sightings=db.get_sightings(20))

# 🚨 Terima alert
@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.add_alert(data)
    return jsonify({"status": "ok"})

# 📍 Sighting
@app.route('/sighting', methods=['POST'])
def receive_sighting():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    db.add_sighting(data)
    return jsonify({"status": "recorded"})

# 🧟 Zombie Scan
@app.route('/api/zombie/scan', methods=['POST'])
def scan_zombie():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    keyword = request.json.get('keyword', 'palestine')
    results = []

    domains = [f"{keyword}.com", f"old-{keyword}.net", f"backup-{keyword}.org"]
    for domain in domains:
        try:
            result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=5)
            if "No match" in result.stdout or "NOT FOUND" in result.stdout:
                result_data = {
                    "domain": domain,
                    "status": "expired",
                    "risk": "high",
                    "action": "register_or_takeover",
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result_data)
                db.add_zombie(result_data)
        except:
            pass

    return jsonify(results)

# 🧟 Hasil zombie
@app.route('/api/zombie/results')
def get_zombie_results():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify(db.get_zombies(50))

# 📊 Status
@app.route('/api/status')
def api_status():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify({
        "total_alerts": len(db.get_alerts(1000)),
        "total_sightings": len(db.get_sightings(1000)),
        "total_zombies": len(db.get_zombies(1000)),
        "version": "vΩ",
        "ai_status": "active"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)