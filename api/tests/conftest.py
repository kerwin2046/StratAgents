"""Pytest fixtures: mock LLM and isolate session storage for tests."""
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure api directory is on path so "from app import app" works
_api_dir = Path(__file__).resolve().parent.parent
if str(_api_dir) not in sys.path:
    sys.path.insert(0, str(_api_dir))

# Avoid loading real keys; use temp session file so tests don't touch .data/
os.environ.pop("DEEPSEEK_API_KEY", None)
_tmpdir = tempfile.mkdtemp()
os.environ["SESSIONS_FILE"] = os.path.join(_tmpdir, "sessions.json")


@pytest.fixture(autouse=True)
def mock_get_llm_model():
    """Mock get_llm_model so startup and /status succeed without DEEPSEEK_API_KEY."""
    with patch("app.get_llm_model") as m:
        m.return_value = MagicMock()
        yield m
