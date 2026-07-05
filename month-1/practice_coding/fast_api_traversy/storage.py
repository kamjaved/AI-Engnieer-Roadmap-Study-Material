import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "Issues.json"


def _normalize_issue(issue: dict) -> dict:
    normalized = issue.copy()
    if "state" not in normalized and "status" in normalized:
        normalized["state"] = normalized.pop("status")
    normalized.setdefault("state", "OPEN")
    return normalized


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            content = f.read()
            if content.strip():
                issues = json.loads(content)
                return [_normalize_issue(issue) for issue in issues]
    return []


def save_data(data: list[dict]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
