import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

def test_connection():
    print("=" * 70)
    print("TESTING QDRANT CLOUD CONNECTION...")
    print("=" * 70)
    print(f"URL: {QDRANT_URL}")
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # List existing collections
    collections_res = client.get_collections()
    collection_names = [c.name for c in collections_res.collections]
    print(f"Connected to Qdrant Cloud! Existing collections: {collection_names}")
    
    # Test creating a sample collection (BCS-401) if not present
    test_collection = "TEST_COLLECTION"
    if not client.collection_exists(test_collection):
        client.create_collection(
            collection_name=test_collection,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
        )
        print(f"Created test collection '{test_collection}' with 1536 dimensions (COSINE distance).")

    # Clean up test collection
    client.delete_collection(test_collection)
    print(f"Deleted test collection '{test_collection}'.")
    print("✨ QDRANT CLOUD CONNECTION TEST PASSED SUCCESSFULLY! ✨")

if __name__ == "__main__":
    test_connection()
