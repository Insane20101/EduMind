import asyncio
import os
import re
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

async def test_case_insensitive_mongo():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.edumind

    print("=" * 70)
    print("TESTING REAL MONGODB CASE-INSENSITIVE QUERIES...")
    print("=" * 70)

    test_subject_ids = ["BCS-401", "bcs-401", "Bcs-401", "  bcs-401  "]

    for sub_id in test_subject_ids:
        query = {"status": "approved"}
        query["subject_id"] = {"$regex": f"^{re.escape(sub_id.strip())}$", "$options": "i"}
        
        docs = await db.resources.find(query).to_list(100)
        print(f"Query subject_id='{sub_id}' -> Found {len(docs)} approved resources in REAL MongoDB.")
        for d in docs:
            print(f"   Resource: {d.get('title')}, Type: {d.get('resource_type')}, Subject: {d.get('subject_id')}")

    for sub_id in test_subject_ids:
        query = {"subject_id": {"$regex": f"^{re.escape(sub_id.strip())}$", "$options": "i"}}
        docs = await db.playlists.find(query).to_list(100)
        print(f"Query subject_id='{sub_id}' -> Found {len(docs)} playlists in REAL MongoDB.")
        for d in docs:
            print(f"   Playlist: {d.get('title')}, Subject: {d.get('subject_id')}")

if __name__ == "__main__":
    asyncio.run(test_case_insensitive_mongo())
