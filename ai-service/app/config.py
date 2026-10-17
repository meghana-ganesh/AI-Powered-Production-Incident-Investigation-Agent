import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8081")

