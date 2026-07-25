#!/usr/bin/env python3
"""
verificar.py — Script de verificación offline para la espina de ejemplo Ana N.
Adaptado del Paso 4 de A.5 de ESPINA v0.9.

Uso:
    python tools/verificar.py

El script verifica:
  1. Los 12 hashes SHA-256 de los ficheros de espina-ana-n/
  2. El manifest_checksum del manifiesto
  3. Ausencia de ficheros huérfanos (ficheros en disco no listados en manifiesto)

Requisitos: Python 3.7+
"""

import hashlib
import json
import os
import sys


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESPINA_DIR = os.path.join(REPO_ROOT, "espina-ana-n")
MANIFEST_PATH = os.path.join(ESPINA_DIR, "06-provenance", "manifest.json")


def normalize_lf(data: bytes) -> bytes:
    """Normaliza a LF, sin BOM, con un único salto de línea final."""
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    data = data.replace(b"\r\n", b"\n")
    return data.rstrip(b"\n") + b"\n"


def verify_file_hashes(manifest: dict) -> bool:
    """Verifica que los hashes de todos los ficheros coincidan."""
    ok = True
    for entry in manifest["files"]:
        path = os.path.join(ESPINA_DIR, entry["path"])
        if not os.path.exists(path):
            print(f"  FALTA: {entry['path']}")
            ok = False
            continue
        raw = open(path, "rb").read()
        raw = normalize_lf(raw)
        h = "sha256:" + hashlib.sha256(raw).hexdigest()
        if h == entry["sha256"]:
            print(f"  OK:    {entry['path']}")
        else:
            print(f"  FAIL:  {entry['path']}")
            print(f"         esperado: {entry['sha256']}")
            print(f"         obtenido: {h}")
            ok = False
    return ok


def verify_manifest_checksum(manifest: dict) -> bool:
    """Verifica el manifest_checksum recalculando el hash del manifiesto sin ese campo."""
    m2 = {k: v for k, v in manifest.items() if k != "manifest_checksum"}
    canonical = json.dumps(m2, sort_keys=True, separators=(",", ":"))
    checksum = "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if checksum == manifest["manifest_checksum"]:
        print(f"  OK:    manifest_checksum")
        return True
    else:
        print(f"  FAIL:  manifest_checksum")
        print(f"         esperado: {manifest['manifest_checksum']}")
        print(f"         obtenido: {checksum}")
        return False


def detect_orphans(manifest: dict) -> bool:
    """Detecta ficheros presentes en disco pero ausentes en el manifiesto."""
    manifest_paths = {entry["path"] for entry in manifest["files"]}
    ok = True
    for root, _dirs, files in os.walk(ESPINA_DIR):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ESPINA_DIR).replace(os.sep, "/")
            # El manifiesto no se lista a si mismo en el array de ficheros
            if rel == "06-provenance/manifest.json":
                continue
            if rel not in manifest_paths:
                print(f"  ORFANO: {rel}")
                ok = False
                print(f"  ORFANO: {rel}")
                ok = False
    if ok:
        print("  OK:    ningún fichero huérfano detectado")
    return ok


def main() -> int:
    print("=" * 60)
    print("ESPINA v0.9 — Verificación offline de espina-ana-n/")
    print("=" * 60)

    if not os.path.exists(MANIFEST_PATH):
        print(f"ERROR: No se encuentra el manifiesto: {MANIFEST_PATH}")
        return 1

    manifest = json.load(open(MANIFEST_PATH, "r", encoding="utf-8"))

    print("\n[1/3] Verificando hashes de ficheros...")
    files_ok = verify_file_hashes(manifest)

    print("\n[2/3] Verificando manifest_checksum...")
    checksum_ok = verify_manifest_checksum(manifest)

    print("\n[3/3] Detectando ficheros huérfanos...")
    orphans_ok = detect_orphans(manifest)

    print("\n" + "=" * 60)
    if files_ok and checksum_ok and orphans_ok:
        print("RESULTADO: Todos los hashes coinciden.")
        print(f"  Ficheros verificados: {len(manifest['files'])}/{len(manifest['files'])}")
        print(f"  manifest_checksum:    {manifest['manifest_checksum']}")
        print("  Estado: OK")
        print("=" * 60)
        return 0
    else:
        print("RESULTADO: VERIFICACIÓN FALLIDA.")
        print("  Revisa los mensajes FAIL/ORFANO arriba.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
