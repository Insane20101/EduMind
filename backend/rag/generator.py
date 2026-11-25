import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def _resolve_google_model(model_name: str) -> str:
    """Map internal or legacy model names to valid LangChain Google model identifiers."""
    if not model_name:
        return "gemini-3.8-flash"
    # If legacy 2.x or 1.x models requested, upgrade to latest active flash
    if "gemini-1.5" in model_name or "gemini-2.0" in model_name or "gemini-2.5" in model_name:
        return "gemini-3.8-flash"
    if not model_name.startswith("gemini-"):
        return "gemini-3.8-flash"
    return model_name

def get_primary_llm(model_name: str = "gemini-3.8-flash", temperature: float = 0.3):
    """
    Returns primary ChatGoogleGenerativeAI model instance with instant failover max_retries=0.
    """
    if GEMINI_API_KEY:
        resolved_model = _resolve_google_model(model_name)
        return ChatGoogleGenerativeAI(
            model=resolved_model,
            google_api_key=GEMINI_API_KEY,
            temperature=temperature,
            max_retries=0,
            timeout=15
        )
    elif OPENAI_API_KEY:
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=OPENAI_API_KEY,
            temperature=temperature,
            max_retries=0,
            timeout=15
        )
    raise ValueError("No valid LLM API key (GEMINI_API_KEY or OPENAI_API_KEY) found.")

def get_fallback_llms(temperature: float = 0.3):
    """
    Returns fallback LLM models (ChatGoogleGenerativeAI alternatives, ChatGroq, ChatOpenAI).
    """
    fallbacks = []
    # 1. Active Gemini models (latest high-performance production versions)
    if GEMINI_API_KEY:
        for m in ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-flash-latest"]:
            try:
                fallbacks.append(ChatGoogleGenerativeAI(
                    model=m,
                    google_api_key=GEMINI_API_KEY,
                    temperature=temperature,
                    max_retries=0,
                    timeout=15
                ))
            except Exception:
                pass

    # 2. OpenAI fallback
    if OPENAI_API_KEY:
        try:
            fallbacks.append(ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=temperature, max_retries=1, timeout=15))
        except Exception:
            pass

    # 3. Active Groq production models
    if GROQ_API_KEY:
        groq_models = [
            'qwen/qwen3.8-27b',
            'openai/gpt-oss-20b',
            'openai/gpt-oss-120b'
        ]
        for m in groq_models:
            try:
                fallbacks.append(ChatGroq(model=m, groq_api_key=GROQ_API_KEY, temperature=temperature, max_retries=1, timeout=12))
            except Exception: 
                pass

    return fallbacks

def get_llm_with_fallback(model_name: str = "gemini-3.8-flash", temperature: float = 0.3):
    """
    Returns a LangChain LLM equipped with fallbacks using .with_fallbacks()
    """
    primary = get_primary_llm(model_name=model_name, temperature=temperature)
    fallbacks = get_fallback_llms(temperature=temperature)
    if fallbacks:
        return primary.with_fallbacks(fallbacks)
    return primary

def generate_with_retry(prompt: str, is_json: bool = False, model: str = 'gemini-3.8-flash', response_schema=None) -> str | None:
    """
    Generates text or JSON content using LangChain LCEL runnable chains with fallback support.
    If response_schema (Pydantic model) is passed, uses .with_structured_output().
    """
    try:
        if response_schema:
            llm = get_llm_with_fallback(model_name=model, temperature=0.3)
            structured_llm = llm.with_structured_output(response_schema)
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an educational assessment assistant. Produce output strictly conforming to the requested schema."),
                ("user", "{input}")
            ])
            chain = prompt_template | structured_llm
            result = chain.invoke({"input": prompt})
            if hasattr(result, "model_dump_json"):
                return result.model_dump_json()
            elif isinstance(result, dict):
                import json
                return json.dumps(result)
            return str(result)
        else:
            llm = get_llm_with_fallback(model_name=model, temperature=0.3)
            prompt_template = ChatPromptTemplate.from_messages([
                ("user", "{input}")
            ])
            chain = prompt_template | llm | StrOutputParser()
            result = chain.invoke({"input": prompt})
            return result.strip() if result else None
    except Exception as e:
        print(f"  LangChain generation primary error: {e}")
        fallbacks = get_fallback_llms()
        for fb in fallbacks:
            try:
                if response_schema:
                    structured_fb = fb.with_structured_output(response_schema)
                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", "You are an educational assessment assistant. Produce output strictly conforming to the requested schema."),
                        ("user", "{input}")
                    ])
                    chain = prompt_template | structured_fb
                    res = chain.invoke({"input": prompt})
                    if hasattr(res, "model_dump_json"):
                        return res.model_dump_json()
                    elif isinstance(res, dict):
                        import json
                        return json.dumps(res)
                    return str(res)
                else:
                    prompt_template = ChatPromptTemplate.from_messages([("user", "{input}")])
                    chain = prompt_template | fb | StrOutputParser()
                    res = chain.invoke({"input": prompt})
                    if res and res.strip():
                        return res.strip()
            except Exception as fb_err:
                print(f"  Generation fallback failed: {fb_err}")
                continue
        return None

def generate_stream(prompt: str, model: str = 'gemini-3.8-flash'):
    """
    Streams text content from LangChain runnable chain, yielding text chunks as they arrive.
    """
    try:
        llm = get_llm_with_fallback(model_name=model, temperature=0.3)
        prompt_template = ChatPromptTemplate.from_messages([
            ("user", "{input}")
        ])
        chain = prompt_template | llm | StrOutputParser()
        
        streamed_any = False
        for chunk in chain.stream({"input": prompt}):
            if chunk:
                streamed_any = True
                yield chunk
        if streamed_any:
            return
    except Exception as e:
        print(f"  LangChain streaming primary error: {e}")
        fallbacks = get_fallback_llms()
        for fb in fallbacks:
            try:
                prompt_template = ChatPromptTemplate.from_messages([("user", "{input}")])
                chain = prompt_template | fb | StrOutputParser()
                streamed_any = False
                for chunk in chain.stream({"input": prompt}):
                    if chunk:
                        streamed_any = True
                        yield chunk
                if streamed_any:
                    return
            except Exception as fb_err:
                print(f"  Streaming fallback failed: {fb_err}")
                continue
        yield "API limit reached. Please wait a few seconds and try asking again!"


