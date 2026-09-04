import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

async def test_real_mongodb():
    print("=" * 70)
    print("TESTING REAL MONGODB PERSISTENT DATABASE CONNECTION...")
    print("=" * 70)
    print(f"MONGODB_URI: {MONGODB_URI[:35]}...")
    
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.edumind
    
    # 1. List collections
    collections = await db.list_collection_names()
    print(f"Collections found in real MongoDB 'edumind' database: {collections}")
    
    # 2. Count users in real MongoDB
    user_count = await db.users.count_documents({})
    print(f"Total Users in Real MongoDB: {user_count}")
    
    users = await db.users.find({}).to_list(10)
    for u in users:
        print(f"  -> Real DB User Enrollment: '{u.get('enrollment')}', Email: '{u.get('email')}', Semester: '{u.get('semester')}'")
        
    # 3. Count resources in real MongoDB
    resource_count = await db.resources.count_documents({})
    print(f"Total Approved Resources in Real MongoDB: {resource_count}")
    
    resources = await db.resources.find({}).to_list(10)
    for r in resources:
        print(f"  -> Real DB Resource Title: '{r.get('title')}', Subject: '{r.get('subject_id')}', Type: '{r.get('resource_type')}'")
        
    # 4. Count playlists in real MongoDB
    playlist_count = await db.playlists.count_documents({})
    print(f"Total Playlists in Real MongoDB: {playlist_count}")

if __name__ == "__main__":
    asyncio.run(test_real_mongodb())
