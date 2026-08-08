import argparse
import json
import pathlib


REQUIRED = [
    "README.md",
    "install_rc.py",
    "drive_current_generic.py",
    "surface_cli.py",
    "validate_installable_runtime.py",
]


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RC_RUNTIME_INSTALLABLE.")
    parser.add_argument("root")
    parser.add_argument("--extension-root")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    extension = pathlib.Path(args.extension_root).resolve() if args.extension_root else root.parent
    passes, warnings, failures = [], [], []
    for rel in REQUIRED:
        if (root / rel).exists():
            passes.append(f"exists:{rel}")
        else:
            failures.append(f"missing:{rel}")
    checks = {
        "activation_package_example": extension / "examples/lab_rc_installable_sanitized/activation_package.example.json",
        "generic_read_report": extension / "reports/runtime_proofs/installable_generic_read_current.json",
        "generic_append_report": extension / "reports/runtime_proofs/installable_surface_append.json",
        "revocation_report": extension / "reports/runtime_proofs/installable_revoked_surface_blocked.json",
        "privacy_export_report": extension / "reports/runtime_proofs/installable_privacy_export.json",
        "free_private_boundary": extension / "FREE_PRIVATE_BOUNDARY.md",
    }
    for name, path in checks.items():
        if path.exists():
            passes.append(f"{name}:exists")
        else:
            warnings.append(f"{name}:missing")
    append_report = checks["generic_append_report"]
    if append_report.exists() and load_json(append_report).get("status") == "GENERIC_APPEND_VERIFIED":
        passes.append("generic_surface_append_verified:true")
    revoke_report = checks["revocation_report"]
    if revoke_report.exists() and load_json(revoke_report).get("status") == "SURFACE_REVOKED_BLOCKED_VERIFIED":
        passes.append("surface_revocation_verified:true")
    export_report = checks["privacy_export_report"]
    if export_report.exists() and load_json(export_report).get("status") == "PRIVACY_EXPORT_VERIFIED":
        passes.append("privacy_export_verified:true")
    status = "PASS_INSTALLABLE_RUNTIME_WITH_SANITIZED_LAB_PROOFS" if not failures else "FAIL"
    report = {"status": status, "passes": len(passes), "warnings": len(warnings), "failures": len(failures), "pass_items": passes, "warning_items": warnings, "failure_items": failures}
    if args.write_report:
        out = root / "installable_runtime_validation.json"
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
