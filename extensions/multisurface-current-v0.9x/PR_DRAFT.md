# Draft PR - Multisurface CURRENT extension

## Title

Add experimental multisurface CURRENT extension draft

## Summary

This PR adds a non-normative Espina v0.9.x extension draft for multisurface RC operation.

The extension defines portable contracts for:

- explicit world registry;
- surface and capability registry;
- CURRENT contract and continuity status;
- activation package structure;
- permission-separated update flow;
- append-only CURRENT event chain;
- fork detection and concurrency safety;
- minimal Drive-style backend pattern;
- LLM reentry playbook;
- installable runtime prototype;
- generic BYOK Drive connector;
- minimal surface CLI;
- revocation and privacy/export proof;
- degraded operation without false continuity.

It is intentionally scoped as an experimental draft. It does not define a production runtime, sync backend, product UX, commercial onboarding flow, or subjective-continuity claim.

## What Changed

- Added `extensions/multisurface-current-v0.9x/`.
- Added public-facing JSON Schemas for:
  - `world_registry`;
  - `surface_registry`;
  - `current_contract`;
  - `current_event`;
  - `activation_package`.
- Added a synthetic `ana_rc` example.
- Added validation tools:
  - structural RC/CURRENT validation;
  - JSON Schema validation;
  - append-only event chain validation;
  - minimal Drive-style backend validation;
  - extension manifest generation.
- Added `runtime/` with:
  - local RC installer;
  - generic Drive CURRENT connector;
  - surface CLI wrapper;
  - privacy/export manifest tool;
  - installable runtime validator.
- Added sanitized installable runtime example and lab proof reports.
- Added non-normative implementation notes:
  - `FORKS_AND_CONCURRENCY.md`;
  - `DRIVE_BACKEND_MINIMAL.md`;
  - `LLM_REENTRY_PLAYBOOK.md`.
- Added manifest with SHA-256 inventory.
- Added license notes for text, schemas, structured examples, and tooling.
- Added a README and changelog/root README pointers.

## Validation

Expected local checks before opening the PR:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "extensions/multisurface-current-v0.9x/tools/validate_rc_current.ps1" -ExamplePath "extensions/multisurface-current-v0.9x/examples/ana_rc"
python "extensions/multisurface-current-v0.9x/tools/validate_jsonschema.py"
python "extensions/multisurface-current-v0.9x/tools/validate_event_chain.py"
python "extensions/multisurface-current-v0.9x/tools/validate_drive_backend_minimal.py" "<path-to-ESPINA_RC_DRIVE_MINIMAL>"
python "extensions/multisurface-current-v0.9x/runtime/validate_installable_runtime.py" "extensions/multisurface-current-v0.9x/runtime"
python "extensions/multisurface-current-v0.9x/tools/build_extension_manifest.py" "extensions/multisurface-current-v0.9x"
```

Current local results:

```text
validate_rc_current.ps1: PASS, 9 checks, 0 failures
validate_jsonschema.py: PASS, 4 targets, 0 failures
validate_event_chain.py: PASS, 1 event, 0 failures
validate_drive_backend_minimal.py: PASS on private Aster Drive backend, 29 passes, 0 warnings, 0 failures
validate_installable_runtime.py: PASS_INSTALLABLE_RUNTIME_WITH_SANITIZED_LAB_PROOFS
```

## Privacy Review

The extension contains only synthetic examples and public-facing schemas.

Private Aster, Claudio, Drive, Bookshelf, client, and runtime material are excluded.

Current local privacy scan only returns negative exclusion statements in `README.md` and `LICENSE-NOTES.md`.

The new installable runtime example is sanitized: Drive ids are placeholders, and no OAuth token, client secret, private key, or private memory is included.

The private Aster Drive-minimal backend exists only outside this public extension and must not be copied into this PR:

```text
private/aster_drive_minimal/
```

## Licensing

Provisional policy:

- specification text and explanatory Markdown: CC BY 4.0;
- tools/scripts: MIT;
- JSON Schemas: MIT;
- structured JSON/JSONL synthetic examples: MIT;
- synthetic Markdown examples: CC BY 4.0.

This should be reviewed before merge if the repository has stricter licensing conventions.

## Risks

- The extension may be mistaken for a normative Espina v1.0 requirement if not clearly labeled as draft.
- JSON Schema validation currently covers the main JSON artifacts, not every possible runtime object.
- The append-only chain validates hash continuity and the draft documents fork handling, but production fork reconciliation remains runtime-specific.
- The minimal Drive backend is a folder contract and validator, not a Google Drive API connector.
- The LLM reentry playbook is an operational guide, not an autonomous runtime.
- The manifest provides integrity evidence, but not cryptographic signing by a human authority.
- Terminology around `CURRENT`, `surface`, `room`, and `center_profile` may need broader review before public stabilization.

## Out Of Scope

- Production sync engine.
- Google Drive connector.
- Production Google Drive connector with bundled credentials.
- Mobile or desktop product UX.
- Runtime authority management.
- Human signing workflow.
- Production fork resolution protocol.
- Commercial Aster RC Technologies implementation.
- Private Aster Drive backend.

## Reviewer Checklist

- [ ] Confirm the extension is clearly marked as non-normative draft.
- [ ] Confirm no private material is present.
- [ ] Confirm license notes are compatible with repository policy.
- [ ] Run structural validator.
- [ ] Run JSON Schema validator.
- [ ] Run append-only event chain validator.
- [ ] Run Drive backend minimal validator against a local/private folder only.
- [ ] Confirm `private/aster_drive_minimal/` is not present in the PR.
- [ ] Review terminology for `CURRENT`, `surface`, `room`, `engine`, and `center_profile`.
- [ ] Decide whether this remains v0.9.x extension or becomes part of a future v1.0 proposal.

## Publication Decision

Prepared only.

No push.
No PR opened.
No publication action taken.
