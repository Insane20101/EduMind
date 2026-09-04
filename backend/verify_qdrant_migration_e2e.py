import os
import sys
import uuid
from dotenv import load_dotenv

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

sys.path.append(os.path.dirname(__file__))

from qdrant_client import QdrantClient
from rag.vector_store import get_qdrant_client, get_or_create_subject_collection, upsert_chunks, delete_resource_chunks
from rag.retriever import retrieve_context, query_vector_store

def test_qdrant_migration_e2e():
    print("=" * 60)
    print("      QDRANT CLOUD END-TO-END MIGRATION VERIFICATION")
    print("=" * 60)

    # 1. Connect & Audit Collections
    client = get_qdrant_client()
    collections_res = client.get_collections()
    collection_names = [c.name for c in collections_res.collections]
    print(f"\n[1] Found {len(collection_names)} collections in Qdrant Cloud:")
    print(f"    Sample Collections: {collection_names[:10]}")
    assert len(collection_names) > 0, "ERROR: No collections found in Qdrant Cloud!"

    # 2. Check BSM-104 Collection & Vector Count
    bsm_collection = "BSM-104"
    assert bsm_collection in collection_names, f"ERROR: Collection {bsm_collection} missing!"
    bsm_info = client.get_collection(bsm_collection)
    print(f"\n[2] Collection '{bsm_collection}' Info:")
    print(f"    Points count: {bsm_info.points_count}")
    print(f"    Vector dim: {bsm_info.config.params.vectors.size}")
    print(f"    Distance metric: {bsm_info.config.params.vectors.distance}")
    assert bsm_info.points_count > 0, f"ERROR: Collection {bsm_collection} has 0 points!"

    # 3. Test Retriever with unit filtering
    print(f"\n[3] Testing Context Retrieval for BSM-104 (matrices/eigenvalues, Unit I)...")
    context_chunks = retrieve_context(
        query="matrices eigenvalues characteristic equation",
        subject_id="BSM-104",
        unit="Unit I",
        top_k=3
    )
    print(f"    Retrieved {len(context_chunks)} chunks:")
    for i, c in enumerate(context_chunks):
        snippet = c.get("text", "")[:100].replace("\n", " ").encode("ascii", "replace").decode("ascii")
        unit = c.get("metadata", {}).get("unit", "N/A")
        print(f"    [{i+1}] Unit: {unit} | Snippet: {snippet}...")
    assert len(context_chunks) > 0, "ERROR: Context retrieval returned 0 chunks!"

    # 4. Test Quiz Store Query
    print(f"\n[4] Testing Quiz Vector Query for BSM-104...")
    quiz_chunks = query_vector_store(
        query="differential equations matrix rank",
        subject_id="BSM-104",
        top_k=3
    )
    print(f"    Retrieved {len(quiz_chunks)} quiz chunks:")
    for i, c in enumerate(quiz_chunks):
        snippet = c.get("text", "")[:100].replace("\n", " ").encode("ascii", "replace").decode("ascii")
        print(f"    [{i+1}] Snippet: {snippet}...")
    assert len(quiz_chunks) > 0, "ERROR: Quiz vector query returned 0 chunks!"

    # 5. Test Scoped Chunk Deletion
    test_subj = "TEST-QDRANT-DEL"
    test_res_id = f"res_{uuid.uuid4().hex[:8]}"
    test_filename = "test_doc_deletion.pdf"

    print(f"\n[5] Testing Scoped Resource Chunk Deletion...")
    print(f"    Inserting dummy test chunk for {test_subj} with resource_id={test_res_id}...")
    dummy_chunk = {
        "text": "This is a secret test chunk for verification of scoped Qdrant deletion.",
        "metadata": {
            "subject_id": test_subj,
            "resource_id": test_res_id,
            "source_file": test_filename,
            "unit": "Unit I"
        }
    }
    upsert_chunks([dummy_chunk])

    # Verify insertion
    retrieved_before = retrieve_context(query="secret test chunk verification", subject_id=test_subj, top_k=3)
    print(f"    Retrieved before deletion: {len(retrieved_before)} chunks")
    assert len(retrieved_before) > 0, "ERROR: Dummy chunk was not retrieved before deletion!"

    # Delete scoped resource chunks
    print(f"    Deleting resource {test_res_id} from subject {test_subj}...")
    del_count = delete_resource_chunks(subject_id=test_subj, resource_id=test_res_id, source_filename=test_filename)
    print(f"    Delete function reported {del_count} chunks removed.")

    # Verify deletion
    retrieved_after = retrieve_context(query="secret test chunk verification", subject_id=test_subj, top_k=3)
    print(f"    Retrieved after deletion: {len(retrieved_after)} chunks")
    assert len(retrieved_after) == 0, "ERROR: Chunk was still retrieved after deletion!"

    # Cleanup test collection
    try:
        client.delete_collection(test_subj)
        print(f"    Cleaned up test collection '{test_subj}'.")
    except Exception as e:
        print(f"    Cleanup notice: {e}")

    print("\n" + "=" * 60)
    print("  ALL QDRANT E2E VERIFICATION TESTS PASSED SUCCESSFULLY!  ")
    print("=" * 60)

if __name__ == "__main__":
    test_qdrant_migration_e2e()
