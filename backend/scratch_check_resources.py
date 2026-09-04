import asyncio
from database import db

async def check_resources():
    resources = await db.resources.find({}).to_list(100)
    print(f"Total resources found: {len(resources)}")
    for r in resources:
        print(f"ID: {r.get('resource_id')}, Title: {r.get('title')}, file_url: {r.get('file_url')}, url: {r.get('url')}")

if __name__ == '__main__':
    asyncio.run(check_resources())
