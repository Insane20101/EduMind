import os
import json
from fastapi import APIRouter, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from slowapi import Limiter
from slowapi.util import get_remote_address


from rag.retriever import retrieve
from rag.prompts import RAG_SYSTEM_PROMPT
from rag.generator import generate_with_retry, generate_stream
from utils.logger import get_logger

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = get_logger(__name__)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    subject_id: str
    unit_id: Optional[str] = None
    message: str
    conversation_history: List[ChatMessage] = []
    video_title: Optional[str] = None

class VideoSummaryRequest(BaseModel):
    video_title: str
    subject_id: str
    unit_name: Optional[str] = None
    playlist_title: Optional[str] = None

@router.post("/video-summary")
@limiter.limit("20/minute")
async def generate_video_summary(request: Request, payload: VideoSummaryRequest):
    """
    Generates a real-time structured summary for a specific lecture video
    combining video title context and ChromaDB RAG course material.
    """
    query = f"{payload.video_title} {payload.unit_name or ''}"
    chunks = retrieve(
        subject_id=payload.subject_id if payload.subject_id != "global" else "BCS-401",
        unit_id=None,
        query=query,
        top_k=6
    )
    
    context_text = ""
    if chunks and chunks[0]['similarity'] >= 0.2:
        context_parts = [f"--- Course Material Context ---\n{c['text']}" for c in chunks if c['similarity'] >= 0.2]
        context_text = "\n\n".join(context_parts)

    prompt = f"""You are EduMind AI Lecture Assistant.
Generate a comprehensive, beautifully structured executive summary for the university lecture video titled:
"{payload.video_title}"
Playlist: {payload.playlist_title or 'University Lecture Series'}
Unit/Topic: {payload.unit_name or 'Core Subject Topic'}

{f'Relevant Course Context:\n{context_text}' if context_text else 'Generate the summary using domain expertise for this computer science/engineering topic.'}

FORMATTING INSTRUCTIONS:
1. Use clean Markdown headers (###).
2. Include sections:
   - 🎯 **Lecture Overview & Objectives**
   - 🔑 **Key Concepts & Definitions**
   - 💡 **Core Takeaways & Formulas/Algorithms**
   - 📝 **3 High-Yield Exam Questions from this Topic**
3. Use bullet points, bold key terms, and clean structure. Keep it engaging, clear, and high quality.
"""

    summary = generate_with_retry(prompt, is_json=False)
    if not summary:
        summary = "Could not generate summary due to API limits. Please try again in a few seconds."

    return {
        "video_title": payload.video_title,
        "summary": summary,
        "grounded": bool(context_text)
    }


