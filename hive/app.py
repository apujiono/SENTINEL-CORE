# hive/app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
import os

# Coba import CyberWarEngine
try:
    from retaliation.cyberwar_engine import CyberWarEngine
    RETALIATION_ENABLED = True
    print("✅ CyberWar Engine dimuat")
except Exception as e:
    print(f"⚠️  CyberWar Engine tidak bisa dimuat: {e}")
    RETALIATION_ENABLED = False

app = Flask(__name__)

def check_auth():
    token = request.args.get('key') or (request.json.get('key') if request.is_json else None)
    return token == os.getenv('DASH_KEY', 'watcher123')

@app.route('/')
def dashboard():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "online",
        "version": "vΩ",
        "retaliation": RETALIATION_ENABLED,
        "agents": 1
    })

@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    print(f"🚨 ALERT: {data}")
    return jsonify({"status": "ok"})

@app.route('/api/retaliate', methods=['POST'])
def api_retaliate():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    
    attacker_ip = request.json.get('ip')
    if not attacker_ip:
        return jsonify({"status": "error", "msg": "IP tidak diberikan"})
    
    if not RETALIATION_ENABLED:
        return jsonify({"status": "error", "msg": "Retaliation module tidak tersedia"})
    
    try:
        engine = CyberWarEngine(attacker_ip)
        engine.execute()
        return jsonify({"status": "cyber_war_launched", "target": attacker_ip})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)