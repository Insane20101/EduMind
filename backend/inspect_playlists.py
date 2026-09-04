import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

async def inspect_real_playlists():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.edumind

    print("=" * 70)
    print("INSPECTING ALL PLAYLISTS IN REAL MONGODB...")
    print("=" * 70)

    playlists = await db.playlists.find({}).to_list(100)
    print(f"Total Playlists in Real MongoDB: {len(playlists)}")
    for p in playlists:
        print(f"  Playlist ID: {p.get('playlist_id')}, Title: '{p.get('title')}', Subject ID: '{p.get('subject_id')}', URL: '{p.get('url')}'")

if __name__ == "__main__":
    asyncio.run(inspect_real_playlists())
