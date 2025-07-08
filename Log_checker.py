import json
import os
from datetime import datetime

# === Load resume_log.json ===
with open("resume_log.json", "r") as file:
    resume = json.load(file)

log_files = []
for kategori in resume["log_files"].values():
    log_files.extend(kategori)

log_last = resume["log_terakhir_diperbarui"]

# === Cek apakah file log tersedia ===
missing_files = [f for f in log_files if not os.path.exists(f)]

# === Cek file terbaru berdasarkan modified time ===
def get_latest_file(files):
    latest = max(files, key=lambda f: os.path.getmtime(f))
    return latest

try:
    latest_file = get_latest_file([f for f in log_files if os.path.exists(f)])
except Exception as e:
    latest_file = None

# === Ringkasan Output ===
print("=== LOG CHECKER ===")
print(f"Total log terdaftar: {len(log_files)}")
print(f"File hilang: {len(missing_files)}")

if missing_files:
    for f in missing_files:
        print(f" ❌ Tidak ditemukan: {f}")
else:
    print(" ✅ Semua file ditemukan.")

if latest_file:
    latest_name = os.path.basename(latest_file)
    if latest_name != log_last:
        print(f" ⚠️ File terbaru adalah '{latest_name}', tapi di resume tertulis '{log_last}'")
    else:
        print(f" ✅ File terbaru sesuai: {log_last}")
    tmod = datetime.fromtimestamp(os.path.getmtime(latest_file))
    print(f" ⏱️ Terakhir dimodifikasi: {tmod}")
else:
    print(" ❌ Tidak bisa menentukan file terbaru.")

print("=== SELESAI ===")
