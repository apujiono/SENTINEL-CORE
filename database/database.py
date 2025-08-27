# database/database.py
import sqlite3
import json
from datetime import datetime

class SentinelDB:
    def __init__(self, db_path="sentinel.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.init_tables()

    def init_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node TEXT,
                alert TEXT,
                level TEXT,
                cpu REAL,
                ram REAL,
                timestamp TEXT
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS sightings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                location TEXT,
                lat REAL,
                lng REAL,
                timestamp TEXT
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS zombie_domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                status TEXT,
                risk TEXT,
                action TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def add_alert(self, data):
        self.conn.execute(
            "INSERT INTO alerts (node, alert, level, cpu, ram, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (data['node'], data['alert'], data.get('level', 'info'), data.get('cpu'), data.get('ram'), data['timestamp'])
        )
        self.conn.commit()

    def get_alerts(self, limit=50):
        cursor = self.conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
        return [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()]

    def add_sighting(self, data):
        self.conn.execute(
            "INSERT INTO sightings (target, location, lat, lng, timestamp) VALUES (?, ?, ?, ?, ?)",
            (data['target'], data['location'], data.get('lat'), data.get('lng'), data['timestamp'])
        )
        self.conn.commit()

    def get_sightings(self, limit=20):
        cursor = self.conn.execute("SELECT * FROM sightings ORDER BY timestamp DESC LIMIT ?", (limit,))
        return [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()]

    def add_zombie(self, data):
        self.conn.execute(
            "INSERT INTO zombie_domains (domain, status, risk, action, timestamp) VALUES (?, ?, ?, ?, ?)",
            (data['domain'], data['status'], data['risk'], data['action'], data['timestamp'])
        )
        self.conn.commit()

    def get_zombies(self, limit=50):
        cursor = self.conn.execute("SELECT * FROM zombie_domains ORDER BY timestamp DESC LIMIT ?", (limit,))
        return [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()]