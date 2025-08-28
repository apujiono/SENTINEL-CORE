# tools/zombie_scanner.py
import subprocess
import json
import re
from urllib.parse import urlparse

def is_domain_expired(domain):
    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True,
            text=True,
            timeout=10
        )
        if any(word in result.stdout.lower() for word in ["no match", "not found", "expired", "available"]):
            return True
    except:
        pass
    return False

def check_subdomain_takeover(subdomain):
    try:
        import requests
        r = requests.get(f"http://{subdomain}", timeout=5, allow_redirects=False)
        server = r.headers.get('Server', '').lower()
        if any(s in server for s in ['heroku', 'github', 'aws', 'azure', 'netlify', 's3']):
            return True
    except:
        try:
            result = subprocess.run(
                ["nslookup", subdomain],
                capture_output=True,
                text=True
            )
            if any(cloud in result.stdout.lower() for cloud in ['heroku', 'github', 's3', 'cloudfront']):
                return True
        except:
            pass
    return False

def scan_zombie_domains(keyword):
    domains = [
        f"{keyword}.com", f"{keyword}.net", f"{keyword}.org",
        f"old-{keyword}.com", f"backup-{keyword}.net", f"legacy-{keyword}.org"
    ]
    results = []

    for domain in domains:
        if is_domain_expired(domain):
            results.append({
                "domain": domain,
                "status": "expired",
                "risk": "high",
                "action": "register_or_takeover"
            })

        subdomains = [f"www.{domain}", f"admin.{domain}", f"blog.{domain}"]
        for sub in subdomains:
            if check_subdomain_takeover(sub):
                results.append({
                    "domain": sub,
                    "status": "subdomain-takeover",
                    "risk": "critical",
                    "action": "claim"
                })

    return results