# hive/app.py
from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)
alerts = []

@app.route('/')
def dashboard():
    token = request.args.get('key')
    if token != os.getenv('DASH_KEY', 'watcher123'):
        return "🔐 Akses Ditolak", 403
    return render_template('dashboard.html', alerts=alerts)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    data['time'] = datetime.now().strftime("%H:%M:%S")
    alerts.append(data)
    print(f"🚨 ALERT: {data}")
    return jsonify({"status": "ok"})

@app.route('/api/alerts')
def api_alerts():
    return jsonify(alerts[-20:])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)