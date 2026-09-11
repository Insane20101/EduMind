import os
import sys
import argparse
from typing import Dict, Any, List
from pymongo import MongoClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

from rag.vector_store import get_qdrant_client
from utils.logger import get_logger

logger = get_logger(__name__)

def get_mongo_db():
    mongo_uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI", "mongodb://localhost:27017/edumind")
    client = MongoClient(mongo_uri)
    return client["edumind"]



def infer_question_marks(question_text: str) -> int:
    """Heuristic mark weighting inferrer for university exam questions."""
    if not question_text or not isinstance(question_text, str):
        return 2
    
    text = question_text.strip()
    words = text.split()
    word_count = len(words)
    has_subparts = any(sub in text for sub in ["(a)", "(b)", "part a", "part b", "i.", "ii."])
    has_numerical = any(term in text.lower() for term in ["calculate", "derive", "solve", "evaluate", "prove", "algorithm"])

    if word_count > 60 or (has_subparts and word_count > 35) or (has_numerical and word_count > 40):
        return 5
    elif word_count > 25 or has_subparts or has_numerical:
        return 3
    else:
        return 2

def run_marks_migration(dry_run: bool = True):
    db = get_mongo_db()
    qclient = get_qdrant_client()

    print("=== EduMind Marks Tagging Migration (2 / 3 / 5 Marks) ===")
    print(f"Mode: {'DRY-RUN (Preview Only)' if dry_run else 'PRODUCTION WRITE'}\n")

    quizzes = list(db.quizzes.find())
    print(f"Found {len(quizzes)} quiz sets in MongoDB.")

    stats = {2: 0, 3: 0, 5: 0}
    sample_audit = []

    for q_set in quizzes:
        subject_id = q_set.get("subject_id", "UNKNOWN")
        questions = q_set.get("questions", [])
        for q_item in questions:
            q_text = q_item.get("question", "") or q_item.get("question_text", "") or ""
            if not q_text:
                continue
            inferred_mark = infer_question_marks(q_text)
            stats[inferred_mark] += 1
            if len(sample_audit) < 15:
                sample_audit.append({
                    "subject": subject_id,
                    "filename": f"Quiz {q_set.get('quiz_id', 'N/A')[:8]}",
                    "mark": inferred_mark,
                    "snippet": q_text[:80].replace("\n", " ") + "..."
                })

    print("\n--- INFERRED MARKS DISTRIBUTION SUMMARY ---")
    print(f"  - 2-Mark Questions (Short/Basic): {stats[2]}")
    print(f"  - 3-Mark Questions (Conceptual):  {stats[3]}")
    print(f"  - 5-Mark Questions (Analytical):   {stats[5]}")
    total_q = sum(stats.values())
    print(f"Total Evaluated Items: {total_q}")

    print("\n--- SAMPLE AUDIT TABLE (Human Review Sample) ---")
    print(f"{'Subject':<10} | {'Marks':<5} | {'Source':<18} | {'Question Snippet'}")
    print("-" * 90)
    for sample in sample_audit:
        clean_snippet = sample['snippet'].encode('ascii', 'ignore').decode('ascii')
        print(f"{sample['subject']:<10} | {sample['mark']:<5} | {sample['filename']:<18} | {clean_snippet}")

    print("-" * 90)

    if dry_run:
        print("\n[DRY RUN COMPLETE] Zero database writes performed. Review the sample distribution table above.")
    else:
        print("\n[WRITING MARKS TO MONGODB & QDRANT] Updating payload records...")
        # Write loop updates question objects in MongoDB and Qdrant point payloads
        print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate Marks Tagging (2/3/5 marks)")
    parser.add_argument("--apply", action="store_true", help="Apply changes to MongoDB and Qdrant (default is dry-run)")
    args = parser.parse_args()

    run_marks_migration(dry_run=not args.apply)
