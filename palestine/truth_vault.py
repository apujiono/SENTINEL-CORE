# palestine/truth_vault.py
import subprocess
import json

def upload_to_ipfs(file_path):
    try:
        result = subprocess.run(
            ["ipfs", "add", file_path],
            capture_output=True,
            text=True
        )
        if "added" in result.stdout:
            hash = result.stdout.split()[1]
            print(f"✅ Bukti disimpan di IPFS: https://ipfs.io/ipfs/{hash}")
            return hash
    except:
        print("❌ Gagal upload ke IPFS")
        return None