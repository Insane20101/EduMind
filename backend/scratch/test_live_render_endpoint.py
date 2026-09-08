import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://edumind-ebk1.onrender.com/api/auth/send-signup-otp"
payload = {
    "enrollment": "TEST2026LIVE02",
    "recovery_email": "test.edumind.live@gmail.com",
    "first_name": "Ashutosh"
}

print("==========================================================================")
print("🌐 LIVE RENDER ENDPOINT INVOCATION TEST (Fresh Email)")
print("==========================================================================")
print(f"Target URL: {url}")
print(f"Payload: {payload}\n")

try:
    response = requests.post(url, json=payload, timeout=20)
    print(f"HTTP Status Code: {response.status_code}")
    print(f"Response Body   : {response.text}")
except Exception as e:
    print(f"Request Exception: {e}")

print("==========================================================================")
