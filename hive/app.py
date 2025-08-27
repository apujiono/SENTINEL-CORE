# hive/app.py
from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# 🔹 DATA SIMULASI (di dunia nyata: ganti dengan database)
alerts = []
sightings = []
agents = [
    {"id": "agent-jkt-01", "ip": "192.168.1.10", "location": "Jakarta", "online": True, "dsi": 92, "role": "scanner", "last_seen": "2025-08-27T14:30:00"},
    {"id": "agent-gz-01", "ip": "45.123.7.1", "location": "Gaza", "online": True, "dsi": 78, "role": "whistleblower", "last_seen": "2025-08-27T14:28:00"}
]
truth_vault = []
zombie_domains = []
intel_feed = [
    {"type": "phishing", "message": "Deteksi: bit.ly/free-palestine palsu", "time": "14:25"},
    {"type": "disinfo", "message": "Hoax: 'Hamas menyerang warga sipil'", "time": "14:20"}
]
deadman_active = False
amplify_history = []

# 🔐 Cek token akses
def check_auth():
    token = request.args.get('key') or request.json.get('key')
    return token == os.getenv('DASH_KEY', 'watcher123')

# 🏠 Dashboard Utama
@app.route('/')
def dashboard():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return render_template('dashboard.html',
        alerts=alerts,
        sightings=sightings,
        agents=agents,
        truth_vault=truth_vault,
        zombie_domains=zombie_domains,
        deadman_active=deadman_active
    )

# 🌍 Peta Ancaman
@app.route('/map')
def map():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return render_template('map.html', sightings=sightings)

# 🚨 Terima alert dari agent
@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['time'] = datetime.now().strftime("%H:%M:%S")
    alerts.append(data)
    print(f"🚨 ALERT: {data}")
    return jsonify({"status": "ok"})

# 📍 Tambah sighting (pantau orang/CCTV)
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
    # Di dunia nyata: kirim via MQTT atau encrypted channel
    return jsonify({"status": "command_sent", "agent": agent_id, "command": cmd})

# 🧟 Cari zombie domain
@app.route('/api/zombie')
def api_zombie():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    keyword = request.args.get('keyword', 'palestine')
    results = [
        {"domain": f"old-{keyword}.com", "type": "expired", "url": f"http://old-{keyword}.com", "risk": "high"},
        {"domain": f"backup-{keyword}.net", "type": "subdomain-takeover", "url": f"http://backup-{keyword}.net", "risk": "critical"},
        {"domain": f"legacy-{keyword}.org", "type": "cms-vuln", "url": f"http://legacy-{keyword}.org", "risk": "medium"}
    ]
    zombie_domains.extend(results)
    return jsonify(results)

# 🧟 Ambil alih zombie domain
@app.route('/api/takeover', methods=['POST'])
def api_takeover():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    domain = request.json.get('domain')
    result = {
        "domain": domain,
        "status": "taken_over",
        "node": "agent-jkt-01",
        "time": datetime.now().isoformat(),
        "purpose": "relay_node"
    }
    print(f"🧟 Ambil alih: {domain}")
    return jsonify(result)

# 📦 Simpan bukti di Truth Vault
@app.route('/api/truth', methods=['POST'])
def api_truth():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['uploaded'] = datetime.now().isoformat()
    truth_vault.append(data)
    print(f"✅ Bukti disimpan: {data.get('title')}")
    return jsonify({"status": "archived", "hash": f"truth-{len(truth_vault)}"})

# 📢 Amplify ke platform
@app.route('/api/amplify', methods=['POST'])
def api_amplify():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    platform = data.get('platform')
    message = data.get('message')
    record = {
        "message": message,
        "platform": platform,
        "time": datetime.now().isoformat(),
        "status": "sent"
    }
    amplify_history.append(record)
    print(f"📢 Amplify ke {platform}: {message}")
    return jsonify({"status": "amplified", "to": platform})

# 🕵️‍♂️ Intel Feed (disinfo, phishing, dll)
@app.route('/api/intel')
def api_intel():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify(intel_feed)

# ⚰️ Dead Man's Switch
@app.route('/api/deadman/activate', methods=['POST'])
def api_deadman_activate():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    global deadman_active
    deadman_active = True
    print("⚰️ DEAD MAN'S SWITCH DIJALANKAN")
    # Di dunia nyata: sebar semua bukti ke IPFS, Telegram, dll
    return jsonify({"status": "activated", "message": "Jika tidak aktif 24 jam, semua bukti akan bocor"})

@app.route('/api/deadman/status')
def api_deadman_status():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify({"active": deadman_active})

# 📊 Status Global
@app.route('/api/status')
def api_status():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify({
        "agents_online": len([a for a in agents if a["online"]]),
        "total_alerts": len(alerts),
        "sightings": len(sightings),
        "truth_count": len(truth_vault),
        "zombie_hunted": len(zombie_domains),
        "version": "vΩ",
        "purpose": "Protect the oppressed"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)