
import json

from app.agents.evidence_validator import validate_evidence
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL, BACKEND_BASE_URL
from app.services.backend_client import get_investigation_data
from app.agents.incident_graph import incident_graph
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="AI Production Incident Agent",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)

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
    result = incident_graph.invoke({"incident_id": incident_id})

    
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
}
