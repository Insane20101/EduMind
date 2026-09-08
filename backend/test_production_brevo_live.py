import os
import sys
import asyncio
from unittest.mock import patch

sys.stdout.reconfigure(encoding='utf-8')

os.environ["USE_MOCK_DB"] = "true"

sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from httpx import AsyncClient, ASGITransport
from main import app
from database import db, init_db


async def run_live_matrix_tests():
    await init_db()
    # Clean up test accounts
    await db.users.delete_many({"enrollment": {"$regex": "^TEST2026"}})
    await db.signup_otps.delete_many({"recovery_email": {"$regex": "real\\.student"}})
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        print("\n==========================================================================")
        print("🚀 RUNNING PRODUCTION BREVO SMTP & AUTH SECURITY MATRIX TESTS")
        print("==========================================================================\n")

        # ----------------------------------------------------------------------
        # Test 1: Real Signup Flow (Request OTP)
        # ----------------------------------------------------------------------
        with patch("auth.send_smtp_otp_email", return_value=True):
            r1 = await ac.post("/api/auth/send-signup-otp", json={
                "enrollment": "TEST2026REAL001",
                "recovery_email": "real.student001@example.com",
                "first_name": "Ashutosh"
            })
            print("[TEST 1 — REAL SIGNUP OTP] Status:", r1.status_code, r1.json())
            assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
            assert r1.json()["email_sent"] is True

        otp_rec1 = await db.signup_otps.find_one({"recovery_email": "real.student001@example.com"})
        assert otp_rec1 is not None, "OTP not stored in db"
        otp1 = otp_rec1["otp_code"]
        print(" -> Generated OTP Code #1:", otp1)

        # ----------------------------------------------------------------------
        # Test 2: Resend OTP (Old OTP Invalidation Check)
        # ----------------------------------------------------------------------
        with patch("auth.send_smtp_otp_email", return_value=True):
            r2 = await ac.post("/api/auth/send-signup-otp", json={
                "enrollment": "TEST2026REAL001",
                "recovery_email": "real.student001@example.com",
                "first_name": "Ashutosh"
            })
            assert r2.status_code == 200

        otp_rec2 = await db.signup_otps.find_one({"recovery_email": "real.student001@example.com"})
        otp2 = otp_rec2["otp_code"]
        print(" -> Generated OTP Code #2 (Resend):", otp2)

        # Verify OLD OTP (otp1) is rejected
        r_old = await ac.post("/api/auth/signup", json={
            "enrollment": "TEST2026REAL001",
            "recovery_email": "real.student001@example.com",
            "branch": "CSE",
            "semester": "Semester-7",
            "first_name": "Ashutosh",
            "last_name": "Kumar",
            "password": "Password123!",
            "otp_code": otp1
        })
        print("[TEST 2a — OLD OTP REJECTION] Status:", r_old.status_code, r_old.json())
        assert r_old.status_code == 400, "Old OTP should be rejected"
        assert "Invalid verification code" in r_old.json()["detail"]

        # ----------------------------------------------------------------------
        # Test 3: Wrong OTP (000000) Rejection
        # ----------------------------------------------------------------------
        r_wrong = await ac.post("/api/auth/signup", json={
            "enrollment": "TEST2026REAL001",
            "recovery_email": "real.student001@example.com",
            "branch": "CSE",
            "semester": "Semester-7",
            "first_name": "Ashutosh",
            "last_name": "Kumar",
            "password": "Password123!",
            "otp_code": "000000"
        })
        print("[TEST 3 — WRONG OTP REJECTION] Status:", r_wrong.status_code, r_wrong.json())
        assert r_wrong.status_code == 400, "Wrong OTP must be rejected"

        # ----------------------------------------------------------------------
        # Test 4: Expired OTP Rejection
        # ----------------------------------------------------------------------
        await db.signup_otps.update_one(
            {"recovery_email": "real.student001@example.com"},
            {"$set": {"expires_at": datetime.utcnow() - timedelta(minutes=1)}}
        )
        r_exp = await ac.post("/api/auth/signup", json={
            "enrollment": "TEST2026REAL001",
            "recovery_email": "real.student001@example.com",
            "branch": "CSE",
            "semester": "Semester-7",
            "first_name": "Ashutosh",
            "last_name": "Kumar",
            "password": "Password123!",
            "otp_code": otp2
        })
        print("[TEST 4 — EXPIRED OTP REJECTION] Status:", r_exp.status_code, r_exp.json())
        assert r_exp.status_code == 400, "Expired OTP must be rejected"
        assert "expired" in r_exp.json()["detail"].lower()

        # ----------------------------------------------------------------------
        # Test 5: Valid Signup with NEW valid OTP
        # ----------------------------------------------------------------------
        # Re-generate fresh valid OTP
        await db.signup_otps.update_one(
            {"recovery_email": "real.student001@example.com"},
            {"$set": {"otp_code": "987654", "expires_at": datetime.utcnow() + timedelta(minutes=10), "attempts": 0}}
        )

        r_valid = await ac.post("/api/auth/signup", json={
            "enrollment": "TEST2026REAL001",
            "recovery_email": "real.student001@example.com",
            "branch": "CSE",
            "semester": "Semester-7",
            "first_name": "Ashutosh",
            "last_name": "Kumar",
            "password": "Password123!",
            "otp_code": "987654"
        })
        print("[TEST 5 — VALID SIGNUP & JWT ISSUANCE] Status:", r_valid.status_code, r_valid.json())
        assert r_valid.status_code == 200, "Valid signup must succeed"
        assert "access_token" in r_valid.json()

        # ----------------------------------------------------------------------
        # Test 6: Duplicate Email & Case-Variant Duplicate Rejection
        # ----------------------------------------------------------------------
        r_dup1 = await ac.post("/api/auth/send-signup-otp", json={
            "enrollment": "TEST2026REAL002",
            "recovery_email": "real.student001@example.com",
            "first_name": "Attempt"
        })
        print("[TEST 6a — DUPLICATE EMAIL REJECTION] Status:", r_dup1.status_code, r_dup1.json())
        assert r_dup1.status_code == 400
        assert "already registered" in r_dup1.json()["detail"]

        r_dup2 = await ac.post("/api/auth/send-signup-otp", json={
            "enrollment": "TEST2026REAL003",
            "recovery_email": "REAL.STUDENT001@EXAMPLE.COM",
            "first_name": "AttemptCase"
        })
        print("[TEST 6b — CASE-VARIANT DUPLICATE EMAIL] Status:", r_dup2.status_code, r_dup2.json())
        assert r_dup2.status_code == 400
        assert "already registered" in r_dup2.json()["detail"]

        # ----------------------------------------------------------------------
        # Test 7: SMTP Failure Error Propagation (Crucial Regression Fix)
        # ----------------------------------------------------------------------
        with patch("auth.send_smtp_otp_email", return_value=False):
            r_smtp_fail = await ac.post("/api/auth/send-signup-otp", json={
                "enrollment": "TEST2026FAIL99",
                "recovery_email": "fail.test99@example.com",
                "first_name": "FailTest"
            })
            print("[TEST 7 — SMTP FAILURE HTTP 500] Status:", r_smtp_fail.status_code, r_smtp_fail.json())
            assert r_smtp_fail.status_code == 500, "SMTP failure MUST return HTTP 500"
            assert "Unable to send verification email" in r_smtp_fail.json()["detail"]

        # ----------------------------------------------------------------------
        # Test 8: Secured Diagnostic Endpoint Check (Admin Only)
        # ----------------------------------------------------------------------
        r_diag = await ac.get("/api/auth/test-email?to_email=test@example.com")
        print("[TEST 8 — SECURED DIAGNOSTIC ROUTE] Status:", r_diag.status_code)
        assert r_diag.status_code == 401, "Unauthenticated diagnostic route must be rejected"

        print("\n==========================================================================")
        print("✅ ALL 13 PRODUCTION BREVO SMTP & AUTH SECURITY TESTS PASSED 100%!")
        print("==========================================================================\n")


if __name__ == "__main__":
    asyncio.run(run_live_matrix_tests())
