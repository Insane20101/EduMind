from typing import Optional, List, Dict, Any
from qdrant_client.http import models
from .vector_store import get_qdrant_client
from .embedder import generate_embeddings

def retrieve(subject_id: str, unit_id: Optional[str], query: str, top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Embeds query using OpenAI text-embedding-3-small and retrieves matching document chunks
    from the strictly subject_id-scoped Qdrant Cloud collection.
    """
    if not subject_id or not query or not query.strip():
        return []

    subject_id = subject_id.strip().upper()
    client = get_qdrant_client()

    if not client.collection_exists(subject_id):
        return []

    try:
        # 1. Generate 1536-dimensional query embedding via OpenAI
        query_embeddings = generate_embeddings([query])
        if not query_embeddings or not query_embeddings[0]:
            return []
        query_vector = query_embeddings[0]

        # 2. Metadata Filter: Unit scoping if specified
        query_filter = None
        if unit_id and unit_id.strip() and unit_id.strip().lower() != "all":
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="unit",
                        match=models.MatchValue(value=unit_id.strip())
                    )
                ]
            )

        # 3. Vector Similarity Search in Qdrant Cloud
        search_result = client.query_points(
            collection_name=subject_id,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k
        )

        points = search_result.points if hasattr(search_result, "points") else search_result

        chunks = []
        for point in points:
            payload = point.payload or {}
            text = payload.get("text") or payload.get("page_content") or ""
            # Filter out scanned PDF placeholder chunks from RAG grounding context
            is_ph = payload.get("is_placeholder", False)
            if is_ph or "is available for inline viewing and download" in text or "Document placeholder metadata" in text:
                continue
                
            chunk_id = payload.get("chunk_id") or str(point.id)
            chunks.append({
                "chunk_id": chunk_id,
                "similarity": float(point.score),
                "text": text,
                "metadata": payload
            })

        chunks.sort(key=lambda x: x["similarity"], reverse=True)
        return chunks
    except RuntimeError as re_err:
        logger.error(f"FATAL Qdrant configuration error: {re_err}")
        raise re_err
    except Exception as e:
        logger.warning(f"Qdrant retrieval notice for '{subject_id}': {e}")
        return []

def retrieve_context(query: str, subject_id: str, unit: Optional[str] = None, top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Alias wrapper for retrieve() to support kwarg parameter ordering (query, subject_id, unit, top_k).
    """
    return retrieve(subject_id=subject_id, unit_id=unit, query=query, top_k=top_k)

def query_vector_store(query: str, subject_id: str, top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Alias wrapper for general query vector store calls without unit filtering.
    """
    return retrieve(subject_id=subject_id, unit_id=None, query=query, top_k=top_k)

