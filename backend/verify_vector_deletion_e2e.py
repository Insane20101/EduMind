import asyncio
import os
import uuid
import requests
from database import db, upload_file, delete_file
from rag.ingester import ingest_document
from rag.retriever import retrieve
from rag.vector_store import get_qdrant_client, delete_resource_chunks

SECRET_KEYWORD = "QUANTUM_CYPHER_XYZ_9988"
FILENAME = "Quantum_Encryption_Test_Unit1.md"
SUBJECT_ID = "BCS-401"
BASE_URL = "http://localhost:8000"

async def run_e2e_verification():
    print("=" * 70)
    print("STEP 1: Ingesting Test Document into Qdrant Cloud & GridFS...")
    print("=" * 70)

    test_content = (
        f"# Quantum Encryption Unit 1 Note\n\n"
        f"The primary classification secret for quantum security is {SECRET_KEYWORD}.\n"
        f"This secret key defines the quantum security protocol for Operating Systems."
    ).encode("utf-8")

    resource_id = str(uuid.uuid4())
    cloud_file_id = await upload_file(FILENAME, test_content, "text/markdown")

    # Ingest document into Qdrant Cloud collection for BCS-401
    ingest_summary = ingest_document(
        content_bytes=test_content,
        filename=FILENAME,
        subject_id=SUBJECT_ID,
        unit_id="UNIT-I",
        resource_type="note"
    )

    print(f"-> Ingestion Success! Chunks created: {ingest_summary['chunk_count']}")

    # Insert document record into MongoDB db.resources
    doc = {
        "resource_id": resource_id,
        "cloud_file_id": cloud_file_id,
        "subject_id": SUBJECT_ID,
        "resource_type": "note",
        "title": "Quantum Encryption Test Note",
        "filename": FILENAME,
        "url": "",
        "cloudinary_public_id": None,
        "status": "approved",
        "uploaded_by": "admin",
        "uploaded_at": "2026-09-04T10:50:00Z",
        "reviewed_by": "admin",
        "reviewed_at": "2026-09-04T10:50:00Z",
        "reject_reason": None,
        "source": "admin",
        "ingest_summary": ingest_summary
    }
    await db.resources.insert_one(doc)
    print(f"-> Created MongoDB Resource Record (resource_id: {resource_id})")

    # Verify vector store contains chunks
    client = get_qdrant_client()
    points, _ = client.scroll(
        collection_name=SUBJECT_ID,
        scroll_filter=None,
        limit=100
    )
    matching_points = [p for p in points if p.payload and p.payload.get("source_filename") == FILENAME]
    before_count = len(matching_points)
    print(f"-> Qdrant Collection '{SUBJECT_ID}' Chunks Count for '{FILENAME}': {before_count}")
    assert before_count > 0, "ERROR: Vector chunks were not created in Qdrant!"

    print("\n" + "=" * 70)
    print("STEP 2: Retrieval Check BEFORE Deletion — Confirming Content is Retrievable...")
    print("=" * 70)

    retrieved_before = retrieve(SUBJECT_ID, None, SECRET_KEYWORD, top_k=5)
    matching_before = [c for c in retrieved_before if SECRET_KEYWORD in c["text"]]
    print(f"-> Retrieved {len(matching_before)} matching chunks containing '{SECRET_KEYWORD}'.")
    assert len(matching_before) > 0, "ERROR: Content was not retrievable before deletion!"
    print(f"-> Snippet: \"{matching_before[0]['text'][:120]}\"")
    print("-> [VERIFIED]: Secret content is RETRIEVABLE via RAG Retriever!")

    print("\n" + "=" * 70)
    print(f"STEP 3: Executing Resource Deletion Workflow for resource_id '{resource_id}'...")
    print("=" * 70)

    # 1. Purge Qdrant Vector Chunks
    purged_count = delete_resource_chunks(subject_id=SUBJECT_ID, resource_id=resource_id, source_filename=FILENAME)
    print(f"-> Purged {purged_count} chunks from Qdrant Cloud collection '{SUBJECT_ID}'.")

    # 2. Delete GridFS File
    if cloud_file_id:
        await delete_file(cloud_file_id)
        print(f"-> Deleted GridFS file '{cloud_file_id}'.")

    # 3. Delete MongoDB Metadata Record
    await db.resources.delete_many({"resource_id": resource_id})
    print(f"-> Deleted resource metadata record from MongoDB.")

    print("\n" + "=" * 70)
    print("STEP 4: Post-Deletion Verifications...")
    print("=" * 70)

    # 4a. Check MongoDB Document
    db_doc_after = await db.resources.find_one({"resource_id": resource_id})
    print(f"-> MongoDB Record Exists: {db_doc_after is not None} (Expected False)")
    assert db_doc_after is None, "ERROR: Resource record still exists in MongoDB!"

    # 4b. Check Qdrant collection chunks
    points_after, _ = client.scroll(
        collection_name=SUBJECT_ID,
        scroll_filter=None,
        limit=100
    )
    matching_after_points = [p for p in points_after if p.payload and p.payload.get("source_filename") == FILENAME]
    after_count = len(matching_after_points)
    print(f"-> Qdrant Collection '{SUBJECT_ID}' Chunks Count for '{FILENAME}': {after_count} (Expected 0)")
    assert after_count == 0, "ERROR: Vector chunks still present in Qdrant!"

    # 4c. Check RAG Retriever AFTER Deletion
    retrieved_after = retrieve(SUBJECT_ID, None, SECRET_KEYWORD, top_k=5)
    matching_after = [c for c in retrieved_after if SECRET_KEYWORD in c["text"]]
    print(f"-> Retrieved {len(matching_after)} matching chunks containing '{SECRET_KEYWORD}'. (Expected 0)")
    assert len(matching_after) == 0, "ERROR: Content was STILL retrievable after deletion!"
    print("-> [VERIFIED]: Secret content is NO LONGER RETRIEVABLE anywhere in the system!")

    print("\n" + "=" * 70)
    print("ALL SCOPED-DELETION VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_e2e_verification())
