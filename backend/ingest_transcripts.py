# pip install yt-dlp youtube-transcript-api
import asyncio
import os
import time
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from database import db

# Base data directory relative to backend folder
BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "CSE")

async def main():
    print("Starting transcript ingestion...")
    
    subjects_processed = 0
    transcripts_saved = 0
    transcripts_skipped = 0
    
    try:
        # Fetch all verified subjects
        cursor = db.subjects.find({"status": "verified"})
        subjects = []
        async for doc in cursor:
            subjects.append(doc)
    except Exception as e:
        print(f"Error fetching subjects from database: {e}")
        return

    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
    }
    
    for subject in subjects:
        semester = subject.get("semester")
        code = subject.get("code")
        name = subject.get("name", "")
        playlists = subject.get("playlists", [])
        
        if not semester or not code:
            continue
            
        # Build the output folder path
        safe_name = name.replace(" ", "_")
        folder_name = f"{code}_{safe_name}"
        target_dir = os.path.join(BASE_DATA_DIR, semester, folder_name, "transcripts")
        
        # Ensure the directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        print(f"Processing subject: {code} - {name} ({len(playlists)} playlists)")
        
        video_index = 1
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for playlist_url in playlists:
                try:
                    info = ydl.extract_info(playlist_url, download=False)
                    if not info or 'entries' not in info:
                        print(f"Warning: Could not extract videos from {playlist_url}")
                        continue
                        
                    entries = info['entries']
                    for entry in entries:
                        if not entry:
                            continue
                        
                        video_id = entry.get('id')
                        if not video_id:
                            continue
                            
                        # Fetch transcript
                        try:
                            transcript_segments = YouTubeTranscriptApi.get_transcript(video_id)
                            transcript_text = " ".join([seg['text'] for seg in transcript_segments])
                            
                            filename = f"video_{video_index}_{video_id}.txt"
                            filepath = os.path.join(target_dir, filename)
                            
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(transcript_text)
                                
                            transcripts_saved += 1
                            print(f"  Saved transcript for video {video_id} -> {filename}")
                            video_index += 1
                            
                        except (TranscriptsDisabled, NoTranscriptFound):
                            print(f"  Skipped video {video_id}: Transcripts disabled or not found")
                            transcripts_skipped += 1
                        except Exception as e:
                            print(f"  Error fetching transcript for video {video_id}: {e}")
                            transcripts_skipped += 1
                            
                        # Sleep to avoid hitting rate limits
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"Error processing playlist {playlist_url}: {e}")
        
        subjects_processed += 1
        
    print("\n--- Summary ---")
    print(f"Subjects processed: {subjects_processed}")
    print(f"Transcripts saved: {transcripts_saved}")
    print(f"Transcripts skipped: {transcripts_skipped}")

if __name__ == "__main__":
    asyncio.run(main())
