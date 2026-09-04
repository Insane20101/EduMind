import asyncio
import json
import requests

# Base URL for API
BASE_URL = "http://localhost:8000"

def test_two_student_responses():
    print("=" * 70)
    print("TESTING TWO SEPARATE STUDENT ACCOUNTS SIDE-BY-SIDE ON /BCS-401...")
    print("=" * 70)

    # Student 1 Registration / Auth Token
    user1_enrollment = "2023TEST0001"
    user1_pass = "Password123!"
    
    # Student 2 Registration / Auth Token
    user2_enrollment = "2023TEST0002"
    user2_pass = "Password123!"

    # Signup Student 1
    r1_signup = requests.post(f"{BASE_URL}/api/auth/signup", json={
        "enrollment": user1_enrollment,
        "name": "Test Student One",
        "email": "teststudent1@example.com",
        "recovery_email": "teststudent1_rec@example.com",
        "password": user1_pass,
        "semester": "Semester-4",
        "branch": "CSE"
    })
    
    # Signup Student 2
    r2_signup = requests.post(f"{BASE_URL}/api/auth/signup", json={
        "enrollment": user2_enrollment,
        "name": "Test Student Two",
        "email": "teststudent2@example.com",
        "recovery_email": "teststudent2_rec@example.com",
        "password": user2_pass,
        "semester": "Semester-4",
        "branch": "CSE"
    })

    # Login Student 1
    r1_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "enrollment": user1_enrollment,
        "password": user1_pass
    })
    token1 = r1_login.json().get("access_token")

    # Login Student 2
    r2_login = requests.post(f"{BASE_URL}/api/auth/login", json={
        "enrollment": user2_enrollment,
        "password": user2_pass
    })
    token2 = r2_login.json().get("access_token")

    headers1 = {"Authorization": f"Bearer {token1}"} if token1 else {}
    headers2 = {"Authorization": f"Bearer {token2}"} if token2 else {}

    subject_id = "BCS-401"

    # Fetch Notes
    notes1 = requests.get(f"{BASE_URL}/api/resources?subject_id={subject_id}&resource_type=note", headers=headers1).json()
    notes2 = requests.get(f"{BASE_URL}/api/resources?subject_id={subject_id}&resource_type=note", headers=headers2).json()

    # Fetch PYQs
    pyqs1 = requests.get(f"{BASE_URL}/api/resources?subject_id={subject_id}&resource_type=pyq", headers=headers1).json()
    pyqs2 = requests.get(f"{BASE_URL}/api/resources?subject_id={subject_id}&resource_type=pyq", headers=headers2).json()

    # Fetch Playlists
    pl1 = requests.get(f"{BASE_URL}/api/resources/playlists?subject_id={subject_id}", headers=headers1).json()
    pl2 = requests.get(f"{BASE_URL}/api/resources/playlists?subject_id={subject_id}", headers=headers2).json()

    print("\n--- STUDENT 1 (2023TEST0001) RESPONSES ---")
    print(f"GET /notes -> {json.dumps(notes1, indent=2)}")
    print(f"GET /pyqs  -> {json.dumps(pyqs1, indent=2)}")
    print(f"GET /playlists -> {json.dumps(pl1, indent=2)}")

    print("\n--- STUDENT 2 (2023TEST0002) RESPONSES ---")
    print(f"GET /notes -> {json.dumps(notes2, indent=2)}")
    print(f"GET /pyqs  -> {json.dumps(pyqs2, indent=2)}")
    print(f"GET /playlists -> {json.dumps(pl2, indent=2)}")

if __name__ == "__main__":
    test_two_student_responses()
