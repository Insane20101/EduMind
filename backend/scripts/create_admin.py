import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import getpass
from passlib.context import CryptContext
from database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def main():
    print("--- EduMind Admin Creation ---")
    
    # Check if admin already exists
    existing = await db.admin_credentials.find_one({})
    if existing:
        print("Error: An admin account already exists. Only one admin is allowed.")
        return

    admin_id = input("Enter admin_id: ").strip()
    if not admin_id:
        print("Error: admin_id cannot be empty.")
        return

    password = getpass.getpass("Enter password: ")
    if len(password) < 8:
        print("Error: password must be at least 8 characters.")
        return

    password_confirm = getpass.getpass("Confirm password: ")
    if password != password_confirm:
        print("Error: passwords do not match.")
        return

    password_hash = pwd_context.hash(password)

    await db.admin_credentials.insert_one({
        "admin_id": admin_id,
        "password_hash": password_hash
    })

    print(f"Admin '{admin_id}' created successfully!")

if __name__ == "__main__":
    asyncio.run(main())
