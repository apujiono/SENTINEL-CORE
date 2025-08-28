# hive/app.py
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
from datetime import datetime

# Import lokal (opsional)
try:
    from ai.sentinel_ai import ThreatAI
    from tools.zombie_scanner import scan_zombie_domains
    AI_ENABLED = True
    ai = ThreatAI()
except:
    AI_ENABLED = False

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'super-secret-key')

# 🔹 Data global
alerts = []
sightings = []
agents = []
zombie_results = []
intel_feed = [
    {"type": "phishing", "message": "bit.ly/free-palestine palsu", "time": "14:25"},
    {"type": "disinfo", "message": "Hoax: 'Hamas menyerang warga sipil'", "time": "14:20"}
]
deadman_active = False

# 🔐 Login
def require_login(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def check_auth():
    token = request.args.get('key') or (request.json.get('key') if request.is_json else None)
    return token == os.getenv('DASH_KEY', 'watcher123')

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

@app.route('/')
@require_login
def dashboard():
    return render_template('dashboard.html',
        alerts=alerts,
        sightings=sightings,
        agents=agents,
        zombie_results=zombie_results,
        intel_feed=intel_feed,
        deadman_active=deadman_active
    )

@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['time'] = datetime.now().strftime("%H:%M:%S")
    alerts.append(data)
    return jsonify({"status": "ok"})

@app.route('/agent', methods=['POST'])
def register_agent():
    data = request.json
    data['last_seen'] = datetime.now().isoformat()
    existing = next((a for a in agents if a['id'] == data['id']), None)
    if existing:
        existing.update(data)
    else:
        agents.append(data)
    return jsonify({"status": "registered"})

@app.route('/api/agents')
@require_login
def api_agents():
    return jsonify(agents)

@app.route('/api/zombie/scan', methods=['POST'])
@require_login
def api_scan_zombie():
    keyword = request.json.get('keyword', 'palestine')
    results = scan_zombie_domains(keyword)
    global zombie_results
    zombie_results = results
    return jsonify(results)

@app.route('/api/deadman/activate', methods=['POST'])
@require_login
def api_deadman_activate():
    global deadman_active
    deadman_active = True
    return jsonify({"status": "activated"})

@app.route('/api/deadman/status')
@require_login
def api_deadman_status():
    return jsonify({"active": deadman_active})

@app.route('/api/status')
@require_login
def api_status():
    return jsonify({
        "agents": len(agents),
        "alerts": len(alerts),
        "version": "vΩ"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)