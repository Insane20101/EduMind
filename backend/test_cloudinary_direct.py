import requests

url_image = "https://res.cloudinary.com/rqemj4tq/image/upload/v1788470594/edumind/bcs-401/pyq/2e3e4456-5033-4016-a60f-f0e7f5ea6efe.pdf"
url_raw = "https://res.cloudinary.com/rqemj4tq/raw/upload/v1788470594/edumind/bcs-401/pyq/2e3e4456-5033-4016-a60f-f0e7f5ea6efe.pdf"
url_raw_no_ext = "https://res.cloudinary.com/rqemj4tq/raw/upload/v1788470594/edumind/bcs-401/pyq/2e3e4456-5033-4016-a60f-f0e7f5ea6efe.pdf"

for name, u in [("Image URL", url_image), ("Raw URL", url_raw)]:
    try:
        res = requests.get(u, timeout=10)
        print(f"[{name}] Status: {res.status_code}, Length: {len(res.content)}")
        if res.status_code == 200:
            print(f"[{name}] First 30 bytes: {res.content[:30]}")
    except Exception as e:
        print(f"[{name}] Error: {e}")
