"""Seed a smoke-test admin into the mock DB by calling the running local API."""
import requests
import sys

BASE = "http://localhost:8000/api"

# The create_admin script is interactive, so we drive it via the API instead.
# We'll use the bcrypt-hashed password route, but we need to register the admin
# through the live server's /admin/auth route — it doesn't have a seeding endpoint.
# So instead, write directly into mock_db.json using the server's own passlib context
# by having uvicorn's own worker do the hashing.

import subprocess
result = subprocess.run(
    ["python", "-c",
     "import sys,os; sys.path.insert(0,os.getcwd()); "
     "from passlib.context import CryptContext; import json; "
     "pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); "
     "h=pwd.hash('smokepass1'); "
     "print(json.dumps({'hash':h}))"],
    capture_output=True, text=True,
    cwd=r"C:\Users\ASUS\Desktop\EduMind\backend"
)
print("stdout:", result.stdout.strip()[:200])
print("stderr:", result.stderr.strip()[:200])

if result.returncode != 0 or not result.stdout.strip():
    print("HASH FAILED")
    sys.exit(1)

import json
h = json.loads(result.stdout.strip())["hash"]

# Write directly to mock_db.json
import pathlib
db_file = pathlib.Path(r"C:\Users\ASUS\Desktop\EduMind\backend\data\mock_db.json")
db = json.loads(db_file.read_text(encoding="utf-8"))
if not db.get("admin_credentials"):
    db["admin_credentials"] = []
# Remove any existing smoke admin
db["admin_credentials"] = [a for a in db["admin_credentials"] if a.get("admin_id") != "smokeadmin"]
db["admin_credentials"].append({"admin_id": "smokeadmin", "password_hash": h})

# Seed CS301 subject for smoke test
if not db.get("subjects"):
    db["subjects"] = []
db["subjects"] = [s for s in db["subjects"] if s.get("code") != "CS301"]
db["subjects"].append({
    "semester": "Semester-5",
    "code": "CS301",
    "name": "Test Subject CS301",
    "status": "none",
    "playlists": [],
    "note": None
})

db_file.write_text(json.dumps(db, indent=2, default=str), encoding="utf-8")
print("Admin and CS301 subject seeded into mock_db.json")
