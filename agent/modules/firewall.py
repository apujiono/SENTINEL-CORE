# agent/modules/firewall.py
import os

class Firewall:
    def block_ip(self, ip):
        try:
            os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
            os.system(f"sudo iptables -A OUTPUT -d {ip} -j DROP")
            return True
        except:
            return False