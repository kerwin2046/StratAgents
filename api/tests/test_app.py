"""API endpoint tests."""
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Apply env before importing app so CORS_ORIGINS is set for tests
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")

from app import app

client = TestClient(app)


def test_health():
    """GET /health returns healthy status."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_status():
    """GET /status returns api and llm status (mocked)."""
    r = client.get("/status")
    assert r.status_code == 200
    data = r.json()
    assert data["api_status"] == "running"
    assert "llm_status" in data
    assert "active_sessions" in data
    assert "timestamp" in data


def test_demo_scenarios():
    """GET /demo-scenarios returns scenario list."""
    r = client.get("/demo-scenarios")
    assert r.status_code == 200
    data = r.json()
    assert "scenarios" in data
    assert len(data["scenarios"]) >= 1
    assert "name" in data["scenarios"][0]
    assert "website" in data["scenarios"][0]


def test_sessions_empty_or_persisted():
    """GET /sessions returns active_sessions and sessions dict."""
    r = client.get("/sessions")
    assert r.status_code == 200
    data = r.json()
    assert "active_sessions" in data
    assert "sessions" in data
    assert isinstance(data["sessions"], dict)


def test_analyze_requires_post():
    """POST /analyze with valid body is accepted (workflow mocked)."""
    with patch("app.MultiAgentCompetitiveIntelligence") as mock_ci:
        mock_instance = MagicMock()
        mock_instance.run_competitive_intelligence_workflow.return_value = {
            "competitor": "TestCo",
            "website": "https://test.com",
            "research_findings": "findings",
            "strategic_analysis": "analysis",
            "final_report": "report",
            "timestamp": "2025-01-01T00:00:00",
            "status": "success",
            "workflow": "multi_agent",
        }
        mock_ci.return_value = mock_instance

        r = client.post(
            "/analyze",
            json={
                "competitor_name": "TestCo",
                "competitor_website": "https://test.com",
                "stream": False,
            },
        )
        assert r.status_code == 200
        data = r.json()
        assert data["competitor"] == "TestCo"
        assert data["status"] == "success"
        assert data["final_report"] == "report"
