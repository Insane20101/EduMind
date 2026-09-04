import os
from langchain_chroma import Chroma
from .embedder import get_embeddings_model

def get_chroma_client():
    import chromadb
    CHROMA_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_data")
    return chromadb.PersistentClient(path=CHROMA_DATA_DIR)

def get_or_create_subject_collection(subject_id: str):
    """
    Creates or retrieves a ChromaDB collection strictly tied to one subject_id.
    """
    client = get_chroma_client()
    return client.get_or_create_collection(name=subject_id)

def get_langchain_vectorstore(subject_id: str):
    """
    Returns a LangChain Chroma vectorstore instance configured for a specific subject collection.
    """
    CHROMA_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_data")
    return Chroma(
        collection_name=subject_id,
        embedding_function=get_embeddings_model(),
        persist_directory=CHROMA_DATA_DIR
    )

def upsert_chunks(chunks: list[dict]):
    """
    chunks is a list of dicts: {"text": str, "metadata": dict, "embedding": list[float]}
    Writes to a collection PER SUBJECT based on chunk.metadata.subject_id.
    """
    if not chunks:
        return
        
    # Group chunks by subject_id
    subject_chunks = {}
    for chunk in chunks:
        subject_id = chunk['metadata'].get('subject_id')
        if not subject_id:
            continue
        if subject_id not in subject_chunks:
            subject_chunks[subject_id] = []
        subject_chunks[subject_id].append(chunk)
        
    for subject_id, s_chunks in subject_chunks.items():
        collection = get_or_create_subject_collection(subject_id)
        
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        for chunk in s_chunks:
            chunk_id = f"{chunk['metadata']['source_file']}_{chunk['metadata']['chunk_index']}"
            ids.append(chunk_id)
            documents.append(chunk['text'])
            metadatas.append(chunk['metadata'])
            if 'embedding' in chunk:
                embeddings.append(chunk['embedding'])
                
        if embeddings:
            collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        else:
            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

