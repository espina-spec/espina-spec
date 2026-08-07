import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXT = ROOT / "public_draft"


def sha256_file(path: pathlib.Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(data) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def build_manifest(extension_path: pathlib.Path) -> dict:
    files = []
    for path in sorted(extension_path.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(extension_path).as_posix()
        if rel == "MANIFEST.json":
            continue
        files.append({
            "path": rel,
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })

    manifest = {
        "manifest_id": "manifest_espina_v09x_multisurface_current_draft_20260807",
        "manifest_version": "v0.9x-draft",
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "created_by": "build_extension_manifest.py",
        "scope": "Espina v0.9.x Multisurface CURRENT Extension Draft",
        "private_material_excluded": True,
        "files": files,
    }
    checksum = hashlib.sha256(canonical_json(manifest).encode("utf-8")).hexdigest()
    manifest["manifest_checksum"] = "sha256:" + checksum
    return manifest


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else EXT
    target = target.resolve()
    manifest = build_manifest(target)
    out = target / "MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "manifest": str(out),
        "files": len(manifest["files"]),
        "manifest_checksum": manifest["manifest_checksum"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
