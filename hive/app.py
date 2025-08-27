# hive/app.py
from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# 🔹 Inisialisasi semua variabel global
alerts = []
sightings = []
truth_vault = []
agents = set()

@app.route('/')
def dashboard():
    token = request.args.get('key')
    if token != os.getenv('DASH_KEY', 'watcher123'):
        return "🔐 Akses Ditolak", 403
    return render_template(
        'dashboard.html',
        alerts=alerts,
        sightings=sightings,
        truth_vault=truth_vault,
        agent_count=len(agents)
    )

@app.route('/map')
def map():
    token = request.args.get('key')
    if token != os.getenv('DASH_KEY', 'watcher123'):
        return "🔐 Akses Ditolak", 403
    return render_template('map.html', sightings=sightings)

@app.route('/alert', methods=['POST'])
def receive_alert():
    data = request.json
    data['time'] = datetime.now().strftime("%H:%M:%S")
    alerts.append(data)
    agents.add(data.get('node', 'unknown'))
    print(f"🚨 ALERT: {data}")
    return jsonify({"status": "ok"})

@app.route('/sighting', methods=['POST'])
def receive_sighting():
    data = request.json
    data['time'] = datetime.now().isoformat()
    sightings.append(data)
    print(f"📌 SIGHTING: {data}")
    return jsonify({"status": "recorded"})

@app.route('/truth', methods=['POST'])
def add_truth():
    data = request.json
    data['uploaded'] = datetime.now().isoformat()
    truth_vault.append(data)
    print(f"✅ TRUTH: {data['title']} disimpan")
    return jsonify({"status": "archived"})

@app.route('/api/status')
def api_status():
    return jsonify({
        "agents": len(agents),
        "alerts": len(alerts),
        "sightings": len(sightings),
        "truth_count": len(truth_vault),
        "version": "vΩ",
        "purpose": "Protect the oppressed"
    })

@app.route('/api/alerts')
def api_alerts():
    return jsonify(alerts[-20:])

@app.route('/api/sightings')
def api_sightings():
    return jsonify(sightings[-10:])

@app.route('/api/truth')
def api_truth():
    return jsonify(truth_vault[-10:])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)