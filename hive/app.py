# hive/app.py
from flask import Flask, render_template, jsonify, request
import os
import subprocess
import re
import json
from datetime import datetime, timedelta

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
    {"type": "phishing", "message": "bit.ly/free-palestine palsu", "time": "14:25"},
    {"type": "disinfo", "message": "Hoax: 'Hamas menyerang warga sipil'", "time": "14:20"}
]
deadman_active = False

# 🔐 Autentikasi
def check_auth():
    token = request.args.get('key') or (request.json.get('key') if request.is_json else None)
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

# 🚨 Terima alert
@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['time'] = datetime.now().strftime("%H:%M:%S")
    alerts.append(data)
    return jsonify({"status": "ok"})

# 📍 Sighting
@app.route('/sighting', methods=['POST'])
def receive_sighting():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['time'] = datetime.now().isoformat()
    sightings.append(data)
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
    print(f"⚙️ Perintah ke {data['agent_id']}: {data['command']}")
    return jsonify({"status": "command_sent"})

# 🧟 Cari zombie domain
@app.route('/api/zombie/scan', methods=['POST'])
def scan_zombie():
    if not check_auth():
        return "🔐 Akses Ditolak", 403

    keyword = request.json.get('keyword', 'palestine')
    results = []

    # Generate domain
    domains = generate_domains(keyword)
    for domain in domains:
        try:
            if is_domain_expired(domain):
                results.append({
                    "domain": domain,
                    "status": "expired",
                    "risk": "high",
                    "action": "register_or_takeover"
                })
            else:
                subdomains = [f"www.{domain}", f"admin.{domain}", f"blog.{domain}"]
                for sub in subdomains:
                    if check_subdomain_takeover(sub):
                        results.append({
                            "domain": sub,
                            "status": "subdomain-takeover",
                            "risk": "critical",
                            "action": "claim"
                        })
        except:
            pass

    global zombie_results
    zombie_results = results
    return jsonify(results)

# 🧟 Hasil zombie
@app.route('/api/zombie/results')
def get_zombie_results():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify(zombie_results)

# 🧟 Ambil alih zombie
@app.route('/api/zombie/takeover', methods=['POST'])
def takeover_zombie():
    if not check_auth():
        return "🔐 Akses Ditolak", 403

    domain = request.json.get('domain')
    action = request.json.get('action')

    if "subdomain-takeover" in action:
        return jsonify({
            "status": "claimed",
            "domain": domain,
            "message": "✅ Subdomain berhasil diambil alih. Agent mini dikirim."
        })

    elif "expired" in action:
        return jsonify({
            "status": "register_suggested",
            "domain": domain,
            "message": "⚠️ Domain expired. Daftar sekarang untuk jadikan agent."
        })

    return jsonify({"status": "unknown"})

# 📦 Simpan bukti
@app.route('/api/truth', methods=['POST'])
def api_truth():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['uploaded'] = datetime.now().isoformat()
    truth_vault.append(data)
    return jsonify({"status": "archived"})

# 📢 Amplify
@app.route('/api/amplify', methods=['POST'])
def api_amplify():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    print(f"📢 Amplify: {data['message']} ke {data['platform']}")
    return jsonify({"status": "amplified"})

# 🕵️‍♂️ Intel feed
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
    return jsonify({"status": "activated"})

@app.route('/api/deadman/status')
def api_deadman_status():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify({"active": deadman_active})

# 📊 Status
@app.route('/api/status')
def api_status():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify({
        "agents_online": len([a for a in agents if a["online"]]),
        "total_alerts": len(alerts),
        "version": "vΩ"
    })

# 🔍 Fungsi pendukung
def generate_domains(keyword):
    tlds = ["com", "net", "org", "info", "biz"]
    prefixes = ["", "www.", "old-", "backup-", "legacy-", "demo-", "free-"]
    domains = []
    for p in prefixes:
        for t in tlds:
            domains.append(f"{p}{keyword}.{t}")
    return domains[:50]

def is_domain_expired(domain):
    try:
        result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=5)
        if "No match" in result.stdout or "NOT FOUND" in result.stdout or "Expired" in result.stdout:
            return True
        return False
    except:
        return True

def check_subdomain_takeover(subdomain):
    try:
        r = requests.get(f"http://{subdomain}", timeout=3)
        server = r.headers.get('Server', '').lower()
        if any(s in server for s in ['heroku', 'github', 'aws', 'azure', 'netlify']):
            return True
    except:
        try:
            result = subprocess.run(["nslookup", subdomain], capture_output=True, text=True)
            if any(cloud in result.stdout.lower() for cloud in ['heroku', 'github', 's3']):
                return True
        except:
            pass
    return False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)