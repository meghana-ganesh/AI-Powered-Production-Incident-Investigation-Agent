
import json
from unittest.mock import patch, MagicMock

import pytest

from app.agents import incident_graph as graph_module


def test_fetch_evidence_returns_backend_data():
    expected_data = {
        "logs": ["Database timeout"],
        "metrics": [],
        "deployments": []
    }

    with patch.object(
        graph_module,
        "get_investigation_data",
        return_value=expected_data
    ) as mock_backend:
        result = graph_module.fetch_evidence({"incident_id": 123})

    mock_backend.assert_called_once_with(123)
    assert result["investigation_data"] == expected_data


def test_fetch_evidence_propagates_backend_failure():
    with patch.object(
        graph_module,
        "get_investigation_data",
        side_effect=ConnectionError("Backend unavailable")
    ):
        with pytest.raises(ConnectionError, match="Backend unavailable"):
            graph_module.fetch_evidence({"incident_id": 123})


def test_synthesize_findings_rejects_invalid_json():
    state = {
        "investigation_data": {"logs": ["Database timeout"]},
        "log_analysis": "Database timeout found",
        "metrics_analysis": "No metrics provided",
        "deployment_analysis": "No deployment data provided"
    }

    mock_response = MagicMock()
    mock_response.content = "This is not valid JSON"

    with patch.object(graph_module, "ChatOllama") as mock_llm:
        mock_llm.return_value.invoke.return_value = mock_response

        with pytest.raises((json.JSONDecodeError, ValueError)):
            graph_module.synthesize_findings(state)
