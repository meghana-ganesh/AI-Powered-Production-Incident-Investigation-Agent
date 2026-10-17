
import json
import re
from typing import Any


def normalize_text(value: str) -> str:
    """Normalize text for case-insensitive evidence matching."""
    value = value.lower()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^\w\s.-]", "", value)
    return value.strip()


def collect_evidence_text(data: Any) -> str:
    """Extract searchable text from nested incident evidence."""
    if isinstance(data, str):
        return data

    if isinstance(data, dict):
        return " ".join(
            collect_evidence_text(value)
            for value in data.values()
        )

    if isinstance(data, (list, tuple)):
        return " ".join(
            collect_evidence_text(item)
            for item in data
        )

    if data is None:
        return ""

    return str(data)


def validate_evidence(
    analysis: dict,
    investigation_data: Any,
) -> dict:
    """
    Check whether each supporting-evidence claim appears
    in the original incident evidence.
    """
    evidence_text = normalize_text(
        collect_evidence_text(investigation_data)
    )

    supporting_evidence = analysis.get(
        "supporting_evidence", []
    )

    if isinstance(supporting_evidence, str):
        supporting_evidence = [supporting_evidence]

    results = []

    for claim in supporting_evidence:
        normalized_claim = normalize_text(str(claim))

        # Empty claims cannot be verified.
        supported = (
            bool(normalized_claim)
            and normalized_claim in evidence_text
        )

        results.append({
            "claim": str(claim),
            "status": (
                "supported"
                if supported
                else "unverified"
            ),
            "reason": (
                "Matching text found in incident evidence."
                if supported
                else (
                    "No exact text match found. "
                    "This does not prove the claim is false."
                ),
            ),
        })

    if not results:
        overall_status = "inconclusive"
    elif all(
        item["status"] == "supported"
        for item in results
    ):
        overall_status = "supported"
    elif any(
        item["status"] == "supported"
        for item in results
    ):
        overall_status = "partially_supported"
    else:
        overall_status = "inconclusive"

    return {
        "status": overall_status,
        "checked_claims": len(results),
        "supported_claims": sum(
            item["status"] == "supported"
            for item in results
        ),
        "claims": results,
    }
