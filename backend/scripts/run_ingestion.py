import os
import sys
import glob
import hashlib
import argparse

# Add backend dir to python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rag.chunker import chunk_transcript, chunk_markdown
from rag.embedder import generate_embeddings
from rag.vector_store import upsert_chunks

BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "CSE")
HASH_TRACKER_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ingestion_hashes.txt")

def load_hashes():
    hashes = {}
    if os.path.exists(HASH_TRACKER_FILE):
        with open(HASH_TRACKER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        # filepath -> (hash, model)
                        model = parts[2] if len(parts) >= 3 else "unknown"
                        hashes[parts[0]] = (parts[1], model)
    return hashes

def save_hash(filepath, file_hash, model="text-embedding-3-small"):
    os.makedirs(os.path.dirname(HASH_TRACKER_FILE), exist_ok=True)
    with open(HASH_TRACKER_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{filepath}|{file_hash}|{model}\n")

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print chunks without embedding/storing")
    parser.add_argument("--force", action="store_true", help="Force re-ingestion ignoring saved hashes")
    parser.add_argument("--semester", type=str, help="Filter by semester (e.g., Semester1)")
    parser.add_argument("--subject", type=str, help="Filter by subject id (e.g., BSM-104)")
    args = parser.parse_args()

    file_hashes = {} if args.force else load_hashes()
    
    if args.semester:
        search_path = os.path.join(BASE_DATA_DIR, args.semester, "*")
    else:
        search_path = os.path.join(BASE_DATA_DIR, "*", "*")
        
    subject_dirs = glob.glob(search_path)
    
    summary = []
    
    for subj_dir in subject_dirs:
        if not os.path.isdir(subj_dir):
            continue
            
        subject_name_full = os.path.basename(subj_dir)
        subject_id = subject_name_full.split(' ')[0]
        semester = os.path.basename(os.path.dirname(subj_dir))
        
        if args.subject and subject_id != args.subject:
            continue
        
        print(f"\nProcessing {subject_id} ({semester})...")
        
        files_processed = 0
        chunks_created = 0
        skipped = 0
        failed = 0
        
        # Process files
        all_files = []
        all_files.extend(glob.glob(os.path.join(subj_dir, "transcripts", "*.txt")))
        all_files.extend(glob.glob(os.path.join(subj_dir, "*.md")))
        
        for filepath in all_files:
            if "syllabus.md" in filepath:
                continue 
                
            abs_path = os.path.abspath(filepath)
            try:
                current_hash = get_file_hash(abs_path)
            except Exception as e:
                print(f"  [ERROR] Cannot read {abs_path}: {e}")
                failed += 1
                continue
            
            if not args.dry_run and abs_path in file_hashes:
                saved_hash, saved_model = file_hashes[abs_path]
                if saved_hash == current_hash and saved_model == "text-embedding-3-small":
                    skipped += 1
                    continue
                
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"  [ERROR] Cannot open {abs_path}: {e}")
                failed += 1
                continue
                
            filename = os.path.basename(abs_path)
            
            if filename.endswith('.txt'):
                chunks = chunk_transcript(content, filename, subject_id, semester)
                source_type = "transcript"
            elif filename.endswith('.md'):
                source_type = "question_bank" if "Question_Bank" in filename else "solution"
                chunks = chunk_markdown(content, filename, subject_id, semester, source_type)
            
            if args.dry_run:
                print(f"  [DRY RUN] {filename}: {len(chunks)} chunks")
                if len(chunks) > 0 and chunks_created == 0:
                    print(f"    Sample Metadata: {chunks[0]['metadata']}")
                    safe_text = chunks[0]['text'][:150].encode('ascii', 'replace').decode('ascii')
                    print(f"    Sample Text: {safe_text}...")
            else:
                if chunks:
                    texts = [c['text'] for c in chunks]
                    try:
                        embeddings = generate_embeddings(texts)
                        for i, c in enumerate(chunks):
                            c['embedding'] = embeddings[i]
                        upsert_chunks(chunks)
                        
                        save_hash(abs_path, current_hash)
                        file_hashes[abs_path] = (current_hash, "text-embedding-3-small")
                    except Exception as e:
                        print(f"  [ERROR] Failed processing {filename}: {e}")
                        failed += 1
                        continue
                        
            files_processed += 1
            chunks_created += len(chunks)
            
        summary.append({
            "subject": subject_id,
            "processed": files_processed,
            "skipped": skipped,
            "failed": failed,
            "chunks": chunks_created
        })
        
    print("\n=== Ingestion Summary ===")
    print(f"{'Subject':<15} | {'Processed':<10} | {'Skipped':<10} | {'Failed':<10} | {'Chunks'}")
    print("-" * 65)
    for s in summary:
        print(f"{s['subject']:<15} | {s['processed']:<10} | {s['skipped']:<10} | {s['failed']:<10} | {s['chunks']}")

if __name__ == "__main__":
    main()
