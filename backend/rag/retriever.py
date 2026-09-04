from typing import Optional, List, Dict, Any
from .vector_store import get_chroma_client, get_langchain_vectorstore

def retrieve(subject_id: str, unit_id: Optional[str], query: str, top_k: int = 6) -> List[Dict[str, Any]]:
    """
    Embeds query and retrieves matching document chunks from the strictly subject_id-scoped Chroma collection using LangChain.
    """
    client = get_chroma_client()
    try:
        collection = client.get_collection(name=subject_id)
        if collection.count() == 0:
            return []
    except Exception:
        return []

    try:
        vector_store = get_langchain_vectorstore(subject_id)
        where = {"unit": unit_id} if unit_id else None
        
        results_with_score = vector_store.similarity_search_with_score(
            query=query,
            k=top_k,
            filter=where
        )
    except Exception as e:
        print(f"  LangChain retrieval error: {e}")
        return []

    chunks = []
    for doc, dist in results_with_score:
        sim = 1.0 - (dist / 2.0)
        chunk_id = doc.metadata.get("chunk_id") or f"{doc.metadata.get('source_file')}_{doc.metadata.get('chunk_index')}"
        chunks.append({
            "chunk_id": chunk_id,
            "similarity": sim,
            "text": doc.page_content,
            "metadata": doc.metadata
        })
        
    chunks.sort(key=lambda x: x["similarity"], reverse=True)
    return chunks

