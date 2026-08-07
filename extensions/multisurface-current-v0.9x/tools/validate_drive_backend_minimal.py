import json
import pathlib
import sys


ALLOWED_CONTINUITY = {
    "CONTINUITY_OK",
    "CONTINUITY_PARTIAL",
    "CURRENT_STALE",
    "CURRENT_DIVERGENT",
    "CURRENT_UNKNOWN",
    "DEGRADED_MODE",
    "BLOCKED",
}

SAFE_WITHOUT_HEAD = {
    "CONTINUITY_PARTIAL",
    "CURRENT_STALE",
    "CURRENT_DIVERGENT",
    "CURRENT_UNKNOWN",
    "DEGRADED_MODE",
    "BLOCKED",
}


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_exists(root: pathlib.Path, rel: str, failures: list[str], passes: list[str]) -> pathlib.Path:
    path = root / rel
    if path.exists():
        passes.append(f"exists {rel}")
    else:
        failures.append(f"missing {rel}")
    return path


def validate(root: pathlib.Path) -> tuple[list[str], list[str], list[str]]:
    passes = []
    warnings = []
    failures = []

    required_dirs = [
        "00_espina",
        "01_current",
        "01_current/state",
        "01_current/events",
        "01_current/proposals",
        "02_activation",
        "03_reports",
        "04_tools",
    ]
    for rel in required_dirs:
        path = root / rel
        if path.is_dir():
            passes.append(f"dir {rel}")
        else:
            failures.append(f"missing directory {rel}")

    pointer_path = check_exists(root, "01_current/CURRENT_POINTER.json", failures, passes)
    check_exists(root, "DRIVE_BACKEND_PROTOCOL.md", failures, passes)
    check_exists(root, "README.md", failures, passes)

    pointer = {}
    if pointer_path.exists():
        try:
            pointer = load_json(pointer_path)
            passes.append("pointer_json_parse")
        except Exception as exc:
            failures.append(f"pointer_json_parse failed: {exc}")

    for key in [
        "rc_id",
        "state_path",
        "continuity_path",
        "open_loops_path",
        "latest_events_path",
        "accepted_head",
        "continuity_status",
    ]:
        if key in pointer:
            passes.append(f"pointer_has {key}")
        else:
            failures.append(f"pointer missing {key}")

    continuity_status = pointer.get("continuity_status")
    accepted_head = pointer.get("accepted_head")
    if continuity_status in ALLOWED_CONTINUITY:
        passes.append(f"pointer_continuity_allowed {continuity_status}")
    elif continuity_status is not None:
        failures.append(f"pointer continuity_status not allowed: {continuity_status}")

    if accepted_head is None and continuity_status == "CONTINUITY_OK":
        failures.append("CONTINUITY_OK is not allowed when accepted_head is null")
    elif accepted_head is None and continuity_status in SAFE_WITHOUT_HEAD:
        passes.append("no_head_continuity_safe")

    for pointer_key in ["state_path", "continuity_path", "open_loops_path", "latest_events_path"]:
        rel = pointer.get(pointer_key)
        if not rel:
            continue
        target = root / rel
        if target.exists():
            passes.append(f"pointer_target_exists {pointer_key}")
        else:
            failures.append(f"pointer target missing for {pointer_key}: {rel}")

    for pointer_key in ["state_path", "continuity_path", "open_loops_path"]:
        rel = pointer.get(pointer_key)
        if not rel:
            continue
        target = root / rel
        if target.exists():
            try:
                data = load_json(target)
                passes.append(f"json_parse {pointer_key}")
                if data.get("rc_id") and pointer.get("rc_id") and data.get("rc_id") != pointer.get("rc_id"):
                    failures.append(f"rc_id mismatch in {rel}")
            except Exception as exc:
                failures.append(f"json_parse failed for {rel}: {exc}")

    events_rel = pointer.get("latest_events_path")
    if events_rel:
        events_path = root / events_rel
        if events_path.exists():
            lines = [line for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if lines:
                passes.append(f"events_present count={len(lines)}")
            else:
                warnings.append("latest event log is empty; CONTINUITY_OK requires a verified accepted_head")

    if not (root / "00_espina" / "world_registry.json").exists():
        warnings.append("00_espina/world_registry.json is not present in template")
    if not (root / "00_espina" / "surface_registry.json").exists():
        warnings.append("00_espina/surface_registry.json is not present in template")
    if not (root / "00_espina" / "current_contract.json").exists():
        warnings.append("00_espina/current_contract.json is not present in template")

    return passes, warnings, failures


def write_report(root: pathlib.Path, passes: list[str], warnings: list[str], failures: list[str]) -> pathlib.Path:
    report = root / "03_reports" / "drive_backend_minimal_validation.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Drive backend minimal validation",
        "",
        f"Status: {status}",
        f"Root: `{root}`",
        f"Passes: {len(passes)}",
        f"Warnings: {len(warnings)}",
        f"Failures: {len(failures)}",
        "",
        "## Passes",
        "",
    ]
    lines.extend(f"- {item}" for item in passes)
    if warnings:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in warnings)
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {item}" for item in failures)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_drive_backend_minimal.py <ESPINA_RC_DRIVE_MINIMAL>")
        return 2
    root = pathlib.Path(sys.argv[1]).resolve()
    passes, warnings, failures = validate(root)
    report = write_report(root, passes, warnings, failures)
    print(json.dumps({
        "status": "PASS" if not failures else "FAIL",
        "passes": len(passes),
        "warnings": len(warnings),
        "failures": len(failures),
        "report": str(report),
    }, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
