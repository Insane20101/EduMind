import os
import sys
import json
import re
import argparse
from typing import List, Dict, Any

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.vector_store import get_qdrant_client
from rag.retriever import retrieve
from rag.prompts import HINT_GENERATOR_PROMPT, DIAGRAM_EXPLAINER_PROMPT, CRAM_SUMMARY_PROMPT
from utils.logger import get_logger
from pymongo import MongoClient

logger = get_logger(__name__)

# Quality Gate 1: Hard Refusal Code Gate
def check_refusal_gate(response_text: str) -> bool:
    """Returns True if the response contains a refusal string or context failure."""
    if not response_text or not response_text.strip():
        return True
    refusal_keywords = [
        "REFUSAL:",
        "insufficient grounded course material",
        "insufficient context",
        "does not contain enough information"
    ]
    lowered = response_text.lower()
    for kw in refusal_keywords:
        if kw.lower() in lowered:
            return True
    return False

# Quality Gate 2: Citation Validation Gate
def validate_citations_gate(candidate_citations: List[str], valid_chunk_ids: List[str]) -> List[str]:
    """Filters candidate citations so only IDs that truly exist in retrieved Qdrant chunks survive."""
    if not candidate_citations or not valid_chunk_ids:
        return []
    valid_set = set(valid_chunk_ids)
    return [cid for cid in candidate_citations if cid in valid_set]

# Quality Gate 3: Headless Mermaid Syntax Gate
def check_mermaid_syntax_gate(mermaid_code: str) -> bool:
    """Validates basic Mermaid.js syntax structure before admin review insertion."""
    if not mermaid_code or not isinstance(mermaid_code, str):
        return False
    code = mermaid_code.strip()
    valid_headers = ["graph", "flowchart", "sequencediagram", "statediagram", "classdiagram", "gantt", "erdiagram"]
    has_valid_header = any(code.lower().startswith(h) for h in valid_headers)
    if not has_valid_header:
        return False
    
    # Bracket & Quote Balance Check
    open_brackets = code.count("[") + code.count("(") + code.count("{")
    close_brackets = code.count("]") + code.count(")") + code.count("}")
    if abs(open_brackets - close_brackets) > 2:  # allow minor tolerance for nested labels
        return False
    
    quote_count = code.count('"')
    if quote_count % 2 != 0:  # Unmatched double quotes
        return False

    return True

def get_mongo_db():
    mongo_uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI", "mongodb://localhost:27017/edumind")
    client = MongoClient(mongo_uri)
    return client["edumind"]


def synthesize_unit_assets(subject_id: str, unit: str, asset_type: str = "all", dry_run: bool = False):
    subject_id = subject_id.strip().upper()
    print(f"--- Synthesizing Assets for Subject {subject_id} {unit} ---")
    
    # 1. Retrieve RAG chunks for topic context
    chunks = retrieve(subject_id=subject_id, unit_id=unit, query="core algorithms formulas summary key topics", top_k=6)
    if not chunks:
        print(f"No vector chunks retrieved for {subject_id} {unit}. Skipping synthesis.")
        return

    context_str = "\n\n".join([f"[Chunk ID: {c['chunk_id']}]\n{c['text']}" for c in chunks])
    valid_chunk_ids = [c['chunk_id'] for c in chunks]

    # Import OpenAI lazily
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY missing.")
        return
    client = OpenAI(api_key=api_key)

    types_to_generate = ["hint", "diagram", "cram"] if asset_type == "all" else [asset_type]

    db = get_mongo_db() if not dry_run else None

    for a_type in types_to_generate:
        print(f"\nProcessing asset_type: {a_type}...")
        prompt_tmpl = HINT_GENERATOR_PROMPT if a_type == "hint" else (DIAGRAM_EXPLAINER_PROMPT if a_type == "diagram" else CRAM_SUMMARY_PROMPT)
        formatted_prompt = prompt_tmpl.format(context=context_str, topic=f"{subject_id} {unit} core concepts")

        try:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": formatted_prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            raw_text = res.choices[0].message.content or ""

            # Gate 1: Hard Refusal Gate Check
            if check_refusal_gate(raw_text):
                print(f"  [Refusal Gate Triggered] LLM signaled insufficient context for {a_type}. Record dropped.")
                continue

            parsed = json.loads(raw_text)

            # Gate 2: Citation Validation Gate
            raw_citations = parsed.get("citations", [])
            valid_citations = validate_citations_gate(raw_citations, valid_chunk_ids)
            parsed["citations"] = valid_citations
            print(f"  [Citation Gate] Validated {len(valid_citations)} / {len(raw_citations)} citations.")

            # Gate 3: Headless Mermaid Syntax Gate
            if a_type == "diagram":
                m_code = parsed.get("mermaid_code", "")
                if not check_mermaid_syntax_gate(m_code):
                    print("  [Mermaid Syntax Gate Failed] Malformed Mermaid syntax detected. Record dropped.")
                    continue
                print("  [Mermaid Syntax Gate Passed] Mermaid code validated.")

            asset_doc = {
                "subject_id": subject_id,
                "unit": unit,
                "asset_type": a_type,
                "topic": parsed.get("topic", f"{subject_id} {unit}"),
                "content": parsed,
                "citations": valid_citations,
                "status": "pending_review",
                "created_at": "2026-09-11T13:30:00Z"
            }

            if dry_run:
                print("  [Dry Run] Asset ready for pending_review:")
                print(json.dumps(asset_doc, indent=2))
            else:
                res_db = db.synthesized_assets.insert_one(asset_doc)
                print(f"  [Saved to MongoDB] Inserted ID: {res_db.inserted_id} with status='pending_review'")

        except Exception as err:
            print(f"  [Error] Failed synthesizing {a_type}: {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthesize Content Assets for EduMind")
    parser.add_argument("--subject", type=str, required=True, help="Subject ID (e.g., BCS-401)")
    parser.add_argument("--unit", type=str, default="Unit I", help="Unit ID")
    parser.add_argument("--type", type=str, default="all", choices=["all", "hint", "diagram", "cram"])
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing to MongoDB")
    args = parser.parse_args()

    synthesize_unit_assets(subject_id=args.subject, unit=args.unit, asset_type=args.type, dry_run=args.dry_run)