@router.post("/stream")
@limiter.limit("20/minute")
async def chat_stream(request: Request, payload: ChatRequest):
    if payload.subject_id == "global":
        history_text = ""
        for msg in payload.conversation_history[-5:]:
            history_text += f"{msg.role.upper()}: {msg.content}\n"
            
        prompt = f"""You are EduMind AI teaching assistant. The user has asked a question without selecting a specific subject.
Your task is to answer the user's question using your general knowledge (including basic information like subjects and syllabus if relevant).

IMPORTANT: You MUST start your response EXACTLY with this friendly reminder, followed by two newlines, then your actual answer:
"I'm your EduMind AI teaching assistant! To get accurate and helpful answers based on your course materials, please **select a specific subject** from the homepage first. I can help you better when I know exactly what you're studying!"

Include Mermaid flowcharts whenever possible to explain concepts. MANDATORY DIAGRAM RULE: If your text refers to or promises a diagram or flowchart (e.g. "Below is the diagram", "Here is the flowchart"), you MUST include the complete ```mermaid ... ``` code block. Never claim a diagram is provided without outputting the ```mermaid code block. DO NOT provide unsolicited or arbitrary examples of mathematical equations unless requested.

Conversation History:
{history_text if history_text else "None"}

User Query: {payload.message}
"""
        grounded = False
        source_ids = []
    else:
        chunks = retrieve(
            subject_id=payload.subject_id,
            unit_id=payload.unit_id,
            query=payload.message,
            top_k=6
        )
        grounded = False
        context_text = ""
        source_ids = []
        if chunks and chunks[0]['similarity'] >= 0.3:
            grounded = True
            context_parts = []
            for c in chunks:
                if c['similarity'] >= 0.3:
                    context_parts.append(f"--- Chunk ID: {c['chunk_id']} ---\n{c['text']}")
                    source_ids.append(c['chunk_id'])
            context_text = "\n\n".join(context_parts)
            
        history_text = ""
        for msg in payload.conversation_history[-5:]:
            history_text += f"{msg.role.upper()}: {msg.content}\n"
            
        user_query_with_video = f"[Currently Watching Video: \"{payload.video_title}\"]\n\n{payload.message}" if payload.video_title else payload.message
        prompt = RAG_SYSTEM_PROMPT.format(
            context=context_text if grounded else "No relevant context found in course materials.",
            history=history_text if history_text else "None",
            query=user_query_with_video
        )

    def event_generator():
        meta = json.dumps({"type": "metadata", "grounded": grounded, "sources": source_ids})
        yield f"data: {meta}\n\n"
        
        has_chunks = False
        for chunk in generate_stream(prompt):
            has_chunks = True
            data = json.dumps({"type": "chunk", "text": chunk})
            yield f"data: {data}\n\n"
            
        if not has_chunks:
            error_msg = "Gemini API rate limit reached (Free tier limit is 20 requests/minute). Please wait a few seconds and try asking again!"
            data = json.dumps({"type": "chunk", "text": error_msg})
            yield f"data: {data}\n\n"
            
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/")
@limiter.limit("20/minute")
async def chat(request: Request, payload: ChatRequest):
    if payload.subject_id == "global":
        history_text = ""
        for msg in payload.conversation_history[-5:]:
            history_text += f"{msg.role.upper()}: {msg.content}\n"
            
        prompt = f"""You are EduMind AI teaching assistant. The user has asked a question without selecting a specific subject.
Your task is to answer the user's question using your general knowledge (including basic information like subjects and syllabus if relevant).

IMPORTANT: You MUST start your response EXACTLY with this friendly reminder, followed by two newlines, then your actual answer:
"I'm your EduMind AI teaching assistant! To get accurate and helpful answers based on your course materials, please **select a specific subject** from the homepage first. I can help you better when I know exactly what you're studying!"

Include Mermaid flowcharts whenever possible to explain concepts. MANDATORY DIAGRAM RULE: If your text refers to or promises a diagram or flowchart (e.g. "Below is the diagram", "Here is the flowchart"), you MUST include the complete ```mermaid ... ``` code block. Never claim a diagram is provided without outputting the ```mermaid code block. DO NOT provide unsolicited or arbitrary examples of mathematical equations unless requested.

Conversation History:
{history_text if history_text else "None"}

User Query: {payload.message}
"""
        answer = generate_with_retry(prompt, is_json=False)
        if not answer:
            answer = "Gemini API rate limit reached (Free tier limit is 20 requests/minute). Please wait a few seconds and try asking again!"
            
        return {
            "answer": answer,
            "grounded": False,
            "sources": []
        }
        
    # 1. Retrieve context
    chunks = retrieve(
        subject_id=payload.subject_id,
        unit_id=payload.unit_id,
        query=payload.message,
        top_k=6
    )
    
    # 2. Check similarity threshold (e.g., 0.3 minimum)
    grounded = False
    context_text = ""
    source_ids = []
    
    if chunks and chunks[0]['similarity'] >= 0.3:
        grounded = True
        context_parts = []
        for c in chunks:
            if c['similarity'] >= 0.3:
                context_parts.append(f"--- Chunk ID: {c['chunk_id']} ---\n{c['text']}")
                source_ids.append(c['chunk_id'])
        context_text = "\n\n".join(context_parts)
        
    # 3. Format history
    history_text = ""
    for msg in payload.conversation_history[-5:]: # Keep last 5 turns
        history_text += f"{msg.role.upper()}: {msg.content}\n"
        
    # 4. Build prompt
    prompt = RAG_SYSTEM_PROMPT.format(
        context=context_text if grounded else "No relevant context found in course materials.",
        history=history_text if history_text else "None",
        query=payload.message
    )
    
    # 5. Call LLM
    answer = generate_with_retry(prompt, is_json=False)
    if not answer:
        answer = "Gemini API rate limit reached (Free tier limit is 20 requests/minute). Please wait a few seconds and try asking again!"
        
    logger.info("Chat response generated", extra={
        "subject_id": payload.subject_id,
        "unit_id": payload.unit_id,
        "grounded": grounded,
        "source_ids": source_ids
    })
    
    return {
        "answer": answer,
        "grounded": grounded,
        "sources": source_ids
    }

