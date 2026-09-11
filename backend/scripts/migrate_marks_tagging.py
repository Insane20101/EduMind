import os
import sys
import re
import argparse
from typing import Dict, Any, List
from pymongo import MongoClient
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

from rag.vector_store import get_qdrant_client
from utils.logger import get_logger

logger = get_logger(__name__)

def infer_question_marks_with_source(question_text: str) -> (int, str):
    """
    Infers mark weightings (2, 3, 5 marks) from question text using explicit exam mark tags,
    analytical question heuristics, and calibrated word-length fallbacks.
    Returns (inferred_mark: int, rule_source: str).
    """
    if not question_text or not isinstance(question_text, str):
        return 2, "default_fallback"

    text = question_text.strip()
    lowered = text.lower()
    words = text.split()
    wlen = len(words)

    # 1. Explicit Mark Regex Matching (Highest Precision)
    if re.search(r'\[\s*(?:5|10)\s*marks?\s*\]|\(\s*(?:5|10)\s*marks?\s*\)|\b(?:5|10)\s*marks?\b|\bmarks?\s*:\s*(?:5|10)\b', lowered):
        return 5, "explicit_regex"
    if re.search(r'\[\s*3\s*marks?\s*\]|\(\s*3\s*marks?\s*\)|\b3\s*marks?\b|\bmarks?\s*:\s*3\b', lowered):
        return 3, "explicit_regex"
    if re.search(r'\[\s*2\s*marks?\s*\]|\(\s*2\s*marks?\s*\)|\b2\s*marks?\b|\bmarks?\s*:\s*2\b', lowered):
        return 2, "explicit_regex"

    # 2. Structural & Analytical Heuristics
    has_multiple_parts = len(re.findall(r'\([a-d|i-v]+\)', lowered)) >= 2 or ("(a)" in lowered and "(b)" in lowered)
    has_analytical_keywords = any(kw in lowered for kw in [
        "explain the working", "derive", "draw the", "architecture",
        "calculate", "master theorem", "time complexity", "reliability",
        "prove that", "write short notes on any two", "fault tolerance"
    ])

    if has_analytical_keywords or has_multiple_parts:
        m = 5 if wlen > 35 else 3
        return m, "analytical_keyword"

    # 3. Calibrated Word-Count Fallback
    if wlen > 60:
        return 5, "word_count_fallback"
    elif wlen > 30:
        return 3, "word_count_fallback"
    else:
        return 2, "word_count_fallback"

def is_question_chunk(payload: Dict[str, Any]) -> bool:
    """Checks if a vector point payload belongs to a Question Bank or PYQ document."""
    chunk_type = str(payload.get("chunk_type") or payload.get("category_key") or "").lower()
    fn = str(payload.get("source_filename") or "").lower()
    text = str(payload.get("text") or payload.get("page_content") or "").lower()

    if chunk_type in ["question_bank", "pyq"]:
        return True
    if any(k in fn for k in ["question", "qbank", "pyq", "assignment", "solution"]):
        return True
    if re.search(r'^\s*(?:q\d+|question\s*\d+|\d+\.\s*\*\*)', text):
        return True
    return False

