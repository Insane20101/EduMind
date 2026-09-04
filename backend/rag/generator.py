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
    """Map internal model names to valid LangChain Google model identifiers."""
    if not model_name or "3.6" in model_name:
        return "gemini-1.5-flash"
    if not model_name.startswith("gemini-"):
        return "gemini-1.5-flash"
    return model_name

def get_primary_llm(model_name: str = "gemini-1.5-flash", temperature: float = 0.3):
    """
    Returns primary ChatGoogleGenerativeAI model instance.
    """
    if GEMINI_API_KEY:
        resolved_model = _resolve_google_model(model_name)
        return ChatGoogleGenerativeAI(
            model=resolved_model,
            google_api_key=GEMINI_API_KEY,
            temperature=temperature
        )
    elif OPENAI_API_KEY:
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=OPENAI_API_KEY,
            temperature=temperature
        )
    raise ValueError("No valid LLM API key (GEMINI_API_KEY or OPENAI_API_KEY) found.")

def get_fallback_llms(temperature: float = 0.3):
    """
    Returns fallback LLM models (ChatGroq / ChatOpenAI).
    """
    fallbacks = []
    if GROQ_API_KEY:
        groq_models = ['llama-3.3-70b-versatile', 'llama3-70b-8192', 'mixtral-8x7b-32768']
        for m in groq_models:
            try:
                fallbacks.append(ChatGroq(model=m, groq_api_key=GROQ_API_KEY, temperature=temperature))
            except Exception:
                pass
    if OPENAI_API_KEY:
        fallbacks.append(ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=temperature))
    return fallbacks

def get_llm_with_fallback(model_name: str = "gemini-1.5-flash", temperature: float = 0.3):
    """
    Returns a LangChain LLM equipped with fallbacks using .with_fallbacks()
    """
    primary = get_primary_llm(model_name=model_name, temperature=temperature)
    fallbacks = get_fallback_llms(temperature=temperature)
    if fallbacks:
        return primary.with_fallbacks(fallbacks)
    return primary

def generate_with_retry(prompt: str, is_json: bool = False, model: str = 'gemini-1.5-flash', response_schema=None) -> str | None:
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
        print(f"  LangChain generation error: {e}")
        try:
            fallbacks = get_fallback_llms()
            if fallbacks:
                prompt_template = ChatPromptTemplate.from_messages([("user", "{input}")])
                chain = prompt_template | fallbacks[0] | StrOutputParser()
                res = chain.invoke({"input": prompt})
                return res.strip() if res else None
        except Exception as e2:
            print(f"  LangChain secondary fallback error: {e2}")
        return None

def generate_stream(prompt: str, model: str = 'gemini-1.5-flash'):
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
        print(f"  LangChain streaming error: {e}")
        try:
            fallbacks = get_fallback_llms()
            if fallbacks:
                prompt_template = ChatPromptTemplate.from_messages([("user", "{input}")])
                chain = prompt_template | fallbacks[0] | StrOutputParser()
                for chunk in chain.stream({"input": prompt}):
                    if chunk:
                        yield chunk
                return
        except Exception as e2:
            print(f"  LangChain secondary streaming fallback error: {e2}")
            yield "API limit reached. Please wait a few seconds and try asking again!"


