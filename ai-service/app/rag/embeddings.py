from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings

from app.config import (
    GEMINI_EMBEDDING_MODEL,
    GOOGLE_API_KEY,
    LLM_PROVIDER,
)


def get_embeddings():
    """Return the embedding implementation matching the configured provider."""
    if LLM_PROVIDER == "gemini":
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY is not configured.")
        return GoogleGenerativeAIEmbeddings(
            model=GEMINI_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY,
        )

    if LLM_PROVIDER == "ollama":
        return OllamaEmbeddings(model="nomic-embed-text")

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}. Choose 'ollama' or 'gemini'."
    )


def get_collection_name() -> str:
    """Keep vectors from different embedding spaces in separate collections."""
    model = (
        GEMINI_EMBEDDING_MODEL
        if LLM_PROVIDER == "gemini"
        else "nomic-embed-text"
    )
    safe_model = "".join(character if character.isalnum() else "_" for character in model)
    return f"incident_knowledge_base_{LLM_PROVIDER}_{safe_model}"
