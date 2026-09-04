import asyncio
from database import db, upload_file

# Valid 1-page PDF binary with text
SAMPLE_PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj<>/Type/Catalog>>endobj\n"
    b"2 0 obj<>/Type/Page/Parent 1 0 R/MediaBox[0 0 612 792]/Contents 3 0 R/Resources<>>>endobj\n"
    b"3 0 obj<>/Length 145>>stream\n"
    b"BT /F1 24 Tf 50 700 Td (EduMind Academic Course Document) Tj ET\n"
    b"BT /F1 14 Tf 50 650 Td (Subject: BCS-401 - Operating Systems) Tj ET\n"
    b"BT /F1 12 Tf 50 600 Td (Official Syllabus Practice & Review Material) Tj ET\n"
    b"endstream\n"
    b"endobj\n"
    b"xref\n"
    b"0 4\n"
    b"0000000000 65535 f\n"
    b"0000000009 00000 n\n"
    b"0000000058 00000 n\n"
    b"0000000185 00000 n\n"
    b"trailer<>/Root 1 0 R>>\n"
    b"startxref\n"
    b"380\n"
    b"%%EOF\n"
)

async def seed_valid_pdfs():
    resources = await db.resources.find({}).to_list(100)
    print(f"Found {len(resources)} resources to fix.")
    
    for r in resources:
        rid = r.get("resource_id")
        title = r.get("title", "Assignment")
        
        # Upload valid sample PDF content to files store
        file_id = await upload_file(f"{title}.pdf", SAMPLE_PDF_BYTES, "application/pdf")
        
        # Update resource with cloud_file_id
        await db.resources.update_one(
            {"resource_id": rid},
            {"$set": {
                "cloud_file_id": file_id
            }}
        )
        print(f"Updated resource {rid} ({title}) with file_id: {file_id}")

if __name__ == "__main__":
    asyncio.run(seed_valid_pdfs())
