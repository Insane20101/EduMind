import os
import time
import glob
import sys

# Add backend dir to python path
sys.path.append(os.path.dirname(__file__))

from rag.generator import generate_with_retry

# Base data directory relative to backend folder
BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "CSE")
TRACKER_FILE = os.path.join(os.path.dirname(__file__), "cleaned_log.txt")

SYSTEM_PROMPT = """You are a transcript editor. Clean and structure the following lecture transcript chunk. Fix punctuation and capitalization, remove filler words (um, uh, so basically, okay so, like), and break it into clear paragraphs by topic. 
Do NOT summarize, shorten, or remove any technical content — preserve every concept, example, and explanation as-is. Only clean the language and structure."""

MAX_CHUNK_SIZE = 15000

def chunk_text(text, max_size):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_size
        if end < len(text):
            last_period = text.rfind('.', start, end)
            last_space = text.rfind(' ', start, end)
            if last_period != -1 and last_period > start + max_size * 0.8:
                end = last_period + 1
            elif last_space != -1 and last_space > start + max_size * 0.8:
                end = last_space + 1
        chunks.append(text[start:end])
        start = end
    return chunks

def load_cleaned_files():
    if not os.path.exists(TRACKER_FILE):
        return set()
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def mark_as_cleaned(filepath):
    with open(TRACKER_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{filepath}\n")

def main():
    print("Starting transcript cleaning process with Gemini (google-genai)...")

    total_files = 0
    cleaned_successfully = 0
    skipped_files = 0
    failed_files = 0
    
    search_pattern = os.path.join(BASE_DATA_DIR, "**", "transcripts", "*.txt")
    transcript_files = glob.glob(search_pattern, recursive=True)
    
    total_files = len(transcript_files)
    print(f"Found {total_files} transcript files.")
    
    cleaned_tracker = load_cleaned_files()

    for filepath in transcript_files:
        abs_filepath = os.path.abspath(filepath)
        
        if abs_filepath in cleaned_tracker:
            print(f"Skipping (already in cleaned log): {os.path.basename(abs_filepath)}")
            skipped_files += 1
            continue
            
        print(f"Processing (in-place): {os.path.basename(abs_filepath)}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_text = f.read()
        except Exception as e:
            print(f"  Error reading file: {e}")
            failed_files += 1
            continue
            
        if not raw_text.strip():
            print("  Skipping: File is empty.")
            skipped_files += 1
            continue

        chunks = chunk_text(raw_text, MAX_CHUNK_SIZE)
        cleaned_text_parts = []
        success = True
        
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                print(f"  Cleaning chunk {i+1}/{len(chunks)}...")
                
            prompt = SYSTEM_PROMPT + "\n\n" + chunk
            response_text = generate_with_retry(prompt, is_json=False, model='gemini-3.6-flash')
            
            if response_text:
                cleaned_text_parts.append(response_text)
                chunk_success = True
            
            if not chunk_success:
                success = False
                break
                
            # Wait a few seconds to avoid hitting the 15 RPM limit
            time.sleep(4.5)
            
        if success and cleaned_text_parts:
            final_text = "\n\n".join(cleaned_text_parts)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(final_text)
                
                mark_as_cleaned(abs_filepath)
                cleaned_tracker.add(abs_filepath)
                
                cleaned_successfully += 1
                print(f"  Successfully overwritten {os.path.basename(abs_filepath)}")
            except Exception as e:
                print(f"  Error writing cleaned file: {e}")
                failed_files += 1
        else:
            print(f"  Failed to clean {os.path.basename(abs_filepath)}")
            failed_files += 1
            
    print("\n--- Summary ---")
    print(f"Total files found: {total_files}")
    print(f"Cleaned successfully: {cleaned_successfully}")
    print(f"Skipped (already done): {skipped_files}")
    print(f"Failed: {failed_files}")

if __name__ == "__main__":
    main()
