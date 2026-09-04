# RAG Architecture & Guardrails (Phase 0)

## Current Repository Understanding
- **Backend:** Uses FastAPI + MongoDB (motor driver), JWT auth, Pydantic schemas, and slowapi rate limiting.
- **Frontend:** Uses React 19 + Vite + Tailwind v4 + Zustand + React Router v7 + Axios.
- **Data Structure:** `data/CSE/Semester1-8/` holds per-subject folders containing question banks (e.g., `BCS-201_Question_Bank.md`), solutions (`BCS-201_Solutions.md`), and cleaned transcripts (e.g., `video_5_lg-f92uY1Lc.txt`).
- **Subject Metadata:** `subjects_seed.json` (the exact file name in the repo) holds subject metadata including a flat `playlists` array/string for each subject.

---

## 1. Chunking Strategy & Metadata

Every chunk stored in the vector database will carry strict metadata to enforce isolation and traceability.

### Common Metadata Fields (Attached to ALL chunks)
- `subject_id` (e.g., "BCS-303")
- `semester` (e.g., "Semester-5")
- `unit` (e.g., "UNIT-I" for Question Banks/Solutions. For transcripts, since they live in flat folders without a mapping manifest, this MUST explicitly be set to `"unassigned"`. Do not use null/None.)
- `source_type` ("transcript" | "question_bank" | "solution")
- `source_file` (e.g., "video_5_lg-f92uY1Lc.txt")
- `chunk_index` (integer to preserve ordering)
- `chunk_id` (unique string identifier)

### Chunking by Source Type
- **Transcripts (.txt):** 
  - **Size:** ~1000 tokens / ~4000 characters.
  - **Overlap:** 200 tokens / ~800 characters to maintain context across continuous speech.
  - **Parsing:** Split by paragraph or sentence boundaries using recursive character splitting.
- **Question Banks & Solutions (Markdown):**
  - **Size:** Context-aware chunks based on Markdown headers (e.g., `## Unit I`, `### Question 1`).
  - **Overlap:** Minimal overlap. The goal is to isolate complete Question-Answer pairs into single chunks without splitting logical blocks arbitrarily.

---

## 2. Ingestion Pipeline Steps
1. **Discovery:** Scan `data/CSE/` for all subject folders, loading `.txt` transcripts and `.md` question banks/solutions.
2. **Metadata Extraction:** Determine `subject_id`, `semester`, and `unit` based on folder structure, file names, and Markdown headers.
3. **Chunking:** Apply the specific chunking strategy based on `source_type`.
4. **Embedding Generation (`backend/app/rag/embedder.py`)**
   - We strictly use **OpenAI (`text-embedding-3-small`)** for embedding text chunks.
   - *Why OpenAI instead of Gemini?* Speed and rate limits. Gemini's free tier (15 RPM) is too slow for large-scale ingestion (e.g. 3,500+ chunks), while OpenAI embeddings cost practically nothing and support massive batching (2048 inputs per request) for near-instant ingestion.
   - We use the `python-dotenv` package to load the `OPENAI_API_KEY`. 
   - *Important Architecture Note*: This is a permanent, deliberate split. **OpenAI** is used exclusively for *Embeddings* (both at ingestion time and during runtime query retrieval). **Gemini** (with our existing quota-rotation logic) continues to be used for all *Generation* tasks (chat responses, quiz generation, etc).

#### Quiz Resubmission Policy (Phase 6)
**Decision**: Quiz submissions (`POST /api/quiz/{quiz_id}/submit`) are strictly idempotent (no-retakes allowed).
**Reasoning**: Allowing retakes for the exact same `quiz_id` inflates accuracy metrics and conflates memorizing the quiz structure with true unit mastery. If a student wishes to re-test the same unit, they must generate a new quiz to retrieve fresh questions. Second submission attempts for an existing `quiz_id` will be rejected with a `400 Bad Request`.

5. **Vector Storage (`backend/app/rag/vector_store.py`)**
   - Upsert the embeddings and their associated metadata into a **per-subject ChromaDB collection** (where the collection name is exactly the `subject_id`). The ingestion logic (e.g., in `vector_store.py` -> `upsert_chunks()`) will dynamically create this collection if it doesn't already exist.

---

## 3. Retrieval Flow (Strict Structural Scoping)

To definitively prevent context mixup (e.g., Subject A's content leaking into Subject B's quiz), ChromaDB will use **one collection per `subject_id`**. Relying on a metadata `where` filter inside a shared collection is risky; if a filter is ever omitted by mistake, chunks bleed across subjects. A separate collection makes this structurally impossible.

1. **Hard Boundary (Collection Selection):** The retrieval logic (e.g., in `retriever.py` -> `retrieve()`) **must** first open the Chroma collection explicitly named after the requested `subject_id` before doing anything else.
2. **Metadata Filter (Secondary Layer):** Within that subject's collection, apply a `where={"unit": "..."}` filter if a specific unit is set by the user. **Crucially, chunks marked as `unit: "unassigned"` are strictly INELIGIBLE for unit-scoped queries.** A unit-filtered request must never silently include unassigned chunks just because a loose filter allowed missing/null values.
3. **Semantic Search:** Cosine similarity is applied only within this structurally bounded and (optionally) metadata-filtered collection to retrieve the top-K chunks.

---

## 4. Technology Choices & Anti-Hallucination Guardrails

- **Database (Document Store):** Currently using a local JSON-backed mock database (`USE_MOCK_DB=true`) to simplify Phase 1-5 development without requiring a local MongoDB instance. We will migrate to a real MongoDB connection (using Motor) in Phase 6 for production deployment. The `database.py` file uses an async lock to ensure the JSON mock is safe against concurrent writes during development.
- **Vector Store:** **ChromaDB** will run as a local persistent client alongside FastAPI (path: `backend/chroma_data/`). We will not migrate to MongoDB Atlas Vector Search to avoid new paid infrastructure.
- **Embeddings:** **OpenAI `text-embedding-3-small`** (using the `openai` Python SDK with batching for high-speed, cost-efficient processing).
- **Generation Model:** **`gemini-3.5-flash`** as the primary LLM. 
- **Quota Management:** We will strictly reuse the exact quota-rotation script logic from `clean_transcripts.py` to seamlessly rotate models (e.g., to `gemini-3.5-flash-lite`) if a 429 RESOURCE_EXHAUSTED error occurs.
- **Structured Output Only:** Quiz generation will use Gemini's native JSON mode (`response_mime_type: "application/json"` and `response_schema`). No free-text parsing will be allowed to prevent hallucinated formats or mismatched answer keys.
- **Grounding Refusal Rule:** A single, shared prompt template will enforce the following rule for all generations:
  > *"If the retrieved context does not contain enough information to answer/generate this, say so explicitly rather than inventing content."*
- **Source Citations:** Every chat answer and generated quiz question will return the `chunk_id`(s) it used for grounding. This is a non-negotiable debugging tool to differentiate between retrieval misses and generation hallucinations.
