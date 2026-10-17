from pydantic import BaseModel, Field

class IncidentAnalysis(BaseModel):
    suspected_root_cause: str = Field(
        description="The most likely root cause, or  state that evidence is insufficient."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence level in the suspected root cause, from 0 to 1"
    )

    supporting_evidence: list[str] = Field(
        description="Specific observations grounded in the supplied incident data."
    )

    recommended_actions : list[str] = Field(
        description="Practical investigation or remediation steps."
    )

    uncertainties: list[str] = Field(
        description="Missing information, alternative explanations, or limitations."
    )
