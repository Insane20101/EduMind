import sys
import os
import glob
import json
import hashlib

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rag.chunker import chunk_markdown
from rag.embedder import generate_embeddings
from rag.vector_store import get_chroma_client
from dotenv import load_dotenv

load_dotenv()

def calculate_file_hash(filepath, model_name):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    hasher.update(model_name.encode('utf-8'))
    return hasher.hexdigest()

def get_ingestion_hashes(hash_file):
    if not os.path.exists(hash_file):
        return {}
    with open(hash_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_ingestion_hashes(hash_file, hashes):
    with open(hash_file, 'w', encoding='utf-8') as f:
        json.dump(hashes, f, indent=4)

def reingest_solutions():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    sol_files = glob.glob(os.path.join(base_dir, '**', '*Solutions.md'), recursive=True)
    
    chroma_client = get_chroma_client()
    hash_file = os.path.join(os.path.dirname(__file__), '..', 'ingestion_hashes.txt')
    hashes = get_ingestion_hashes(hash_file)
    
    model_name = "text-embedding-3-small"
    
    total_deleted = 0
    total_inserted = 0

    for sol_file in sol_files:
        filename = os.path.basename(sol_file)
        
        # Extract subject_id from directory or filename (e.g., BCS-201_Solutions.md)
        subject_id = filename.split('_')[0]
        
        # We need to find semester. It's in the path: data/CSE/SemesterX/...
        parts = sol_file.split(os.sep)
        semester = "Unknown"
        for p in parts:
            if p.startswith("Semester"):
                semester = p.replace("Semester", "")
                break
                
        print(f"Processing {filename} (Subject: {subject_id})")
        
        # 2. Delete ONLY solutions chunks for this file
        try:
            collection = chroma_client.get_collection(name=subject_id)
            
            # Fetch to count before deletion (for logging)
            existing = collection.get(where={"source_file": filename})
            count_to_delete = len(existing["ids"]) if existing["ids"] else 0
            
            if count_to_delete > 0:
                collection.delete(where={"source_file": filename})
                print(f"  -> Deleted {count_to_delete} old chunks.")
                total_deleted += count_to_delete
            else:
                print(f"  -> No existing chunks found to delete.")
                
        except Exception as e:
            # Collection might not exist if it was completely skipped
            print(f"  -> Collection {subject_id} not found or error: {e}")
            continue
            
        # 3. Re-chunk
        with open(sol_file, 'r', encoding='utf-8') as f:
            text = f.read()
            
        chunks = chunk_markdown(text, filename, subject_id, semester, "solutions")
        print(f"  -> Generated {len(chunks)} new chunks.")
        
        if not chunks:
            continue
            
        # 4. Re-embed
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        embeddings = generate_embeddings(texts)
        
        # 5. Re-insert
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )
        print(f"  -> Inserted {len(chunks)} new chunks.")
        total_inserted += len(chunks)
        
        # 6. Update hash (so future runs don't reingest)
        # We just recompute and save. It's the same content, but we need to ensure it's in the file.
        new_hash = calculate_file_hash(sol_file, model_name)
        # Store using the relative path from data/ as key (matching ingest_corpus.py logic)
        rel_path = os.path.relpath(sol_file, base_dir).replace('\\', '/')
        hashes[rel_path] = new_hash
        
    save_ingestion_hashes(hash_file, hashes)
    print(f"\nDone! Deleted {total_deleted} old chunks, Inserted {total_inserted} new chunks.")

if __name__ == "__main__":
    reingest_solutions()
