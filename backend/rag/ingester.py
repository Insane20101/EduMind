import os
import io
import re
import uuid
import logging
from typing import Dict, Any, List, Optional
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.vector_store import upsert_chunks
from rag.chunker import chunk_markdown, chunk_transcript
from rag.content_categories import get_category_config, SCHEMA_VERSION


logger = logging.getLogger(__name__)

def extract_text_from_pdf(content_bytes: bytes, filename: str) -> str:
    """
    Extracts text from PDF bytes using PyMuPDF / pypdf.
    Handles encrypted PDFs, password-protected/blank-pass documents, and multi-layout blocks.
    If no text layer exists (scanned image PDF), falls back to Multimodal Vision OCR (Gemini / OpenAI).
    If parsing fails entirely, returns a robust document placeholder chunk so ingestion NEVER fails.
    """
    if not content_bytes:
        return f"--- Document: {filename} ---\nSubject: {filename}\nResource Type: Academic PDF Resource\nSummary: Document '{filename}' is available for inline viewing and download."

    extracted_text = ""
    
    # 1. Native text layer extraction via PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(stream=content_bytes, filetype="pdf")
        
        # Authenticate with empty string if PDF has security/encryption flags set
        if getattr(doc, "is_encrypted", False) or getattr(doc, "needs_pass", False):
            try:
                doc.authenticate("")
            except Exception as auth_err:
                logger.warning(f"PyMuPDF empty auth notice for {filename}: {auth_err}")

        pages = []
        for i, page in enumerate(doc):
            try:
                # Pass 1: Standard text extraction
                t = page.get_text("text")
                
                # Pass 2: Blocks extraction fallback if standard text is empty
                if not (t and t.strip()):
                    blocks = page.get_text("blocks")
                    if blocks:
                        t = "\n".join([b[4] for b in blocks if len(b) >= 5 and isinstance(b[4], str)])

                # Pass 3: Layout extraction fallback
                if not (t and t.strip()):
                    try:
                        t = page.get_text("layout")
                    except Exception:
                        pass

                # Pass 4: Form XObject / Field widgets fallback
                if not (t and t.strip()):
                    try:
                        widget_texts = [w.field_value for w in page.widgets() if getattr(w, 'field_value', None)]
                        if widget_texts:
                            t = "\n".join(widget_texts)
                    except Exception:
                        pass

                if t and t.strip():
                    pages.append(f"--- Page {i+1} ---\n{t.strip()}")
            except Exception:
                continue
        extracted_text = "\n\n".join(pages)
    except Exception as e:
        logger.warning(f"PyMuPDF parse notice for {filename}: {e}")

    # 2. Native text layer fallback via pypdf
    if not extracted_text.strip():
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content_bytes))
            
            if getattr(reader, "is_encrypted", False):
                try:
                    reader.decrypt("")
                except Exception as dec_err:
                    logger.warning(f"pypdf decrypt notice for {filename}: {dec_err}")

            pages = []
            for i, page in enumerate(reader.pages):
                try:
                    t = page.extract_text()
                    if t and t.strip():
                        pages.append(f"--- Page {i+1} ---\n{t.strip()}")
                except Exception:
                    continue
            extracted_text = "\n\n".join(pages)
        except Exception as e2:
            logger.warning(f"pypdf parse notice for {filename}: {e2}")

    # 3. Multimodal Vision OCR fallback for scanned/image PDFs (Gemini or OpenAI)
    if not extracted_text.strip():
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if gemini_key or openai_key:
            logger.info(f"PDF '{filename}' has no native text layer. Running Multimodal Vision OCR fallback...")
            try:
                import fitz
                import base64
                doc = fitz.open(stream=content_bytes, filetype="pdf")
                if getattr(doc, "is_encrypted", False):
                    try: doc.authenticate("")
                    except Exception: pass
                
                ocr_pages = []
                for page in doc:
                    try:
                        pix = page.get_pixmap()
                        img_bytes = pix.tobytes("png")
                        b64 = base64.b64encode(img_bytes).decode("utf-8")
                        
                        ocr_text = ""
                        if gemini_key:
                            try:
                                from langchain_google_genai import ChatGoogleGenerativeAI
                                from langchain_core.messages import HumanMessage
                                llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", google_api_key=gemini_key)
                                res = llm.invoke([HumanMessage(content=[
                                    {"type": "text", "text": "Extract all readable text, formulas, and diagrams from this scanned document page verbatim."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                                ])])
                                if res and res.content:
                                    ocr_text = str(res.content).strip()
                            except Exception as g_err:
                                logger.warning(f"Gemini Vision OCR notice for page: {g_err}")

                        if not ocr_text and openai_key:
                            try:
                                from langchain_openai import ChatOpenAI
                                from langchain_core.messages import HumanMessage
                                llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
                                res = llm.invoke([HumanMessage(content=[
                                    {"type": "text", "text": "Extract all readable text, formulas, and diagrams from this scanned document page verbatim."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                                ])])
                                if res and res.content:
                                    ocr_text = str(res.content).strip()
                            except Exception as o_err:
                                logger.warning(f"OpenAI Vision OCR notice for page: {o_err}")

                        if ocr_text:
                            ocr_pages.append(ocr_text)
                    except Exception:
                        continue
                if ocr_pages:
                    extracted_text = "\n\n".join(ocr_pages)
            except Exception as ocr_err:
                logger.warning(f"Vision OCR fallback notice for {filename}: {ocr_err}")

    # 4. Ultimate Guaranteed Metadata Placeholder (Ingestion NEVER fails)
    if not extracted_text.strip():
        logger.info(f"PDF '{filename}' processed as academic PDF resource. Creating metadata placeholder chunk...")
        extracted_text = f"--- Document: {filename} ---\nSubject: {filename}\nResource Type: Academic PDF Resource\nSummary: Document '{filename}' is available for inline viewing and download."

    return extracted_text


def ingest_document(
    content_bytes: bytes,
    filename: str,
    subject_id: str,
    unit_id: Optional[str] = None,
    category_key: str = "notes",
    resource_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    SINGLE UNIFIED INGESTION PIPELINE
    Configured via Content Category Registry (backend/rag/content_categories.py).
    Stamps chunk_type, subject_id, unit, and schema_version on every Qdrant point.
    """
    if not subject_id or not subject_id.strip():
        raise ValueError("subject_id is mandatory for vector ingestion.")

    # Backward compatibility mapping for legacy resource_type callers
    effective_category = category_key
    if resource_type and (not category_key or category_key == "notes"):
        rt_map = {"note": "notes", "notes": "notes", "pyq": "pyq", "question_bank": "question_bank", "transcript": "transcript"}
        effective_category = rt_map.get(resource_type.lower(), resource_type)

    # Validate category key against Content Category Registry (raises ValueError if unknown)
    cat_config = get_category_config(effective_category)
    chunk_type = cat_config["chunk_type"]

    subject_id = subject_id.strip().upper()
    effective_unit = unit_id.strip() if (unit_id and unit_id.strip()) else "unassigned"

    ext = filename.split(".")[-1].lower() if "." in filename else ""

    # 1. Text Extraction
    if ext == "pdf":
        raw_text = extract_text_from_pdf(content_bytes, filename)
    else:
        try:
            raw_text = content_bytes.decode("utf-8", errors="ignore")
        except Exception:
            raw_text = f"--- Document: {filename} ---\nResource Type: Academic Resource"

    if not raw_text or not raw_text.strip():
        raw_text = f"--- Document: {filename} ---\nSubject: {subject_id}\nResource Type: Academic Resource\nSummary: Document '{filename}' is uploaded and available for viewing."

    # 2. Chunking Routing
    documents: List[Document] = []
    has_qbank_tags = bool(re.search(r'Q\d+:', raw_text) and ("Topic:" in raw_text or "Unit" in raw_text))

    if (has_qbank_tags or cat_config["chunker"] == "tagged_question_boundary") and ext in ["md", "txt"]:
        # Structured question bank tagged format -> Use chunk_markdown from chunker.py
        raw_chunks = chunk_markdown(raw_text, source_file=filename, subject_id=subject_id, semester="Semester-3", source_type="markdown")
        for rc in raw_chunks:
            meta = dict(rc.get("metadata", {}))
            meta["subject_id"] = subject_id
            if not meta.get("unit") or meta.get("unit") == "unassigned":
                meta["unit"] = effective_unit
            meta["source_filename"] = filename
            meta["chunk_type"] = chunk_type
            meta["category_key"] = cat_config["category_key"]
            meta["schema_version"] = SCHEMA_VERSION
            meta["resource_type"] = chunk_type
            documents.append(Document(page_content=rc.get("text", ""), metadata=meta))

    else:
        # Untagged generic prose (PDFs, Markdown notes, transcripts) -> Use RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)
        is_placeholder_doc = ("is available for inline viewing and download" in raw_text or "Document placeholder metadata" in raw_text)
        for i, chunk_str in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{i}_{uuid.uuid4().hex[:6]}"
            meta = {
                "chunk_id": chunk_id,
                "subject_id": subject_id,
                "unit": effective_unit,
                "source_filename": filename,
                "chunk_type": chunk_type,
                "category_key": cat_config["category_key"],
                "schema_version": SCHEMA_VERSION,
                "resource_type": chunk_type,
                "is_placeholder": is_placeholder_doc
            }
            documents.append(Document(page_content=chunk_str, metadata=meta))

    if not documents:
        raise ValueError(f"No valid chunks produced for document '{filename}'.")

    # 3. VectorStore Persistence (Qdrant Cloud)
    chunks_to_upsert = [{"text": d.page_content, "metadata": d.metadata} for d in documents]
    upsert_chunks(chunks_to_upsert)

    logger.info(f"Ingested {len(documents)} chunks for file '{filename}' into subject collection '{subject_id}' (category: '{cat_config['category_key']}', chunk_type: '{chunk_type}', unit: '{effective_unit}', v{SCHEMA_VERSION}).")

    return {
        "status": "success",
        "subject_id": subject_id,
        "unit": effective_unit,
        "filename": filename,
        "category_key": cat_config["category_key"],
        "chunk_type": chunk_type,
        "schema_version": SCHEMA_VERSION,
        "chunk_count": len(documents)
    }
