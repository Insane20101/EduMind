import json
import os
from pydantic import ValidationError
from schemas import Subject

async def seed_subjects_if_needed(db):
    count = await db.subjects.count_documents({})
    if count > 0:
        return

    path = os.path.join(os.path.dirname(__file__), "subjects_seed.json")
    if not os.path.exists(path):
        print("subjects_seed.json not found — skipping subject seed.")
        return

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    docs = []
    for semester, subjects in raw.items():
        for subj in subjects:
            try:
                # Validate through Pydantic Subject schema
                validated = Subject(
                    semester=semester,
                    code=subj["code"],
                    name=subj["name"],
                    status=subj.get("status", "none"),
                    playlists=subj.get("playlists", []),
                    note=subj.get("note")
                )
                docs.append(validated.dict())
            except ValidationError as e:
                print(f"❌ Validation failed for subject {subj.get('code', 'UNKNOWN')} in {semester}:")
                print(e)
                raise  # Fail loudly at seed time instead of silently importing bad data

    if docs:
        await db.subjects.insert_many(docs)
    print(f"Seeded {len(docs)} subjects into the database.")
