import json
import os
import time
import yt_dlp
import re
import ssl
import urllib3
import requests
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Bypass SSL globally for yt-dlp and youtube_transcript_api
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

old_request = requests.Session.request
def new_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(self, method, url, **kwargs)
requests.Session.request = new_request

BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "CSE")
SEED_FILE = os.path.join(os.path.dirname(__file__), "subjects_seed.json")

def main():
    print("Loading subjects from subjects_seed.json...")
    with open(SEED_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    ydl_opts = {'extract_flat': True, 'quiet': True, 'nocheckcertificate': True, 'socket_timeout': 15}
    
    total_processed = 0
    total_saved = 0
    blocked_items = []
    
    for semester, subjects in data.items():
        # IMPORTANT FIX: "Semester-1" -> "Semester1" to match existing folders
        semester_folder = semester.replace("-", "")
        
        for subject in subjects:
            code = subject.get("code")
            name = subject.get("name", "")
            raw_playlists = subject.get("playlists", [])
            
            if isinstance(raw_playlists, str):
                playlist_urls = [raw_playlists]
            elif isinstance(raw_playlists, list):
                playlist_urls = []
                for p in raw_playlists:
                    if isinstance(p, str):
                        playlist_urls.append(p)
                    elif isinstance(p, dict) and "url" in p:
                        playlist_urls.append(p["url"])
            else:
                playlist_urls = []
            
            safe_code = re.sub(r'[<>:"/\\|?*]', '-', code)
            safe_name = re.sub(r'[<>:"/\\|?*]', '-', name)
            folder_name = f"{safe_code} {safe_name}"
            target_dir = os.path.join(BASE_DATA_DIR, semester_folder, folder_name, "transcripts")
            os.makedirs(target_dir, exist_ok=True)
            
            print(f"Processing {code} - {name}...")
            video_index = 1
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for url in playlist_urls:
                    if not url or "playlist?list=" not in url:
                        print(f"  Skipping non-playlist URL: {url}")
                        continue
                        
                    print(f"  Extracting playlist: {url}")
                    try:
                        info = ydl.extract_info(url, download=False)
                        if not info or 'entries' not in info:
                            continue
                            
                        for entry in info['entries']:
                            if not entry: continue
                            video_id = entry.get('id')
                            if not video_id: continue
                            
                            try:
                                # v1.2.4 API
                                ytt_api = YouTubeTranscriptApi()
                                transcript_list = ytt_api.list(video_id)
                                try:
                                    # Try English/Hindi first
                                    transcript = transcript_list.find_transcript(['en', 'en-IN', 'hi'])
                                except:
                                    # Fallback to the first available one
                                    transcript = list(transcript_list)[0]
                                    
                                filepath = os.path.join(target_dir, f"video_{video_index}_{video_id}.txt")
                                if os.path.exists(filepath):
                                    print(f"    Skipping existing {video_id}")
                                    video_index += 1
                                    continue
                                    
                                ts_data = transcript.fetch()
                                text = " ".join([s.text for s in ts_data])
                                
                                with open(filepath, "w", encoding="utf-8") as outf:
                                    outf.write(text)
                                    
                                total_saved += 1
                                video_index += 1
                                print(f"    Saved {video_id} -> {filepath}")
                                
                            except (TranscriptsDisabled, NoTranscriptFound):
                                print(f"    Skipped {video_id}: Transcripts disabled or missing")
                            except Exception as e:
                                print(f"    Error on {video_id}: {e}")
                                if "block" in str(e).lower() or "too many requests" in str(e).lower():
                                    blocked_items.append(f"Video {video_id} from {url}")
                                
                            time.sleep(0.5)
                    except Exception as e:
                        print(f"  Error extracting {url}: {e}")
                        blocked_items.append(f"Playlist {url}")
            total_processed += 1
            
    print(f"\nDone! Processed {total_processed} subjects, saved {total_saved} transcripts.")
    if blocked_items:
        print("\n--- BLOCKED ITEMS ---")
        for item in blocked_items:
            print(item)
        with open("blocked_items.txt", "w", encoding="utf-8") as bf:
            bf.write("\n".join(blocked_items))
        print(f"\nSaved list of blocked items to blocked_items.txt")

if __name__ == "__main__":
    main()
