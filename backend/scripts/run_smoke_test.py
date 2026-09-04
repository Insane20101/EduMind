"""Comprehensive verification test for EduMind Phase B features using real assets."""
import base64
import json
import random
import requests
import sys
import os

BASE = "http://localhost:8000/api"
PASS_OK = []
FAIL = []

def check(label, condition, detail=""):
    if condition:
        PASS_OK.append(label)
        print(f"  PASS  {label}")
    else:
        FAIL.append(label)
        print(f"  FAIL  {label}  [{detail}]")

def main():
    # 0. Load real png asset
    png_path = r"C:\Users\ASUS\Desktop\EduMind\frontend\src\assets\hero.png"
    if not os.path.exists(png_path):
        print(f"Error: PNG asset not found at {png_path}")
        sys.exit(1)
    with open(png_path, "rb") as f:
        real_png_bytes = f.read()

    print("=== Step 1: GET / health check ===")
    try:
        r = requests.get("http://localhost:8000/")
        check("Health endpoint returns 200", r.status_code == 200, f"status={r.status_code}")
    except Exception as e:
        check("Health endpoint returns 200", False, str(e))
        sys.exit(1)

    print("\n=== Step 2: Admin login ===")
    r = requests.post(f"{BASE}/admin/auth/login", json={"admin_id": "smokeadmin", "password": "smokepass1"})
    check("Admin login succeeds", r.status_code == 200, r.text[:200])
    admin_token = r.json().get("access_token", "") if r.ok else ""
    admin_hdr = {"Authorization": f"Bearer {admin_token}"}

    print("\n=== Step 3: Admin list resources ===")
    r = requests.get(f"{BASE}/admin/resources/", headers=admin_hdr)
    check("Admin list resources succeeds", r.status_code == 200, r.text[:200])

    print("\n=== Step 4: Admin upload (auto-approved Cloudinary resource) ===")
    r = requests.post(
        f"{BASE}/admin/resources/upload",
        headers=admin_hdr,
        data={"subject_id": "CS301", "resource_type": "note", "title": "Phase B Admin Core Note"},
        files={"file": ("admin_doc.png", real_png_bytes, "image/png")},
    )
    check("Admin upload returns 200/201", r.status_code == 200, r.text[:300])
    admin_res_id = r.json().get("resource_id", "") if r.ok else ""
    admin_res_url = r.json().get("url", "") if r.ok else ""
    check("Admin upload result has resource_id", bool(admin_res_id))
    check("Admin upload result has Cloudinary URL", admin_res_url.startswith("https://"), admin_res_url[:100])

    print("\n=== Step 5: Public resource list filters by subject ===")
    r = requests.get(f"{BASE}/resources/?subject_id=CS301&resource_type=note")
    check("Public resource GET returns 200", r.status_code == 200, r.text[:200])
    public_resources = r.json() if r.ok else []
    check("Admin note is visible in public list", any(d.get("resource_id") == admin_res_id for d in public_resources))

    print("\n=== Step 6: Student signup + login (Unique enrollment) ===")
    unique_seq = str(random.randint(1000, 9999))
    student_enrollment = f"2023CSE{unique_seq}"
    print(f"Using student enrollment: {student_enrollment}")
    
    r = requests.post(f"{BASE}/auth/signup", json={
        "enrollment": student_enrollment,
        "branch": "CSE",
        "semester": "Semester-5",
        "first_name": "Smoke",
        "last_name": "Student",
        "password": "studentpassword"
    })
    check("Student signup returns 200", r.status_code == 200, r.text[:200])

    r = requests.post(f"{BASE}/auth/login", json={"enrollment": student_enrollment, "password": "studentpassword"})
    check("Student login succeeds", r.status_code == 200, r.text[:200])
    student_token = r.json().get("access_token", "") if r.ok else ""
    student_hdr = {"Authorization": f"Bearer {student_token}"}

    print("\n=== Step 7: Student submits resource suggestions ===")
    # 7a: Suggestion with only URL
    r = requests.post(
        f"{BASE}/resources/suggest",
        headers=student_hdr,
        data={
            "subject_id": "CS301",
            "resource_type": "note",
            "title": "Student Suggested Link",
            "url": "https://google.com/study-notes"
        }
    )
    check("Student URL suggest returns 200", r.status_code == 200, r.text[:200])
    url_suggest_id = r.json().get("resource_id", "") if r.ok else ""

    # 7b: Suggestion with file upload
    r = requests.post(
        f"{BASE}/resources/suggest",
        headers=student_hdr,
        data={
            "subject_id": "CS301",
            "resource_type": "pyq",
            "title": "Student Suggested PYQ File"
        },
        files={"file": ("student_pyq.png", real_png_bytes, "image/png")}
    )
    check("Student File suggest returns 200", r.status_code == 200, r.text[:200])
    file_suggest_id = r.json().get("resource_id", "") if r.ok else ""

    print("\n=== Step 8: Admin checks pending list ===")
    r = requests.get(f"{BASE}/admin/resources/?status=pending", headers=admin_hdr)
    check("Admin pending list returns 200", r.status_code == 200)
    pending_list = r.json() if r.ok else []
    check("URL suggestion in pending list", any(d.get("resource_id") == url_suggest_id for d in pending_list))
    check("File suggestion in pending list", any(d.get("resource_id") == file_suggest_id for d in pending_list))

    print("\n=== Step 9: Admin approves suggestions ===")
    r = requests.post(f"{BASE}/admin/resources/{url_suggest_id}/approve", headers=admin_hdr)
    check("Approve URL suggest returns 200", r.status_code == 200)
    r = requests.post(f"{BASE}/admin/resources/{file_suggest_id}/approve", headers=admin_hdr)
    check("Approve File suggest returns 200", r.status_code == 200)

    print("\n=== Step 10: Verify suggestions are now in public list ===")
    r = requests.get(f"{BASE}/resources/?subject_id=CS301")
    check("Public resources list contains approved URL suggest", any(d.get("resource_id") == url_suggest_id for d in r.json()))
    check("Public resources list contains approved File suggest", any(d.get("resource_id") == file_suggest_id for d in r.json()))

    print("\n=== Step 11: Deprecated subjects/notes and subjects/pyqs endpoints ===")
    r = requests.get(f"{BASE}/subjects/CS301/notes")
    check("Deprecated notes endpoint returns 200", r.status_code == 200)
    check("Deprecated notes endpoint has Deprecation header", r.headers.get("Deprecation") == "true")
    check("Deprecated notes endpoint has successor successor-version Link", "successor-version" in r.headers.get("Link", ""))

    print("\n=== Step 12: Security separation & JWT validation ===")
    def decode_jwt(token):
        try:
            payload_b64 = token.split(".")[1]
            padded = payload_b64 + "=" * (4 - len(payload_b64) % 4)
            return json.loads(base64.b64decode(padded).decode("utf-8"))
        except:
            return {}

    admin_payload = decode_jwt(admin_token)
    student_payload = decode_jwt(student_token)

    check("Admin JWT contains token_type='admin'", admin_payload.get("token_type") == "admin")
    check("Student JWT does NOT contain token_type='admin'", student_payload.get("token_type") != "admin")
    check("Student JWT contains enrollment number", "enrollment" in student_payload)

    # Cross testing tokens on routes
    r = requests.get(f"{BASE}/admin/resources/", headers=student_hdr)
    check("Student token is rejected on Admin route (401)", r.status_code == 401)

    r = requests.post(
        f"{BASE}/resources/suggest",
        headers=admin_hdr,
        data={"subject_id": "CS301", "resource_type": "note", "title": "Admin as Student"}
    )
    check("Admin token is rejected on student suggestion suggest route (401)", r.status_code == 401)

    print("\n=== RESULTS ===")
    print(f"Passed: {len(PASS_OK)}/{len(PASS_OK)+len(FAIL)}")
    if FAIL:
        print("Failed steps:", FAIL)
        sys.exit(1)
    else:
        print("ALL RUNTIME SMOKE TESTS PASSED!")

if __name__ == "__main__":
    main()
