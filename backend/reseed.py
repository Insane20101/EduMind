import asyncio
from database import db
from seed_subjects import seed_subjects_if_needed
from schemas import Subject
from pydantic import ValidationError

async def main():
    print("Dropping existing subjects collection...")
    await db.subjects.delete_many({})
    
    print("Reseeding subjects collection...")
    await seed_subjects_if_needed(db)
    
    print("Verifying all subjects in MongoDB...")
    cursor = db.subjects.find({})
    docs = await cursor.to_list(length=None)
    
    for doc in docs:
        doc.pop("_id", None)
        try:
            # Validate through Pydantic to ensure post-seed data is strictly correct
            Subject(**doc)
        except ValidationError as e:
            print(f"❌ Post-seed validation failed for {doc.get('code', 'UNKNOWN')}")
            print(e)
            return

    print("✅ All subjects seeded and verified successfully.")

if __name__ == "__main__":
    asyncio.run(main())