def run_marks_migration(dry_run: bool = True):
    print("=== EduMind Qdrant Question Bank & PYQ Marks Tagging Migration (2 / 3 / 5 Marks) ===")
    print(f"Mode: {'DRY-RUN (Preview Only)' if dry_run else 'PRODUCTION WRITE'}\n")

    client = get_qdrant_client()

    all_collections = []
    try:
        cols_res = client.get_collections()
        all_collections = [c.name for c in cols_res.collections]
    except Exception as e:
        logger.warning(f"Error fetching Qdrant collections: {e}")

    print(f"Auditing {len(all_collections)} Qdrant Cloud subject collections (Full Offset Pagination)...")

    rule_sources = {"explicit_regex": 0, "analytical_keyword": 0, "word_count_fallback": 0}
    stats = {2: 0, 3: 0, 5: 0}
    sample_audit = []
    total_evaluated = 0

    bsm_stats = {2: 0, 3: 0, 5: 0, "total": 0}

    for col in all_collections:
        offset = None
        while True:
            try:
                points, next_offset = client.scroll(collection_name=col, limit=250, offset=offset, with_payload=True)
                for pt in points:
                    payload = pt.payload or {}
                    if not is_question_chunk(payload):
                        continue

                    text = payload.get("text") or payload.get("page_content") or ""
                    if not text or len(text.strip()) < 15:
                        continue

                    inferred_mark, source = infer_question_marks_with_source(text)
                    rule_sources[source] += 1
                    stats[inferred_mark] += 1
                    total_evaluated += 1

                    if col == "BSM-104":
                        bsm_stats["total"] += 1
                        bsm_stats[inferred_mark] += 1

                    if len(sample_audit) < 25:
                        fn = payload.get("source_filename") or "Question Bank Chunk"
                        clean_snip = text[:80].replace("\n", " ").strip()
                        sample_audit.append({
                            "point_id": str(pt.id),
                            "subject": col,
                            "mark": inferred_mark,
                            "source": source,
                            "filename": str(fn)[:28],
                            "snippet": clean_snip
                        })
                if not next_offset:
                    break
                offset = next_offset
            except Exception as err:
                logger.warning(f"Error processing collection {col}: {err}")
                break

    print("\n--- RULE MATCHING BREAKDOWN ---")
    ex_cnt = rule_sources["explicit_regex"]
    an_cnt = rule_sources["analytical_keyword"]
    fb_cnt = rule_sources["word_count_fallback"]
    print(f"  - Explicit Mark-Stamp Regex:    {ex_cnt} ({ex_cnt/total_evaluated*100:.1f}%)")
    print(f"  - Analytical/Structural Rules:   {an_cnt} ({an_cnt/total_evaluated*100:.1f}%)")
    print(f"  - Calibrated Length Fallback:   {fb_cnt} ({fb_cnt/total_evaluated*100:.1f}%)")

    print("\n--- INFERRED MARKS DISTRIBUTION SUMMARY (PURE QUESTION BANK CORPUS) ---")
    print(f"  - 2-Mark Questions (Basic/Short):     {stats[2]} ({stats[2]/total_evaluated*100:.1f}%)")
    print(f"  - 3-Mark Questions (Conceptual):      {stats[3]} ({stats[3]/total_evaluated*100:.1f}%)")
    print(f"  - 5-Mark Questions (Analytical/Long):  {stats[5]} ({stats[5]/total_evaluated*100:.1f}%)")
    print(f"Total Evaluated Discrete Question Chunks: {total_evaluated}")

    print(f"\n--- BSM-104 SPECIFIC BREAKDOWN (Total {bsm_stats['total']} Discrete Question Chunks) ---")
    print(f"  - 2-Mark: {bsm_stats[2]} | 3-Mark: {bsm_stats[3]} | 5-Mark: {bsm_stats[5]}")

    print("\n--- SAMPLE AUDIT TABLE (Human Review Sample) ---")
    print(f"{'Subject':<10} | {'Marks':<5} | {'Rule Source':<20} | {'Question Snippet'}")
    print("-" * 105)
    for sample in sample_audit[:25]:
        clean_snippet = sample['snippet'].encode('ascii', 'ignore').decode('ascii')
        print(f"{sample['subject']:<10} | {sample['mark']:<5} | {sample['source']:<20} | {clean_snippet}")
    print("-" * 105)

    if dry_run:
        print("\n[DRY RUN COMPLETE] Zero payload mutations executed. Review distribution table above.")
    else:
        print("\n[PRODUCTION WRITE MODE] Updating Qdrant Cloud payload 'marks' field with full pagination...")
        updated_count = 0
        for col in all_collections:
            offset = None
            while True:
                try:
                    points, next_offset = client.scroll(collection_name=col, limit=250, offset=offset, with_payload=True)
                    for pt in points:
                        payload = pt.payload or {}
                        if not is_question_chunk(payload):
                            continue
                        text = payload.get("text") or payload.get("page_content") or ""
                        if not text or len(text.strip()) < 15:
                            continue

                        mark, _ = infer_question_marks_with_source(text)
                        client.set_payload(
                            collection_name=col,
                            payload={"marks": mark},
                            points=[pt.id]
                        )
                        updated_count += 1
                    if not next_offset:
                        break
                    offset = next_offset
                except Exception as e:
                    logger.warning(f"Error updating payload for collection {col}: {e}")
                    break
        print(f"Production update complete! Updated {updated_count} vector point payloads in Qdrant.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate Marks Tagging (2/3/5 marks)")
    parser.add_argument("--apply", action="store_true", help="Apply changes to Qdrant Cloud (default is dry-run)")
    args = parser.parse_args()

    run_marks_migration(dry_run=not args.apply)
