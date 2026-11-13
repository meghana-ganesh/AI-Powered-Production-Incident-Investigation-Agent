
import json
import httpx

from app.agents.evidence_validator import validate_evidence
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from langchain_ollama import ChatOllama
# from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL, BACKEND_BASE_URL
from app.llm import get_llm
from app.config import BACKEND_BASE_URL
from app.services.backend_client import get_investigation_data
from app.agents.incident_graph import incident_graph
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="AI Production Incident Agent",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-powered-production-incident-inve.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# llm = ChatOllama(
#     model=OLLAMA_MODEL,
#     base_url=OLLAMA_BASE_URL,
#     temperature=0
# )

llm = get_llm()

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "ai-service"
    }
@app.post("/chat")
def chat(request: ChatRequest):
    response = llm.invoke(request.message)
    return {
        "response": response.content
    }

@app.get("/test-backend/{incident_id}")
def test_backend(incident_id: int):
    return get_investigation_data(incident_id)

@app.post("/investigate/{incident_id}")
def investigate(incident_id : int):
    try:
        result = incident_graph.invoke({"incident_id": incident_id})
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            retry_after = exc.response.headers.get("Retry-After")
            headers = {"Retry-After": retry_after} if retry_after else None
            raise HTTPException(
                status_code=503,
                detail="The incident backend is rate limiting requests. Please retry shortly.",
                headers=headers,
            ) from exc
        raise HTTPException(
            status_code=502,
            detail=f"The incident backend returned HTTP {exc.response.status_code}.",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="The incident backend could not be reached.",
        ) from exc

    
    analysis_data = result["analysis"]

    # Your graph currently returns analysis as a JSON string.
    if isinstance(analysis_data, str):
        analysis_data = json.loads(analysis_data)

    validation = validate_evidence(
        analysis=analysis_data,
        investigation_data=result["investigation_data"],
    )

    return {
    "incident_id": incident_id,
    "investigation": result["analysis"],
    "evidence": result["investigation_data"],
    "evidence_validation": result["evidence_validation"],
    "investigation_status": result["investigation_status"],
    "sources": result.get("source_references", []),
}
