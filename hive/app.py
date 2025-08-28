# hive/app.py
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'super-secret-key')  # Ganti di production

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

# 🔐 Cek login
def require_login(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# 🔐 Cek auth untuk API
def check_auth():
    token = (
        request.args.get('key') or
        (request.json.get('key') if request.is_json else None) or
        (request.json.get('token') if request.is_json else None)
    )
    return token == os.getenv('DASH_KEY', 'watcher123')

# 🔐 Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == os.getenv('DASH_KEY', 'watcher123'):
            session['logged_in'] = True
            return redirect('/')
        else:
            return "❌ Password salah", 403
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

# 🏠 Dashboard
@app.route('/')
@require_login
def dashboard():
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
@require_login
def map():
    return render_template('map.html', sightings=sightings)

# 🚨 Terima alert (POST)
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
@require_login
def api_agents():
    return jsonify(agents)

# 🧠 Kirim perintah ke agent
@app.route('/api/command', methods=['POST'])
@require_login
def api_command():
    data = request.json
    cmd = data.get('command')
    agent_id = data.get('agent_id')
    print(f"⚙️ Perintah ke {agent_id}: {cmd}")
    return jsonify({"status": "command_sent", "agent": agent_id, "command": cmd})

# 🧟 Cari zombie domain
@app.route('/api/zombie/scan', methods=['POST'])
@require_login
def scan_zombie():
    keyword = request.json.get('keyword', 'palestine')
    results = []

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
@require_login
def get_zombie_results():
    return jsonify(zombie_results)

# 📦 Simpan bukti
@app.route('/api/truth', methods=['POST'])
@require_login
def api_truth():
    data = request.json
    data['uploaded'] = datetime.now().isoformat()
    truth_vault.append(data)
    print(f"✅ Bukti disimpan: {data.get('title')}")
    return jsonify({"status": "archived"})

# 📢 Amplify
@app.route('/api/amplify', methods=['POST'])
@require_login
def api_amplify():
    data = request.json
    platform = data.get('platform')
    message = data.get('message')
    print(f"📢 Amplify ke {platform}: {message}")
    return jsonify({"status": "amplified", "to": platform})

# 🕵️‍♂️ Intel Feed
@app.route('/api/intel')
@require_login
def api_intel():
    return jsonify(intel_feed)

# ⚰️ Dead Man's Switch
@app.route('/api/deadman/activate', methods=['POST'])
@require_login
def api_deadman_activate():
    global deadman_active
    deadman_active = True
    print("⚰️ DEAD MAN'S SWITCH DIJALANKAN")
    return jsonify({"status": "activated"})

@app.route('/api/deadman/status')
@require_login
def api_deadman_status():
    return jsonify({"active": deadman_active})

# 📊 Status Global
@app.route('/api/status')
@require_login
def api_status():
    return jsonify({
        "agents_online": len([a for a in agents if a["online"]]),
        "total_alerts": len(alerts),
        "sightings": len(sightings),
        "version": "vΩ",
        "purpose": "Protect the oppressed"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)