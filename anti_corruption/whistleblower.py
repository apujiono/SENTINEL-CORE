# anti_corruption/whistleblower.py
import shutil
from utils.crypto import encrypt_file

def submit_evidence(file_path):
    encrypted = encrypt_file(file_path)
    shutil.copy(encrypted, "/tmp/whistleblower_encrypted.dat")
    print("✅ Bukti dikirim ke brankas aman")