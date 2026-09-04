import time
import threading
from typing import Dict, Any

class IngestionQueueManager:
    """
    Single-task concurrency lock manager for vector ingestion and OCR tasks.
    Ensures only ONE ingestion operation runs at any time across the entire platform
    to prevent API quota/token exhaustion (429 errors) and ChromaDB write collisions.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._status: Dict[str, Any] = {
            "locked": False,
            "status": "idle",
            "progress": 0,
            "message": "Platform ready for resource ingestion.",
            "filename": "",
            "start_time": 0
        }

    def acquire_lock(self, filename: str) -> bool:
        with self._lock:
            # Auto-expire locks older than 5 minutes in case of unhandled worker crash
            if self._status["locked"]:
                if time.time() - self._status["start_time"] > 300:
                    self._status["locked"] = False
                else:
                    return False

            self._status = {
                "locked": True,
                "status": "processing",
                "progress": 10,
                "message": f"Lock acquired for {filename}. Starting processing...",
                "filename": filename,
                "start_time": time.time()
            }
            return True

    def update_progress(self, progress: int, message: str):
        with self._lock:
            if self._status["locked"]:
                self._status["progress"] = max(0, min(100, progress))
                self._status["message"] = message

    def release_lock(self, success: bool = True, final_message: str = ""):
        with self._lock:
            self._status["locked"] = False
            self._status["status"] = "idle" if success else "failed"
            self._status["progress"] = 100 if success else 0
            self._status["message"] = final_message or ("Ingestion complete." if success else "Ingestion failed.")
            self._status["filename"] = ""
            self._status["start_time"] = 0

    def get_status(self) -> Dict[str, Any]:

        with self._lock:
            # Auto-expire timeout check
            if self._status["locked"] and (time.time() - self._status["start_time"] > 300):
                self._status["locked"] = False
                self._status["status"] = "failed"
                self._status["message"] = "Ingestion timed out."
            return dict(self._status)

# Global singleton instance
ingestion_queue = IngestionQueueManager()
