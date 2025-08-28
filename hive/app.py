# hive/app.py
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
from datetime import datetime
import json

# Import Zombie Hunter
try:
    from tools.zombie_scanner import scan_zombie_domains
    ZOMBIE_ENABLED = True
except:
    ZOMBIE_ENABLED = False

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'super-secret-key')

# 🔹 Data global
alerts = []
agents = []  # Daftar agent aktif
zombie_results = []
commands = []  # Perintah untuk agent
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

# 🏠 Dashboard
@app.route('/')
@require_login
def dashboard():
    return render_template('dashboard.html',
        alerts=alerts,
        agents=agents,
        zombie_results=zombie_results,
        deadman_active=deadman_active
    )

# 🚨 Terima alert
@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['time'] = datetime.now().strftime("%H:%M:%S")
    alerts.append(data)
    return jsonify({"status": "ok"})

# 🤖 Terima pendaftaran agent
@app.route('/agent', methods=['POST'])
def register_agent():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['last_seen'] = datetime.now().isoformat()
    # Update jika sudah ada, tambah jika baru
    existing = next((a for a in agents if a['id'] == data['id']), None)
    if existing:
        existing.update(data)
    else:
        agents.append(data)
    return jsonify({"status": "registered"})

# 🧟 Zombie Hunter
@app.route('/api/zombie/scan', methods=['POST'])
@require_login
def api_scan_zombie():
    keyword = request.json.get('keyword', 'palestine')
    results = scan_zombie_domains(keyword)
    global zombie_results
    zombie_results = results
    return jsonify(results)

@app.route('/api/zombie/results')
@require_login
def api_zombie_results():
    return jsonify(zombie_results)

# 🤖 Kirim perintah ke agent
@app.route('/api/command', methods=['POST'])
@require_login
def api_command():
    data = request.json
    cmd = data.get('command')
    agent_id = data.get('agent_id')
    
    # Simpan perintah untuk agent
    commands.append({
        "agent_id": agent_id,
        "command": cmd,
        "status": "pending",
        "timestamp": datetime.now().isoformat()
    })
    
    print(f"⚙️ Perintah ke {agent_id}: {cmd}")
    return jsonify({"status": "command_sent", "agent": agent_id, "command": cmd})

# 🤖 Cek perintah untuk agent
@app.route('/agent/commands', methods=['GET'])
def get_agent_commands():
    agent_id = request.args.get('id')
    if not agent_id:
        return jsonify([])
    
    # Ambil perintah yang pending untuk agent ini
    pending = [c for c in commands if c['agent_id'] == agent_id and c['status'] == 'pending']
    
    # Tandai sebagai dikirim
    for cmd in pending:
        cmd['status'] = 'sent'
    
    return jsonify(pending)

# 🚪 Login
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)