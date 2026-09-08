import os
import uuid
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from .embedder import get_embeddings_model, generate_embeddings

logger = logging.getLogger(__name__)

def get_qdrant_client() -> QdrantClient:
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    if not url or not api_key:
        raise RuntimeError(
            "FATAL: QDRANT_URL and QDRANT_API_KEY environment variables are strictly required for vector storage. "
            "Please configure them in backend/.env and Render environment settings."
        )
    return QdrantClient(url=url, api_key=api_key, timeout=30.0)

def ensure_payload_indexes(client: QdrantClient, collection_name: str):
    """
    Ensures keyword payload indexes exist on critical filter fields for a Qdrant collection.
    """
    for field in ("unit", "source_filename", "resource_id", "source_file"):
        try:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema=models.PayloadSchemaType.KEYWORD
            )
        except Exception:
            pass

def get_or_create_subject_collection(subject_id: str) -> str:
    """
    Creates or retrieves a Qdrant Cloud collection strictly tied to one subject_id.
    Vector dimensions: 1536 (OpenAI text-embedding-3-small), COSINE distance.
    Creates keyword payload indexes for metadata filtering.
    """
    client = get_qdrant_client()
    collection_name = subject_id.strip().upper()
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
        )
        ensure_payload_indexes(client, collection_name)
        logger.info(f"Created Qdrant Cloud collection '{collection_name}' with payload indexes.")
    else:
        # Ensure indexes exist on pre-existing collections
        ensure_payload_indexes(client, collection_name)
    return collection_name

def upsert_chunks(chunks: list[dict]):
    """
    chunks is a list of dicts: {"text": str, "metadata": dict, "embedding": list[float] (optional)}
    Writes to a Qdrant Cloud collection PER SUBJECT based on chunk.metadata.subject_id.
    """
    if not chunks:
        return
        
    client = get_qdrant_client()
    subject_chunks = {}
    for chunk in chunks:
        subject_id = chunk['metadata'].get('subject_id')
        if not subject_id:
            continue
        subj_clean = subject_id.strip().upper()
        if subj_clean not in subject_chunks:
            subject_chunks[subj_clean] = []
        subject_chunks[subj_clean].append(chunk)

    for subject_id, s_chunks in subject_chunks.items():
        collection_name = get_or_create_subject_collection(subject_id)
        
        # Generate missing OpenAI embeddings in batches
        texts_to_embed = [c['text'] for c in s_chunks if 'embedding' not in c or not c['embedding']]
        if texts_to_embed:
            new_embeddings = generate_embeddings(texts_to_embed)
            embed_idx = 0
            for c in s_chunks:
                if 'embedding' not in c or not c['embedding']:
                    c['embedding'] = new_embeddings[embed_idx]
                    embed_idx += 1

        points = []
        for c in s_chunks:
            point_id = str(uuid.uuid4())
            payload = dict(c['metadata'])
            payload['text'] = c['text']
            payload['page_content'] = c['text']
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=c['embedding'],
                    payload=payload
                )
            )

        # Batch upsert points to Qdrant Cloud
        client.upsert(collection_name=collection_name, points=points)
        logger.info(f"Upserted {len(points)} points into Qdrant Cloud collection '{collection_name}'.")

def delete_resource_chunks(subject_id: str, resource_id: str = None, source_filename: str = None) -> int:
    """
    Deletes all vector points in Qdrant Cloud belonging to subject_id matched by resource_id or source_filename.
    Returns the count of deleted point IDs.
    """
    if not subject_id:
        return 0

    client = get_qdrant_client()
    collection_name = subject_id.strip().upper()

    if not client.collection_exists(collection_name):
        return 0

    # Ensure payload indexes exist
    for field in ("resource_id", "source_filename", "source_file"):
        try:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=field,
                field_schema=models.PayloadSchemaType.KEYWORD
            )
        except Exception:
            pass

    target_point_ids = set()

    # 1. Attempt indexed scroll filter
    for key, val in [("resource_id", resource_id), ("source_filename", source_filename), ("source_file", source_filename)]:
        if not val:
            continue
        scroll_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=val)
                )
            ]
        )
        try:
            points, _ = client.scroll(
                collection_name=collection_name,
                scroll_filter=scroll_filter,
                limit=500,
                with_payload=True
            )
            if points:
                for p in points:
                    target_point_ids.add(p.id)
        except Exception as e:
            logger.warning(f"Error scrolling Qdrant points for {key}={val}: {e}")

    # 2. Fallback: Python-level payload match scan if target_point_ids is empty
    if not target_point_ids:
        try:
            points, _ = client.scroll(
                collection_name=collection_name,
                limit=500,
                with_payload=True
            )
            for p in points:
                payload = p.payload or {}
                if (resource_id and payload.get("resource_id") == resource_id) or \
                   (source_filename and (payload.get("source_filename") == source_filename or payload.get("source_file") == source_filename)):
                    target_point_ids.add(p.id)
        except Exception as scan_err:
            logger.warning(f"Fallback scan notice for {collection_name}: {scan_err}")

    if target_point_ids:
        client.delete(
            collection_name=collection_name,
            points_selector=models.PointIdsList(points=list(target_point_ids))
        )
        logger.info(f"Deleted {len(target_point_ids)} points from Qdrant Cloud collection '{collection_name}'.")
        return len(target_point_ids)

    return 0

