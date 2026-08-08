# Espina v0.9.x - Multisurface CURRENT Extension Draft

Status: non-normative public draft candidate
Date: 2026-08-07

This folder is a clean draft candidate for a future Espina v0.9.x extension.

It contains only synthetic examples and public-facing schemas. It does not contain private Aster, Claudio, client, Drive, Bookshelf, or runtime material.

It is not v1.0 and is not a conformance requirement for Espina v0.9 implementations.

## Purpose

This draft extends Espina v0.9 with portable contracts for:

- explicit world registry;
- multisurface capability registry;
- CURRENT definition and continuity status;
- append-only CURRENT events;
- permission-separated update flow;
- degraded operation without false continuity.

## Contents

```text
README.md
ESPINA_v0.9x_MULTISURFACE_CURRENT_EXTENSION_DRAFT.md
ALBERTO_REVIEW_BRIEF.md
FREE_PRIVATE_BOUNDARY.md
schemas/
examples/ana_rc/
examples/lab_rc_installable_sanitized/
runtime/
tools/validate_rc_current.ps1
tools/validate_jsonschema.py
tools/validate_event_chain.py
tools/validate_drive_backend_minimal.py
tools/build_extension_manifest.py
reports/
reports/runtime_proofs/
reports/runtime_proofs/external_real_account_test_sanitized.md
MANIFEST.json
LICENSE-NOTES.md
PR_DRAFT.md
FORKS_AND_CONCURRENCY.md
DRIVE_BACKEND_MINIMAL.md
LLM_REENTRY_PLAYBOOK.md
```

## License

- Specification text and synthetic Markdown examples: CC BY 4.0, following the Espina specification text license.
- JSON schemas and structured synthetic examples: MIT, following the Espina tooling license, so implementers can copy them directly into validators and runtimes.
- Tools and scripts: MIT.

If a file mixes explanatory text and machine-readable structure, use the more permissive implementation path for the structured artifact and preserve attribution to Espina.

## Non-goals

This draft does not define a full product UX, sync engine, or commercial onboarding system.

It specifies contracts that an implementation may support and now includes a minimal installable runtime prototype for review.

## Installable Runtime Prototype

The `runtime/` folder contains a small reference prototype:

- `install_rc.py` creates a local RC runtime skeleton;
- `drive_current_generic.py` reads/appends to a remote CURRENT using an activation package and user-owned OAuth token;
- `surface_cli.py` wraps the connector as a minimal surface SDK/CLI;
- `privacy_export.py` emits an export/delete readiness manifest;
- `validate_installable_runtime.py` validates the prototype and sanitized lab proof reports.

The prototype is BYOK. It does not include OAuth secrets, OAuth tokens, private signing keys, or private memory.

## Sanitized External Account Proof

The private lab has also verified the installable runtime against a real external Google account with a separate user-owned Drive backend and OAuth setup. A sanitized public-review report is included at:

[`reports/runtime_proofs/external_real_account_test_sanitized.md`](reports/runtime_proofs/external_real_account_test_sanitized.md)

The report excludes live emails, Drive IDs, OAuth client IDs, OAuth secrets, tokens, private signing keys, and private memory.

## Validation

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "extensions/multisurface-current-v0.9x/tools/validate_rc_current.ps1" -ExamplePath "extensions/multisurface-current-v0.9x/examples/ana_rc"
python "extensions/multisurface-current-v0.9x/tools/validate_jsonschema.py"
python "extensions/multisurface-current-v0.9x/tools/validate_event_chain.py"
python "extensions/multisurface-current-v0.9x/runtime/validate_installable_runtime.py" "extensions/multisurface-current-v0.9x/runtime"
```

## Safety Rule

The extension does not claim subjective continuity. It preserves Espina v0.9's honesty clause:

> Activation is continuity of operational record, not proof of continuous subjective experience.
