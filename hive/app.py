# hive/app.py
from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# 🔹 Data global
alerts = []
sightings = []
agents = [
    {"id": "agent-jkt-01", "ip": "192.168.1.10", "location": "Jakarta", "online": True, "dsi": 92, "role": "scanner"},
    {"id": "agent-gz-01", "ip": "45.123.7.1", "location": "Gaza", "online": True, "dsi": 78, "role": "whistleblower"}
]
truth_vault = []
zombie_results = []
intel_feed = [
    {"type": "phishing", "message": "Deteksi: bit.ly/free-palestine palsu", "time": "14:25"},
    {"type": "disinfo", "message": "Hoax: 'Hamas menyerang warga sipil'", "time": "14:20"}
]
deadman_active = False

# 🔐 Autentikasi
def check_auth():
    token = (
        request.args.get('key') or
        (request.json.get('key') if request.is_json else None) or
        (request.json.get('token') if request.is_json else None)
    )
    return token == os.getenv('DASH_KEY', 'watcher123')

# 🏠 Dashboard
@app.route('/')
def dashboard():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return render_template('dashboard.html',
        alerts=alerts,
        sightings=sightings,
        agents=agents,
        truth_vault=truth_vault,
        zombie_results=zombie_results,
        deadman_active=deadman_active
    )

# 🌍 Peta
@app.route('/map')
def map():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return render_template('map.html', sightings=sightings)

# 🚨 Terima alert (POST) — FIX: Tambahkan GET untuk info
@app.route('/alert', methods=['GET'])
def alert_info():
    return """
    <h1>👁️ /alert Endpoint</h1>
    <p>Gunakan <b>POST</b> untuk kirim data dari agent.</p>
    <pre>
curl -X POST "https://your-sentinel.up.railway.app/alert?key=watcher123" \\
-H "Content-Type: application/json" \\
-d '{"node":"agent-01","alert":"CPU Tinggi","cpu":90,"ram":80}'
    </pre>
    """, 200

@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['time'] = datetime.now().strftime("%H:%M:%S")
    alerts.append(data)
    print(f"🚨 ALERT: {data}")
    return jsonify({"status": "ok"})

# 📍 Sighting
@app.route('/sighting', methods=['POST'])
def receive_sighting():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['time'] = datetime.now().isoformat()
    sightings.append(data)
    print(f"📌 SIGHTING: {data}")
    return jsonify({"status": "recorded"})

# 🤖 Daftar agent
@app.route('/api/agents')
def api_agents():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify(agents)

# 🧠 Kirim perintah ke agent
@app.route('/api/command', methods=['POST'])
def api_command():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    cmd = data.get('command')
    agent_id = data.get('agent_id')
    print(f"⚙️ Perintah ke {agent_id}: {cmd}")
    return jsonify({"status": "command_sent", "agent": agent_id, "command": cmd})

# 🧟 Cari zombie domain
@app.route('/api/zombie/scan', methods=['POST'])
def scan_zombie():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    keyword = request.json.get('keyword', 'palestine')
    results = []

    # Simulasi hasil
    domains = [f"old-{keyword}.com", f"backup-{keyword}.net"]
    for domain in domains:
        results.append({
            "domain": domain,
            "status": "expired",
            "risk": "high",
            "action": "register_or_takeover"
        })

    global zombie_results
    zombie_results = results
    return jsonify(results)

# 🧟 Hasil zombie
@app.route('/api/zombie/results')
def get_zombie_results():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify(zombie_results)

# 📦 Simpan bukti
@app.route('/api/truth', methods=['POST'])
def api_truth():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['uploaded'] = datetime.now().isoformat()
    truth_vault.append(data)
    print(f"✅ Bukti disimpan: {data.get('title')}")
    return jsonify({"status": "archived"})

# 📢 Amplify
@app.route('/api/amplify', methods=['POST'])
def api_amplify():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    platform = data.get('platform')
    message = data.get('message')
    print(f"📢 Amplify ke {platform}: {message}")
    return jsonify({"status": "amplified", "to": platform})

# 🕵️‍♂️ Intel Feed
@app.route('/api/intel')
def api_intel():