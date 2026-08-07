import json
import pathlib
import sys

from jsonschema import Draft202012Validator


ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public_draft" if (ROOT / "public_draft").exists() else ROOT
SCHEMAS = PUBLIC / "schemas"
EXAMPLE = PUBLIC / "examples" / "ana_rc"


VALIDATION_TARGETS = [
    ("world_registry", SCHEMAS / "world_registry.schema.json", EXAMPLE / "espina" / "world_registry.json"),
    ("surface_registry", SCHEMAS / "surface_registry.schema.json", EXAMPLE / "espina" / "surface_registry.json"),
    ("current_contract", SCHEMAS / "current_contract.schema.json", EXAMPLE / "espina" / "current_contract.json"),
    ("activation_package", SCHEMAS / "activation_package.schema.json", EXAMPLE / "activation" / "activation_package_001.json"),
]


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    results = []
    failures = 0
    for name, schema_path, instance_path in VALIDATION_TARGETS:
        schema = load_json(schema_path)
        instance = load_json(instance_path)
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
        if errors:
            failures += 1
            results.append({
                "name": name,
                "status": "FAIL",
                "schema": str(schema_path.relative_to(ROOT)),
                "instance": str(instance_path.relative_to(ROOT)),
                "errors": [
                    {
                        "path": "/".join(str(part) for part in error.path),
                        "message": error.message,
                    }
                    for error in errors
                ],
            })
        else:
            results.append({
                "name": name,
                "status": "PASS",
                "schema": str(schema_path.relative_to(ROOT)),
                "instance": str(instance_path.relative_to(ROOT)),
                "errors": [],
            })

    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    report = report_dir / "phase22_jsonschema_validation.md"
    lines = [
        "# Phase 22 JSON Schema validation",
        "",
        f"Status: {'PASS' if failures == 0 else 'FAIL'}",
        f"Targets: {len(results)}",
        f"Failures: {failures}",
        "",
        "## Results",
        "",
    ]
    for result in results:
        lines.append(f"- {result['status']} `{result['name']}`")
        lines.append(f"  - schema: `{result['schema']}`")
        lines.append(f"  - instance: `{result['instance']}`")
        for error in result["errors"]:
            lines.append(f"  - error at `{error['path']}`: {error['message']}")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "PASS" if failures == 0 else "FAIL",
        "targets": len(results),
        "failures": failures,
        "report": str(report),
    }, indent=2))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
