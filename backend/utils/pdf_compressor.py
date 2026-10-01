"""
EduMind High-Performance PDF Compressor Pipeline (Step 1).
Compresses large/scanned PDFs into target byte limits using local PyMuPDF 
with optional external compression API fallback.
"""

import os
import io
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

def compress_pdf_bytes(
    content_bytes: bytes,
    target_max_bytes: int = 10 * 1024 * 1024,  # Default 10 MB
    target_dpi: int = 150,
    jpeg_quality: int = 75,
    force_compression: bool = False
) -> bytes:
    """
    Compresses PDF bytes if size exceeds target_max_bytes or if force_compression is True.
    Returns compressed PDF bytes (or original bytes if compression fails or isn't needed).
    """
    if not content_bytes or not isinstance(content_bytes, bytes):
        return content_bytes

    # Check for PDF magic header (%PDF-)
    if not content_bytes.startswith(b"%PDF-"):
        return content_bytes

    orig_size = len(content_bytes)
    orig_mb = orig_size / (1024 * 1024)

    # If already smaller than target limit and not forced, return as-is
    if orig_size <= target_max_bytes and not force_compression:
        return content_bytes

    logger.info(f"🔄 [Step 1 PDF Compression] Initiating compression for PDF ({orig_mb:.2f} MB, Target limit: {target_max_bytes / (1024 * 1024):.2f} MB)...")

    # ── Attempt 1: External Compressor API (if environment URL configured) ──
    external_api_url = os.getenv("PDF_COMPRESSOR_API_URL")
    if external_api_url:
        try:
            logger.info(f"🌐 Calling external PDF compressor API at {external_api_url}...")
            api_key = os.getenv("PDF_COMPRESSOR_API_KEY", "")
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            files = {"file": ("document.pdf", content_bytes, "application/pdf")}
            resp = requests.post(external_api_url, files=files, headers=headers, timeout=30)
            if resp.status_code == 200 and resp.content and resp.content.startswith(b"%PDF-"):
                ext_size = len(resp.content)
                logger.info(f"✅ External API compression succeeded: {orig_mb:.2f} MB -> {ext_size / (1024 * 1024):.2f} MB")
                return resp.content
            else:
                logger.warning(f"External PDF compression API returned status {resp.status_code}. Falling back to internal engine...")
        except Exception as ext_err:
            logger.warning(f"External PDF compression API call failed ({ext_err}). Falling back to internal engine...")

    # ── Attempt 2: High-Efficiency Internal PyMuPDF Engine ─────────
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            pymupdf = None

    if not pymupdf:
        logger.warning("PyMuPDF / fitz package not available for PDF compression.")
        return content_bytes

    try:
        doc = pymupdf.open(stream=content_bytes, filetype="pdf")
        
        # Pass 1: Try fast garbage collection & stream deflation first
        deflated_bytes = doc.tobytes(
            garbage=4,
            deflate=True,
            clean=True,
            deflate_images=True,
            deflate_fonts=True
        )
        
        deflated_size = len(deflated_bytes)
        if deflated_size <= target_max_bytes:
            logger.info(f"✅ Fast stream deflation compressed PDF: {orig_mb:.2f} MB -> {deflated_size / (1024 * 1024):.2f} MB")
            return deflated_bytes

        # Pass 2: Heavy Scanned PDF Page Image Resampling & Re-encoding
        logger.info(f"⚡ PDF still exceeds limit after fast deflation ({deflated_size / (1024 * 1024):.2f} MB). Running page image compression (DPI: {target_dpi}, Quality: {jpeg_quality})...")
        
        out_doc = pymupdf.open()
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            rect = page.rect
            
            # Render page image at target DPI
            pix = page.get_pixmap(dpi=target_dpi)
            jpg_bytes = pix.tobytes("jpg", jpg_quality=jpeg_quality)
            
            # Create new page and insert re-compressed image
            new_page = out_doc.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(new_page.rect, stream=jpg_bytes)

        compressed_bytes = out_doc.tobytes(
            garbage=4,
            deflate=True,
            clean=True,
            deflate_images=True,
            deflate_fonts=True
        )
        out_doc.close()
        doc.close()

        comp_size = len(compressed_bytes)
        comp_mb = comp_size / (1024 * 1024)
        ratio = (1 - (comp_size / orig_size)) * 100

        logger.info(f"✅ PyMuPDF image re-encoding compression complete: {orig_mb:.2f} MB -> {comp_mb:.2f} MB ({ratio:.1f}% reduction)")
        return compressed_bytes

    except Exception as comp_err:
        logger.error(f"❌ PDF compression encountered error: {comp_err}. Returning original file bytes.")
        return content_bytes
