import json
from typing import TypedDict, Any
from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.llm import get_llm
from app.services.backend_client import get_investigation_data
from app.agents.schemas import IncidentAnalysis
from app.agents.evidence_validator import validate_evidence

from typing import Any

from app.rag.retrieve import retrieve_relevant_documents


# Shared State
class IncidentState(TypedDict,total = False):
    incident_id : int
    investigation_data : dict[str,Any]

    log_analysis: str
    metrics_analysis: str
    deployment_analysis: str

    evidence_validation: dict[str, Any]
    investigation_status: str

    analysis: str

    retrieved_context: list[dict[str, Any]]

    source_references: list[dict[str, Any]]

#Node 1 : Fetch incident evidence from spring boot
def fetch_evidence(state: IncidentState) -> dict:
    incident_id = state["incident_id"]
    data = get_investigation_data(incident_id)
    return {
        "investigation_data": data
    }


#Node 2 : Analyze logs
def analyze_logs(state : IncidentState) -> dict:
    data = state["investigation_data"]

    # llm = ChatOllama(
    #     model = OLLAMA_MODEL,
    #     base_url = OLLAMA_BASE_URL,
    #     temperature = 0
    # )
    llm = get_llm()

    prompt = f"""
    You are a production incident investigator.
    Focus on log evidence in the supplied incident data.

    Identify:
    1.Errors and Exceptions
    2.Repeated failures or suspicious patterns
    3.Relevant timestamps and affected components
    4.What the logs establish and what remains uncertain

    Do not invent log entries. If logs are missing, say so.

    Incident data:
    {json.dumps(data,indent=2,default = str)}
    """

    response = llm.invoke(prompt)
    return{
        "log_analysis" : response.content
    }



def analyze_metrics(state: IncidentState) -> dict:
    data = state["investigation_data"]

    # llm = ChatOllama(
    #     model=OLLAMA_MODEL,
    #     base_url=OLLAMA_BASE_URL,
    #     temperature=0
    # )
    llm = get_llm()
    prompt = f"""
    You are a production reliability engineer.

    Focus on metrics in the supplied incident data.

    Identify:
    1.Abnormal metric values or trends
    2.Potential latency, throughput or resource issues
    3.Relevant timestamps and ffected components
    4.What the metrics establish and what remains uncertain

    Do not invent metric values or thresholds.
    If metrics are missing,say so.

    Incident data:
    {json.dumps(data,indent=2,default=str)}
    """

    response = llm.invoke(prompt)
    return{
        "metrics_analysis": response.content
    }



def analyze_deployments(state: IncidentState) -> dict:
    data = state["investigation_data"]

    # llm = ChatOllama(
    #     model = OLLAMA_MODEL,
    #     base_url = OLLAMA_BASE_URL,
    #     temperature = 0
    # )

    llm = get_llm()

    prompt = f"""
    You are a production incident investigator.
    Focus on deployment evidence in the supplied incident data.

    Identify:
    1.Recent deployments or configuration changes.
    2.Their timestamps and affected services, if provided
    3.Whether the timeline correlates with the incident.
    4.What additional evidence would be needed to establish causation

    Do not assume that a deployment caused the incident merely because it occured nearby in time.
    If deployment evidence is missing, say so.

    Incident data:
    {json.dumps(data,indent=2,default=str)}
    """
    response = llm.invoke(prompt)
    return{
        "deployment_analysis": response.content
    }





def synthesize_findings(state: IncidentState) -> dict:
    llm = ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL,
        temperature=0,
        format=IncidentAnalysis.model_json_schema(),
    )

    prompt = f"""
You are investigating a production software incident.

Use only the evidence and intermediate findings supplied below.
Do not invent logs, metric values, deployments, or observations.
A correlation does not prove causation.
If evidence is insufficient, say so and explain the uncertainty.
Confidence must reflect the strength of the evidence, not guesswork.
Recommendations must be actionable and safe. Do not claim actions
have already been performed.

INCIDENT EVIDENCE:
{state["investigation_data"]}

LOG ANALYSIS:
{state["log_analysis"]}

METRICS ANALYSIS:
{state["metrics_analysis"]}

DEPLOYMENT ANALYSIS:
{state["deployment_analysis"]}

Return an object matching the requested IncidentAnalysis schema.
"""

    response = llm.invoke(prompt)

    raw = response.content.strip()

    # Remove Markdown code fences if present.
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        raw = "\n".join(lines).strip()

    # Validate the structured response.
    analysis = IncidentAnalysis.model_validate_json(raw)

    return {
        "analysis": analysis.model_dump_json(indent=2)
    }



def validate_findings(state: IncidentState) -> dict:
    analysis = json.loads(state["analysis"])

    validation = validate_evidence(
        analysis=analysis,
        investigation_data=state["investigation_data"],
    )
    return {
    "evidence_validation": validation,
    "investigation_status": validation["status"],
}


# Conditional router: choose the appropriate finalization path
def route_after_validation(state: IncidentState) -> dict:
    status = state["evidence_validation"]["status"]

    if status == "supported":
        return "supported"
    
    if status == "partially supported":
        return "partially_supported"
    return "inconclusive"

def retrieve_context(state: IncidentState) -> dict[str, Any]:
    """
    Retrieve historical incidents and runbooks relevant to this incident.
    Save both the retrieved text and its source references in graph state.
    """

    # Get the incident evidence already fetched from the Spring Boot API.
    investigation_data = state.get("investigation_data", {})

    # Convert the incident evidence to text so vector search can use it.
    incident_text = json.dumps(
        investigation_data,
        indent=2,
        default=str,
    )

    documents = retrieve_relevant_documents(
        query=incident_text,
        k=4,
    )

    retrieved_context = documents

    # build source references
    source_references = [
        {
            "source": document["source"],
            "start_index": document["start_index"],
            "distance": document["distance"],
        }
        for document in documents
    ]

    return {
        "retrieved_context": retrieved_context,
        "source_references": source_references,
    }

# Orchestration - defines the execution order
builder = StateGraph(IncidentState)

builder.add_node("fetch_evidence",fetch_evidence)
builder.add_node("analyze_logs",analyze_logs)
builder.add_node("analyze_metrics",analyze_metrics)
builder.add_node("analyze_deployments",analyze_deployments)
builder.add_node("synthesize_findings",synthesize_findings)
builder.add_node("validate_findings",validate_findings)
builder.add_node("retrieve_context",retrieve_context)



# Start by fetching evidence
builder.add_edge(START, "fetch_evidence")

# Fan-out: analyze evidence in parallel
builder.add_edge("fetch_evidence", "analyze_logs")
builder.add_edge("fetch_evidence", "analyze_metrics")
builder.add_edge("fetch_evidence", "analyze_deployments")
builder.add_edge("fetch_evidence", "retrieve_context")

# Fan-in: synthesize after all three analyses & rag result
builder.add_edge(
    [
        "analyze_logs",
        "analyze_metrics",
        "analyze_deployments",
        "retrieve_context",
    ],
    "synthesize_findings",
)

# Validate the synthesized findings
builder.add_edge("synthesize_findings", "validate_findings")

# Conditional routing
builder.add_conditional_edges(
    "validate_findings",
    route_after_validation,
    {
        "supported": END,
        "partially_supported": END,
        "inconclusive": END,
    },
)

incident_graph = builder.compile()


