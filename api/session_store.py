"""
Persistent session store for streaming analysis sessions.
Saves to a JSON file so sessions survive process restarts.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Default path: api/.data/sessions.json (gitignored)
DEFAULT_SESSIONS_DIR = Path(__file__).resolve().parent / ".data"
DEFAULT_SESSIONS_FILE = DEFAULT_SESSIONS_DIR / "sessions.json"


def _get_sessions_path() -> Path:
    path = os.getenv("SESSIONS_FILE")
    if path:
        return Path(path)
    return DEFAULT_SESSIONS_FILE


def _load_sessions() -> Dict[str, Dict[str, Any]]:
    path = _get_sessions_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Could not load sessions from %s: %s", path, e)
        return {}


def _save_sessions(sessions: Dict[str, Dict[str, Any]]) -> None:
    path = _get_sessions_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        # Only persist serializable fields (no raw objects)
        out = {}
        for sid, data in sessions.items():
            out[sid] = {
                k: v
                for k, v in data.items()
                if isinstance(v, (str, int, float, bool, type(None), dict, list))
            }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
    except OSError as e:
        logger.warning("Could not save sessions to %s: %s", path, e)


class SessionStore:
    """In-memory session store with optional JSON file persistence."""

    def __init__(self, persist: bool = True):
        self._store: Dict[str, Dict[str, Any]] = _load_sessions()
        self._persist = persist

    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get(session_id)

    def __setitem__(self, session_id: str, data: Dict[str, Any]) -> None:
        self._store[session_id] = data
        if self._persist:
            _save_sessions(self._store)

    def __getitem__(self, session_id: str) -> Dict[str, Any]:
        return self._store[session_id]

    def __contains__(self, session_id: str) -> bool:
        return session_id in self._store

    def pop(self, session_id: str, default: Any = None) -> Any:
        value = self._store.pop(session_id, default)
        if self._persist:
            _save_sessions(self._store)
        return value

    def keys(self):
        return self._store.keys()

    def items(self):
        return self._store.items()

    def __len__(self) -> int:
        return len(self._store)

    def save(self) -> None:
        """Persist current in-memory store to file."""
        if self._persist:
            _save_sessions(self._store)
