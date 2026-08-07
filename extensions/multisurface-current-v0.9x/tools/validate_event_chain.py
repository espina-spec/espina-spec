import hashlib
import json
import pathlib
import sys

try:
    import jsonschema
except ImportError:
    jsonschema = None


ROOT = pathlib.Path(__file__).resolve().parents[1]
EVENT_SCHEMA = ROOT / "schemas" / "current_event.schema.json"
DEFAULT_EVENTS = ROOT / "examples" / "ana_rc" / "current" / "events" / "2026-08-07.jsonl"
REPORT = ROOT / "reports" / "phase23_event_chain_validation.md"


def canonical_event_payload(event: dict) -> str:
    payload = dict(event)
    payload.pop("event_hash", None)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def event_hash(event: dict) -> str:
    canonical = canonical_event_payload(event)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_jsonl(path: pathlib.Path) -> list[dict]:
    events = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
        event["_line_number"] = line_number
        events.append(event)
    return events


def validate_chain(events_path: pathlib.Path) -> tuple[list[str], list[str]]:
    errors = []
    notes = []

    schema = json.loads(EVENT_SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema) if jsonschema else None
    if not validator:
        errors.append("jsonschema is not installed")
        return notes, errors

    events = load_jsonl(events_path)
    previous = None
    seen_ids = set()

    for index, event in enumerate(events):
        line_number = event.pop("_line_number")

        schema_errors = sorted(validator.iter_errors(event), key=lambda err: list(err.path))
        for err in schema_errors:
            path = ".".join(str(part) for part in err.path) or "<root>"
            errors.append(f"line {line_number}: schema error at {path}: {err.message}")

        event_id = event.get("event_id")
        if event_id in seen_ids:
            errors.append(f"line {line_number}: duplicate event_id {event_id}")
        seen_ids.add(event_id)

        expected_previous = None if index == 0 else previous
        if event.get("previous_hash") != expected_previous:
            errors.append(
                f"line {line_number}: previous_hash mismatch; "
                f"expected {expected_previous}, found {event.get('previous_hash')}"
            )

        computed = event_hash(event)
        if event.get("event_hash") != computed:
            errors.append(
                f"line {line_number}: event_hash mismatch; "
                f"expected {computed}, found {event.get('event_hash')}"
            )

        previous = computed
        notes.append(f"PASS line {line_number}: {event_id} -> {computed}")

    if not events:
        errors.append("event chain is empty")

    return notes, errors


def write_report(events_path: pathlib.Path, notes: list[str], errors: list[str]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not errors else "FAIL"
    lines = [
        "# Phase 23 event chain validation",
        "",
        f"Status: {status}",
        f"Events file: `{events_path.relative_to(ROOT)}`",
        f"Events checked: {len(notes)}",
        f"Failures: {len(errors)}",
        "",
        "## Chain",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    if errors:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {error}" for error in errors)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    events_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_EVENTS
    events_path = events_path.resolve()
    notes, errors = validate_chain(events_path)
    write_report(events_path, notes, errors)
    print(json.dumps({
        "status": "PASS" if not errors else "FAIL",
        "events": len(notes),
        "failures": len(errors),
        "report": str(REPORT),
    }, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
