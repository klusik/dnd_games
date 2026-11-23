"""Validate independent campaign snapshots and immutable event numbering.

Author: Rudolf Klusal
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    """Read a UTF-8 JSON document.

    :param path: Path to the JSON file.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root=ROOT):
    """Return structural and revision-chain validation errors.

    :param root: Root directory of the campaign repository.
    """
    errors = []
    try:
        registry = load_json(root / "campaigns/index.json")
        if registry["schema_version"] != 1:
            errors.append("Unsupported registry schema")
        seen = set()
        for item in registry["campaigns"]:
            campaign_id = item["id"]
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", campaign_id):
                errors.append(f"Invalid ID: {campaign_id}")
                continue
            if campaign_id in seen:
                errors.append(f"Duplicate ID: {campaign_id}")
            seen.add(campaign_id)
            expected_path = f"campaigns/{campaign_id}"
            if item["path"] != expected_path:
                errors.append(f"{campaign_id}: invalid path")
                continue
            directory = root / expected_path
            for filename in ("rules.md", "history.md", "knowledge.md", "sources.md"):
                if not (directory / filename).is_file():
                    errors.append(f"{campaign_id}: missing {filename}")
            state = load_json(directory / "state.json")
            revision = state["revision"]
            if type(revision) is not int or revision < 0:
                errors.append(f"{campaign_id}: invalid revision")
                continue
            if state["campaign_id"] != campaign_id or state["schema_version"] != 1:
                errors.append(f"{campaign_id}: invalid snapshot identity")
            if state["last_event"] != f"{revision:06d}":
                errors.append(f"{campaign_id}: last_event mismatch")
            for key in ("scene", "character", "world", "objectives", "uncertainties"):
                if key not in state:
                    errors.append(f"{campaign_id}: missing {key}")
            files = sorted((directory / "events").glob("*.json"))
            if len(files) != revision + 1:
                errors.append(f"{campaign_id}: event count mismatch")
            for index, path in enumerate(files):
                event = load_json(path)
                previous = index - 1 if index else None
                if (
                    path.stem != f"{index:06d}"
                    or event["revision"] != index
                    or event["previous_revision"] != previous
                    or event["campaign_id"] != campaign_id
                    or event["schema_version"] != 1
                ):
                    errors.append(f"{campaign_id}: invalid event chain at {path.name}")
                for key in ("player_action", "dm_response", "rolls", "changes", "sources"):
                    if key not in event:
                        errors.append(f"{campaign_id}: missing {key} in {path.name}")
            objectives = state.get("objectives", [])
            identifiers = [objective["id"] for objective in objectives]
            if len(identifiers) != len(set(identifiers)):
                errors.append(f"{campaign_id}: duplicate objective")
            hp = state.get("character", {}).get("hp", {})
            current, maximum = hp.get("current"), hp.get("max")
            if current is not None and maximum is not None and not 0 <= current <= maximum:
                errors.append(f"{campaign_id}: HP outside bounds")
        if registry["default_campaign"] not in seen:
            errors.append("Default campaign not registered")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid data: {exc}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print("All campaign snapshots and event chains valid.")