@router.post("/temp-document")
@limiter.limit("10/minute")
async def chat_temp_document(
    request: Request,
    file: UploadFile = File(...),
    message: str = Form(""),
    subject_id: Optional[str] = Form("global")
):
    try:
        content_bytes = await file.read()
        filename = file.filename or "uploaded_document"
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        extracted_text = ""

        if ext == "pdf":
            try:
                import fitz
                doc = fitz.open(stream=content_bytes, filetype="pdf")
                pages_text = []
                for i, page in enumerate(doc):
                    t = page.get_text()
                    if t and t.strip():
                        pages_text.append(f"--- Page {i+1} ---\n{t.strip()}")
                extracted_text = "\n\n".join(pages_text)
            except Exception as e:
                logger.warning(f"PyMuPDF parse failed: {e}")
                try:
                    import io, pypdf
                    reader = pypdf.PdfReader(io.BytesIO(content_bytes))
                    pages_text = []
                    for i, page in enumerate(reader.pages):
                        t = page.extract_text()
                        if t and t.strip():
                            pages_text.append(f"--- Page {i+1} ---\n{t.strip()}")
                    extracted_text = "\n\n".join(pages_text)
                except Exception as e2:
                    logger.warning(f"pypdf parse failed: {e2}")
                    try:
                        extracted_text = content_bytes.decode("utf-8", errors="ignore")
                    except Exception:
                        extracted_text = ""

        elif ext in ["png", "jpg", "jpeg", "webp"]:
            try:
                import base64
                b64_str = base64.b64encode(content_bytes).decode("utf-8")
                mime_type = f"image/{'jpeg' if ext in ['jpg', 'jpeg'] else ext}"
                
                vision_prompt = f"""You are EduMind AI document assistant.
The user has attached an image document named "{filename}".
User Question / Instruction: {message if message.strip() else 'Extract and solve/explain all text, questions, diagrams, or content visible in this image.'}

FORMATTING INSTRUCTIONS:
1. Extract and analyze ALL text, questions, formulas, tables, and content visible in the image.
2. Structure the response using clean Markdown headers (###), bold key-value pairs (**Field:** Value), and bullet lists.
3. Include Mermaid flowcharts whenever helpful to explain concepts or procedures.
4. If the image contains a question or problem, provide the complete, step-by-step solution."""

                answer = None

                # 1. Try OpenAI Vision (gpt-4o-mini)
                if os.getenv("OPENAI_API_KEY"):
                    try:
                        from langchain_core.messages import HumanMessage
                        from langchain_openai import ChatOpenAI
                        
                        vision_message = HumanMessage(
                            content=[
                                {"type": "text", "text": vision_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:{mime_type};base64,{b64_str}"}
                                }
                            ]
                        )
                        llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
                        res = llm.invoke([vision_message])
                        if res and res.content:
                            answer = str(res.content)
                    except Exception as ve:
                        logger.warning(f"OpenAI Vision failed: {ve}")

                # 2. Try Google GenAI SDK Vision (gemini-3.6-flash)
                if not answer and (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
                    try:
                        from google import genai
                        from google.genai import types
                        gkey = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
                        gclient = genai.Client(api_key=gkey)
                        part = types.Part.from_bytes(data=content_bytes, mime_type=mime_type)
                        gres = gclient.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=[part, vision_prompt]
                        )
                        if gres and gres.text:
                            answer = gres.text
                    except Exception as ve2:
                        logger.warning(f"Google GenAI Vision failed: {ve2}")

                if answer:
                    return {
                        "answer": answer.strip(),
                        "grounded": True,
                        "sources": [{"filename": filename}]
                    }
                else:
                    return {
                        "answer": "Vision API quota limit reached. Please wait a few seconds and try uploading the image again!",
                        "grounded": False,
                        "sources": [{"filename": filename}]
                    }
            except Exception as vis_err:
                logger.warning(f"Vision processing failed: {vis_err}")
                return {
                    "answer": "Failed to process image document. Please ensure it is a valid PNG, JPG, or WEBP image file.",
                    "grounded": False,
                    "sources": [{"filename": filename}]
                }
        else:
            try:
                extracted_text = content_bytes.decode("utf-8", errors="ignore")
            except Exception:
                extracted_text = f"[Uploaded document: {filename}]"


        if not extracted_text.strip():
            extracted_text = f"[Uploaded document: {filename}]"

        prompt = f"""You are EduMind AI assistant. The user has attached a temporary document named "{filename}".
Here is the extracted document text/content:

{extracted_text[:15000]}

User Question/Instructions:
{message if message.strip() else 'Provide a detailed formatted summary of the document.'}

FORMATTING INSTRUCTIONS:
1. Organize the response using clean Markdown headers (###), bold key-value pairs (**Field:** Value), and bullet lists.
2. If summarizing financial data, charges, or structured items, use standard GitHub Markdown tables:
   | Item / Description | Quantity | Amount |
   | :--- | :---: | :---: |
   | Consultation | 1 | $150.00 |
3. Ensure immaculate typography, spacing, and structured sections (e.g. 📄 Document Overview, 📊 Charges Breakdown, 💳 Summary)."""

        answer = generate_with_retry(prompt, is_json=False)
        if not answer:
            raise HTTPException(status_code=500, detail="Failed to generate response from Gemini for document.")

        return {
            "answer": answer,
            "grounded": True,
            "sources": [{"filename": filename}]
        }
    except Exception as e:
        logger.error(f"Error processing temp document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")


