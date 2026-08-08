import hashlib
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public_draft"
EXAMPLE = PUBLIC / "examples" / "ana_rc"
PACKAGE = EXAMPLE / "activation" / "activation_package_001.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def package_checksum(package):
    cloned = json.loads(json.dumps(package, ensure_ascii=False))
    cloned["package_metadata"]["package_checksum"] = ""
    canonical = dump_canonical(cloned)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_basic():
    world_registry = load_json(EXAMPLE / "espina" / "world_registry.json")
    surface_registry = load_json(EXAMPLE / "espina" / "surface_registry.json")
    current_contract = load_json(EXAMPLE / "espina" / "current_contract.json")
    current_pointer = load_json(EXAMPLE / "current" / "CURRENT_POINTER.json")
    current_state = load_json(EXAMPLE / "current" / "state" / "CURRENT_STATE.json")
    package = load_json(PACKAGE)

    checks = []
    checks.append(("rc_id", len({world_registry["rc_id"], surface_registry["rc_id"], current_contract["rc_id"], current_pointer["rc_id"], package["rc_id"]}) == 1))
    checks.append(("active_world_declared", current_state["active_world"] in world_registry["worlds"]))
    checks.append(("active_surface_declared", current_state["active_surface"] in surface_registry["surfaces"]))
    checks.append(("package_current_id", package["current_context"]["current_id"] == current_pointer["current_id"]))
    checks.append(("package_world_match", package["current_context"]["active_world"] == current_state["active_world"]))
    checks.append(("package_surface_match", package["current_context"]["active_surface"] == current_state["active_surface"]))
    checks.append(("object_count", package["package_metadata"]["object_count"] == len(package["retrieved_objects"])))
    checks.append(("safety_frame", all(package["safety_frame"].get(k) is True for k in [
        "is_context_not_mandate",
        "no_canonical_write",
        "separation_evid_inf_lim",
        "membrane_status_present",
        "provenance_required",
    ])))
    checks.append(("objects_passable", all(obj["membrane_status"] in {"PASS", "TRANSFORM"} for obj in package["retrieved_objects"])))
    checks.append(("object_worlds_declared", all(obj["world"] in world_registry["worlds"] for obj in package["retrieved_objects"])))
    return package, checks


def main():
    package, checks = validate_basic()
    checksum = package_checksum(package)
    if package["package_metadata"].get("package_checksum") != checksum:
        package["package_metadata"]["package_checksum"] = checksum
        PACKAGE.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "phase14_integrity_ana_rc.md"
    lines = [
        "# Phase 14 integrity report - Ana RC",
        "",
        f"Package: `{PACKAGE.relative_to(ROOT)}`",
        f"Package checksum: `{checksum}`",
        "",
        "## Checks",
        "",
    ]
    failed = 0
    for name, ok in checks:
        if not ok:
            failed += 1
        mark = "OK" if ok else "FAIL"
        lines.append(f"- {mark} `{name}`")
    lines.extend([
        "",
        "## JSON Schema",
        "",
        "Formal JSON Schema validation was not executed because Python `jsonschema` is not installed in this environment.",
        "Current validation covers canonical checksum and cross-file structural consistency.",
    ])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS" if failed == 0 else "FAIL",
        "failed": failed,
        "checksum": checksum,
        "report": str(report),
    }, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
