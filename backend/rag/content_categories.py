"""
Content Category Registry & Schema Versioning.
Defines every ingestible content category as a versioned configuration entry.
"""

from typing import Dict, Any, List

SCHEMA_VERSION = 1

CONTENT_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "notes": {
        "chunk_type": "note",
        "input_type": "file_upload",
        "accepted_formats": [".pdf", ".md"],
        "chunker": "recursive_or_tagged",
        "requires_unit": False,
        "description": "Study notes and textbook materials (.pdf, .md)"
    },
    "pyq": {
        "chunk_type": "pyq",
        "input_type": "file_upload",
        "accepted_formats": [".pdf"],
        "chunker": "recursive_or_tagged",
        "requires_unit": False,
        "description": "Previous Year Question papers (.pdf)"
    },
    "question_bank": {
        "chunk_type": "question_bank",
        "input_type": "file_upload",
        "accepted_formats": [".md"],
        "chunker": "tagged_question_boundary",
        "requires_unit": True,
        "description": "Tagged question banks with [Unit | Topic | Type | Difficulty] headers (.md)"
    },
    "transcript": {
        "chunk_type": "transcript",
        "input_type": "file_upload",
        "accepted_formats": [".txt"],
        "chunker": "token_window",
        "requires_unit": False,
        "description": "Video/Lecture transcripts (.txt)"
    }
}

def get_category_config(category_key: str) -> Dict[str, Any]:
    """Retrieve category config or raise explicit ValueError if invalid."""
    if not category_key or not isinstance(category_key, str):
        raise ValueError(f"Category key must be a non-empty string. Received: {category_key}")
    
    key = category_key.strip().lower()
    if key not in CONTENT_CATEGORIES:
        valid_keys = list(CONTENT_CATEGORIES.keys())
        raise ValueError(f"Unknown content category '{category_key}'. Supported categories: {valid_keys}")
    
    config = dict(CONTENT_CATEGORIES[key])
    config["category_key"] = key
    config["schema_version"] = SCHEMA_VERSION
    return config
