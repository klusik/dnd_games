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



def validate_modules(directory, state):
    """Validate the referenced modular snapshot without requiring modules in legacy saves.

    :param directory: Campaign directory.
    :param state: Loaded snapshot manifest.
    """
    errors = []
    loaded = {}
    active = set()
    item_ids = set()
    campaign_id = state["campaign_id"]

    def visit(reference, expected_id=None, owner=None):
        """Resolve a campaign-local JSON module and validate its contents.

        :param reference: Relative module path.
        :param expected_id: Expected entity ID, if applicable.
        :param owner: Expected inventory owner, if applicable.
        """
        if not isinstance(reference, str):
            errors.append(f"{campaign_id}: non-string module reference")
            return
        path = Path(reference)
        if path.is_absolute() or ".." in path.parts or path.suffix != ".json":
            errors.append(f"{campaign_id}: unsafe module reference {reference}")
            return
        target = (directory / path).resolve()
        if not target.is_relative_to(directory.resolve()):
            errors.append(f"{campaign_id}: unsafe module reference {reference}")
            return
        if target in active:
            errors.append(f"{campaign_id}: module cycle at {reference}")
            return
        if target in loaded:
            data = loaded[target]
        else:
            try:
                data = load_json(target)
            except (OSError, ValueError) as exc:
                errors.append(f"{campaign_id}: cannot read module {reference}: {exc}")
                return
            if not isinstance(data, dict):
                errors.append(f"{campaign_id}: invalid module {reference}")
                return
            loaded[target] = data
            if data.get("campaign_id") != campaign_id or data.get("schema_version") != 1 or not data.get("id") or not data.get("kind"):
                errors.append(f"{campaign_id}: invalid module identity {reference}")
            hp = data.get("hp")
            if isinstance(hp, dict):
                current, maximum = hp.get("current"), hp.get("max")
                if current is not None and maximum is not None and not 0 <= current <= maximum:
                    errors.append(f"{campaign_id}: HP outside bounds in {reference}")
            if data.get("kind") == "inventory":
                for item in data.get("items", []):
                    identifier = item["id"]
                    if identifier in item_ids:
                        errors.append(f"{campaign_id}: duplicate inventory item {identifier}")
                    item_ids.add(identifier)
                    quantity = item.get("quantity")
                    if quantity is not None and (type(quantity) not in (int, float) or quantity < 0):
                        errors.append(f"{campaign_id}: invalid inventory quantity {identifier}")
                    if item.get("status") not in {"equipped", "carried", "confirmed", "last_known", "provisional", "historical_unverified", "used", "installed", "not_acquired"}:
                        errors.append(f"{campaign_id}: invalid inventory status {identifier}")
                    if not item.get("source"):
                        errors.append(f"{campaign_id}: missing inventory provenance {identifier}")
            active.add(target)
            walk(data)
            active.remove(target)
        if expected_id is not None and data.get("id") != expected_id:
            errors.append(f"{campaign_id}: module ID mismatch {reference}")
        if owner is not None and data.get("owner") != owner:
            errors.append(f"{campaign_id}: inventory owner mismatch {reference}")

    def walk(value):
        """Traverse explicit reference keys and nested containers.

        :param value: JSON value.
        """
        if isinstance(value, list):
            for entry in value:
                walk(entry)
        elif isinstance(value, dict):
            for key, entry in value.items():
                if key in {"ref", "sheet_ref"} and entry is not None:
                    visit(entry, expected_id=value.get("id"))
                elif key == "inventory_ref" and entry is not None:
                    owner = value.get("id") if "sheet_ref" in value or value.get("kind") == "character_sheet" else None
                    visit(entry, owner=owner)
                elif key in {"roster_ref", "archive_ref"} and entry is not None:
                    visit(entry)
                elif key == "inventory_refs" and isinstance(entry, dict):
                    for reference in entry.values():
                        visit(reference)
                elif key == "audit_ref":
                    if entry != "audit.md" or not (directory / entry).is_file():
                        errors.append(f"{campaign_id}: missing or invalid audit reference")
                else:
                    walk(entry)

    if state.get("layout_version", 1) == 2:
        if not state.get("character", {}).get("sheet_ref"):
            errors.append(f"{campaign_id}: missing player sheet reference")
        walk(state)
    elif state.get("layout_version", 1) != 1:
        errors.append(f"{campaign_id}: unsupported layout version")
    return errors


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
            errors.extend(validate_modules(directory, state))
            if state.get("layout_version", 1) == 2 and state.get("status") != item.get("status"):
                errors.append(f"{campaign_id}: registry status mismatch")
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
