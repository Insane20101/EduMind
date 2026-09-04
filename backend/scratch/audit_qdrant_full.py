import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from qdrant_client import QdrantClient

def audit():
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    client = QdrantClient(url=url, api_key=api_key)
    collections = client.get_collections().collections
    sorted_cols = sorted(collections, key=lambda x: x.name)

    print("\n" + "=" * 70)
    print("                 QDRANT CLOUD FULL COLLECTIONS AUDIT REPORT")
    print("=" * 70)
    print(f"{'Collection Name':<20} | {'Point Count':<12} | {'Vector Dim':<10} | {'Distance Metric'}")
    print("-" * 70)

    total_points = 0
    for c in sorted_cols:
        info = client.get_collection(c.name)
        pts = info.points_count
        dim = info.config.params.vectors.size
        metric = info.config.params.vectors.distance
        total_points += pts
        print(f"{c.name:<20} | {pts:<12} | {dim:<10} | {metric}")

    print("=" * 70)
    print(f"TOTAL COLLECTIONS: {len(sorted_cols)}  |  TOTAL VECTOR POINTS: {total_points}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    audit()
