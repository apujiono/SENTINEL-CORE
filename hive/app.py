# hive/app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
import os
import subprocess
from datetime import datetime

# Import lokal
try:
    from database.database import SentinelDB
    from retaliation.cyberwar_engine import CyberWarEngine
    from ai.war_planner import CyberWarPlanner
except Exception as e:
    print(f"❌ Import gagal: {e}")

app = Flask(__name__)
db = SentinelDB()

def check_auth():
    token = request.args.get('key') or (request.json.get('key') if request.is_json else None)
    return token == os.getenv('DASH_KEY', 'watcher123')

@app.route('/')
def dashboard():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return render_template('dashboard.html',
        alerts=db.get_alerts(10),
        sightings=db.get_sightings(5),
        zombies=db.get_zombies(5)
    )

@app.route('/alert', methods=['POST'])
def receive_alert():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.add_alert(data)
    return jsonify({"status": "ok"})

@app.route('/sighting', methods=['POST'])
def receive_sighting():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    db.add_sighting(data)
    return jsonify({"status": "recorded"})

@app.route('/api/zombie/scan', methods=['POST'])
def scan_zombie():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    keyword = request.json.get('keyword', 'palestine')
    results = []
    domains = [f"{keyword}.com", f"old-{keyword}.net"]
    for domain in domains:
        try:
            result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=5)
            if "No match" in result.stdout:
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

@app.route('/api/zombie/results')
def get_zombie_results():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify(db.get_zombies(50))

@app.route('/api/retaliate', methods=['POST'])
def api_retaliate():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    attacker_ip = request.json.get('ip')
    if not attacker_ip:
        return jsonify({"status": "error", "msg": "IP tidak diberikan"})
    try:
        engine = CyberWarEngine(attacker_ip)
        engine.execute()
        return jsonify({"status": "cyber_war_launched", "target": attacker_ip})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

@app.route('/api/status')
def api_status():
    if not check_auth():
        return "🔐 Akses Ditolak", 403
    return jsonify({
        "total_alerts": len(db.get_alerts(1000)),
        "version": "vΩ",
        "ai_status": "active"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)