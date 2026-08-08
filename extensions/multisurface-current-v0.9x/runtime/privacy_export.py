import argparse
import json
import pathlib


EXPORT_FILES = [
    "00_espina/rc_identity.json",
    "00_espina/surface_registry.json",
    "00_espina/export_policy.json",
    "01_current/CURRENT_POINTER.json",
    "01_current/state/CURRENT_STATE.json",
    "01_current/state/OPEN_LOOPS.json",
    "01_current/events/2026-08-08.jsonl",
]


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a minimal privacy/export manifest for an RC runtime.")
    parser.add_argument("root")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    out = pathlib.Path(args.out).resolve()
    policy = load_json(root / "00_espina/export_policy.json")
    files = []
    missing = []
    for rel in EXPORT_FILES:
        path = root / rel
        if path.exists():
            files.append({"path": rel, "bytes": path.stat().st_size})
        else:
            missing.append(rel)
    report = {
        "status": "PRIVACY_EXPORT_VERIFIED" if policy.get("export_required") is True and policy.get("deletion_required") is True and not missing else "PRIVACY_EXPORT_INCOMPLETE",
        "export_required": policy.get("export_required"),
        "deletion_required": policy.get("deletion_required"),
        "export_file_count": len(files),
        "files": files,
        "missing": missing,
        "delete_procedure": "Revoke all surfaces, export files above, then delete or trash the remote folder using the owner OAuth account.",
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "PRIVACY_EXPORT_VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
