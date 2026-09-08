import os
import sys
import asyncio
from unittest.mock import patch

os.environ["USE_MOCK_DB"] = "true"

sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from httpx import AsyncClient, ASGITransport
from main import app
from database import db, init_db


async def run_tests():
    await init_db()
    await db.users.delete_many({"enrollment": {"$regex": "^2026"}})
    await db.signup_otps.delete_many({"recovery_email": {"$regex": "test\\.student"}})
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        print("--- Running EduMind Signup OTP & Uniqueness E2E Tests ---")
        
        # Test 0: Test Unauthenticated /api/auth/test-email (Should be rejected with 401)
        r0 = await ac.get("/api/auth/test-email?to_email=test@example.com")
        print("[TEST 0] Unauthenticated /test-email status:", r0.status_code)
        assert r0.status_code == 401, f"Expected 401 Unauthorized for unprotected test-email, got {r0.status_code}"

        # Test 1a: SMTP Failure handling (When send_smtp_otp_email returns False)
        with patch("auth.send_smtp_otp_email", return_value=False):
            r1a = await ac.post("/api/auth/send-signup-otp", json={
                "enrollment": "2026FAIL001",
                "recovery_email": "test.fail001@example.com",
                "first_name": "FailTest"
            })
            print("[TEST 1a] SMTP Failure Send Signup OTP status:", r1a.status_code, r1a.json())
            assert r1a.status_code == 500, f"Expected 500 on SMTP failure, got {r1a.status_code}"
            assert "Unable to send verification email" in r1a.json()["detail"]

        # Test 1b: Successful Send OTP (Mocking SMTP success)
        with patch("auth.send_smtp_otp_email", return_value=True):
            r1 = await ac.post("/api/auth/send-signup-otp", json={
                "enrollment": "2026TEST001",
                "recovery_email": "test.student001@example.com",
                "first_name": "Test"
            })
            print("[TEST 1b] Send Signup OTP status:", r1.status_code, r1.json())
            assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
            assert r1.json()["email_sent"] is True

        # Fetch OTP from DB
        otp_rec = await db.signup_otps.find_one({"recovery_email": "test.student001@example.com"})
        assert otp_rec is not None, "OTP record not found in database"
        print("[TEST 1 SUCCESS] Generated OTP:", otp_rec["otp_code"])

        # Test 2: Invalid OTP signup
        r2 = await ac.post("/api/auth/signup", json={
            "enrollment": "2026TEST001",
            "recovery_email": "test.student001@example.com",
            "branch": "CSE",
            "semester": "Semester-3",
            "first_name": "Test",
            "last_name": "User",
            "password": "Password123!",
            "otp_code": "000000"
        })
        print("[TEST 2] Invalid OTP response:", r2.status_code, r2.json())
        assert r2.status_code == 400, f"Expected 400, got {r2.status_code}"

        # Test 3: Valid OTP signup
        r3 = await ac.post("/api/auth/signup", json={
            "enrollment": "2026TEST001",
            "recovery_email": "test.student001@example.com",
            "branch": "CSE",
            "semester": "Semester-3",
            "first_name": "Test",
            "last_name": "User",
            "password": "Password123!",
            "otp_code": otp_rec["otp_code"]
        })
        print("[TEST 3] Valid Signup response:", r3.status_code, r3.json())
        assert r3.status_code == 200, f"Expected 200, got {r3.status_code}"
        assert "access_token" in r3.json(), "access_token missing from signup response"

        # Test 4: Duplicate Email Send OTP (Exact Case)
        r4 = await ac.post("/api/auth/send-signup-otp", json={
            "enrollment": "2026NEW002",
            "recovery_email": "test.student001@example.com",
            "first_name": "Attempt"
        })
        print("[TEST 4] Duplicate Email OTP response:", r4.status_code, r4.json())
        assert r4.status_code == 400, f"Expected 400, got {r4.status_code}"
        assert "Email address already registered" in r4.json()["detail"], "Expected email duplication detail"

        # Test 4b: Duplicate Email Send OTP (Mixed Case Variant)
        r4b = await ac.post("/api/auth/send-signup-otp", json={
            "enrollment": "2026NEW003",
            "recovery_email": "TEST.STUDENT001@ExAmPlE.CoM",
            "first_name": "AttemptMixedCase"
        })
        print("[TEST 4b] Case-Variant Duplicate Email OTP response:", r4b.status_code, r4b.json())
        assert r4b.status_code == 400, f"Expected 400, got {r4b.status_code}"
        assert "Email address already registered" in r4b.json()["detail"], "Expected case-insensitive email duplication detail"

        # Test 5: Check Keep Alive Endpoint
        r5 = await ac.get("/api/keep-alive")
        print("[TEST 5] Keep Alive endpoint response:", r5.status_code, r5.json())
        assert r5.status_code == 200
        assert r5.json()["status"] == "alive"

        # Test 6: Direct /signup endpoint gate case-variant enrollment & email uniqueness
        with patch("utils.email_utils.send_smtp_otp_email", return_value=True):
            r6_otp = await ac.post("/api/auth/send-signup-otp", json={
                "enrollment": "2026CASEGATED01",
                "recovery_email": "case.gated@example.com",
                "first_name": "GateTest"
            })
            assert r6_otp.status_code == 200
        
        rec_gated = await db.signup_otps.find_one({"recovery_email": "case.gated@example.com"})

        # Submitting signup with case-variant duplicate enrollment (2026test001 vs 2026TEST001)
        r6_dup_enr = await ac.post("/api/auth/signup", json={
            "enrollment": "2026test001",
            "recovery_email": "case.gated@example.com",
            "branch": "CSE",
            "semester": "Semester-3",
            "first_name": "GateTest",
            "last_name": "User",
            "password": "Password123!",
            "otp_code": rec_gated["otp_code"]
        })
        print("[TEST 6a] Direct Signup Case-Variant Enrollment Duplicate response:", r6_dup_enr.status_code, r6_dup_enr.json())
        assert r6_dup_enr.status_code == 400
        assert "Enrollment number already registered" in r6_dup_enr.json()["detail"]

        # Test 6b: Direct Signup Case-Variant Email Duplicate Gate
        await db.signup_otps.update_one(
            {"recovery_email": "test.student001@example.com"},
            {"$set": {
                "enrollment": "2026CASEGATED02",
                "recovery_email": "test.student001@example.com",
                "otp_code": "999999",
                "attempts": 0,
                "expires_at": datetime.utcnow() + timedelta(minutes=10),
                "created_at": datetime.utcnow()
            }},
            upsert=True
        )

        r6_dup_email = await ac.post("/api/auth/signup", json={
            "enrollment": "2026CASEGATED02",
            "recovery_email": "TEST.STUDENT001@EXAMPLE.COM",
            "branch": "CSE",
            "semester": "Semester-3",
            "first_name": "GateTest",
            "last_name": "User",
            "password": "Password123!",
            "otp_code": "999999"
        })
        print("[TEST 6b] Direct Signup Case-Variant Email Duplicate response:", r6_dup_email.status_code, r6_dup_email.json())
        assert r6_dup_email.status_code == 400
        assert "Email address already registered" in r6_dup_email.json()["detail"]

        print("\n==================================================")
        print("ALL BACKEND OTP & UNIQUENESS TESTS PASSED 100%!")
        print("==================================================")


if __name__ == "__main__":
    asyncio.run(run_tests())
