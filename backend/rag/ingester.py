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


logger = logging.getLogger(__name__)

def extract_text_from_pdf(content_bytes: bytes, filename: str) -> str:
    """
    Extracts text from PDF bytes using PyMuPDF / pypdf.
    If no text layer exists (scanned image PDF), falls back to Multimodal Vision OCR.
    """
    extracted_text = ""
    try:
        import fitz
        doc = fitz.open(stream=content_bytes, filetype="pdf")
        pages = []
        for i, page in enumerate(doc):
            t = page.get_text()
            if t and t.strip():
                pages.append(f"--- Page {i+1} ---\n{t.strip()}")
        extracted_text = "\n\n".join(pages)
    except Exception as e:
        logger.warning(f"PyMuPDF parse failed: {e}")
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content_bytes))
            pages = []
            for i, page in enumerate(reader.pages):
                t = page.extract_text()
                if t and t.strip():
                    pages.append(f"--- Page {i+1} ---\n{t.strip()}")
            extracted_text = "\n\n".join(pages)
        except Exception as e2:
            logger.warning(f"pypdf parse failed: {e2}")

    # Fallback to Vision OCR if text layer is empty (scanned image PDF)
    if not extracted_text.strip():
        logger.info(f"PDF {filename} has no native text layer. Running Vision OCR via gpt-4o-mini...")
        try:
            import fitz
            doc = fitz.open(stream=content_bytes, filetype="pdf")
            ocr_pages = []
            for page in doc:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                
                if os.getenv("OPENAI_API_KEY"):
                    from langchain_openai import ChatOpenAI
                    from langchain_core.messages import HumanMessage
                    import base64
                    b64 = base64.b64encode(img_bytes).decode("utf-8")
                    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
                    res = llm.invoke([HumanMessage(content=[
                        {"type": "text", "text": "Extract all readable text, formulas, and diagrams from this scanned document page verbatim."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                    ])])
                    if res and res.content and str(res.content).strip():
                        ocr_pages.append(str(res.content).strip())
            if ocr_pages:
                extracted_text = "\n\n".join(ocr_pages)
        except Exception as ocr_err:
            logger.warning(f"Vision OCR fallback failed for {filename}: {ocr_err}")

    if not extracted_text.strip():
        logger.info(f"PDF '{filename}' contains image/scanned pages. Creating document placeholder metadata chunk...")
        extracted_text = f"--- Document: {filename} ---\nSubject: {filename}\nResource Type: Academic PDF Resource\nSummary: Document '{filename}' is available for inline viewing and download."

    return extracted_text



def ingest_document(
    content_bytes: bytes,
    filename: str,
    subject_id: str,
    unit_id: Optional[str] = None,
    resource_type: str = "note"
) -> Dict[str, Any]:
    """
    SINGLE UNIFIED INGESTION PIPELINE
    Used by bulk ingestion, admin vector curation, and student upload approvals.

    Guarantees:
    1. subject_id is strictly mandatory.
    2. Missing/null unit_id defaults to "unassigned".
    3. Structured Q# markdown uses question-boundary chunking; generic prose uses token-window chunking.
    4. Writes strictly into get_langchain_vectorstore(subject_id).
    """
    if not subject_id or not subject_id.strip():
        raise ValueError("subject_id is mandatory for vector ingestion.")

    subject_id = subject_id.strip().upper()
    effective_unit = unit_id.strip() if (unit_id and unit_id.strip()) else "unassigned"

    ext = filename.split(".")[-1].lower() if "." in filename else ""

    # 1. Text Extraction
    if ext == "pdf":
        raw_text = extract_text_from_pdf(content_bytes, filename)
    else:
        try:
            raw_text = content_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            raise ValueError(f"Failed to decode text file '{filename}': {e}")

    if not raw_text.strip():
        raise ValueError(f"Document '{filename}' contains no text content.")

    # 2. Chunking Routing
    documents: List[Document] = []
    has_qbank_tags = bool(re.search(r'Q\d+:', raw_text) and ("Topic:" in raw_text or "Unit" in raw_text))

    if has_qbank_tags and ext in ["md", "txt"]:
        # Structured question bank tagged format -> Use chunk_markdown from chunker.py
        raw_chunks = chunk_markdown(raw_text, source_file=filename, subject_id=subject_id, semester="Semester-3", source_type="markdown")
        for rc in raw_chunks:
            meta = dict(rc.get("metadata", {}))
            meta["subject_id"] = subject_id
            if not meta.get("unit") or meta.get("unit") == "unassigned":
                meta["unit"] = effective_unit
            meta["source_filename"] = filename
            meta["resource_type"] = resource_type
            documents.append(Document(page_content=rc.get("text", ""), metadata=meta))

    else:
        # Untagged generic prose (PDFs, Markdown notes, student uploads) -> Use RecursiveCharacterTextSplitter
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
                "resource_type": resource_type,
                "is_placeholder": is_placeholder_doc
            }
            documents.append(Document(page_content=chunk_str, metadata=meta))

    if not documents:
        raise ValueError(f"No valid chunks produced for document '{filename}'.")

    # 3. VectorStore Persistence (Qdrant Cloud)
    chunks_to_upsert = [{"text": d.page_content, "metadata": d.metadata} for d in documents]
    upsert_chunks(chunks_to_upsert)

    logger.info(f"Ingested {len(documents)} chunks for file '{filename}' into subject collection '{subject_id}' (unit: '{effective_unit}').")

    return {
        "status": "success",
        "subject_id": subject_id,
        "unit": effective_unit,
        "filename": filename,
        "chunk_count": len(documents)
    }
