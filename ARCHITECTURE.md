# EduMind System Architecture & Storage Rationale

## 1. Dual Storage Architecture: GridFS + Cloudinary
EduMind utilizes a deliberate **Dual-Backend Storage System** for uploaded PDF, Markdown, and media resources:

1. **Cloudinary CDN (Primary Delivery Layer)**:
   - Serves as the high-speed CDN endpoint (`secure_url`).
   - Enables instant streaming, PDF preview in `PdfViewerModal`, and image rendering with low latency for end users.
2. **MongoDB GridFS (Binary Persistence & Fallback Layer)**:
   - Stores raw binary bytes directly inside MongoDB Atlas alongside document metadata (`cloud_file_id`).
   - Guarantees zero data loss if Cloudinary free-tier bandwidth caps are reached, credentials change, or Cloudinary suffers an outage.
   - Served via `/api/resources/file/{resource_id}` as a direct stream fallback.

## 2. Vector DB Payload Indexing (Qdrant Cloud)
- Every subject collection in Qdrant maintains strict `PayloadSchemaType.KEYWORD` indexes on `unit`, `chunk_type`, `schema_version`, `resource_id`, and `source_filename`.
- Server-side filtering using Qdrant `models.Filter` executes in ~350ms with zero timeouts, enabling scalable multi-dimensional retrieval filtering.
