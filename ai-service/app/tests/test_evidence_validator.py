
from app.agents.evidence_validator import validate_evidence


def test_claim_matching_evidence_is_supported():
    evidence = {
        "logs": ["Database connection timeout occurred"]
    }
    analysis = {
        "supporting_evidence": [
            "Database connection timeout occurred"
        ]
    }

    result = validate_evidence(analysis, evidence)

    assert result["status"] == "supported"
    assert result["checked_claims"] == 1
    assert result["supported_claims"] == 1
    assert result["claims"][0]["status"] == "supported"


def test_claim_not_found_is_unverified():
    evidence = {"logs": ["Database connection timeout occurred"]}
    analysis = {
        "supporting_evidence": ["Payment service crashed"]
    }

    result = validate_evidence(analysis, evidence)

    assert result["status"] == "inconclusive"
    assert result["supported_claims"] == 0
    assert result["claims"][0]["status"] == "unverified"


def test_partially_supported_claims():
    evidence = {
        "logs": [
            "Database connection timeout occurred",
            "Request failed with status 500"
        ]
    }
    analysis = {
        "supporting_evidence": [
            "Database connection timeout occurred",
            "Payment service was restarted"
        ]
    }

    result = validate_evidence(analysis, evidence)

    assert result["status"] == "partially_supported"
    assert result["checked_claims"] == 2
    assert result["supported_claims"] == 1


def test_empty_claims_are_inconclusive():
    evidence = {"logs": ["Request failed"]}
    analysis = {"supporting_evidence": []}

    result = validate_evidence(analysis, evidence)

    assert result["status"] == "inconclusive"
    assert result["checked_claims"] == 0


def test_string_claim_is_supported():
    evidence = {"logs": ["Database connection timeout occurred"]}
    analysis = {
        "supporting_evidence": "Database connection timeout occurred"
    }

    result = validate_evidence(analysis, evidence)

    assert result["status"] == "supported"
    assert result["checked_claims"] == 1
