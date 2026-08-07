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
  - extension manifest generation.
- Added manifest with SHA-256 inventory.
- Added license notes for text, schemas, structured examples, and tooling.
- Added a README and changelog/root README pointers.

## Validation

Expected local checks before opening the PR:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "extensions/multisurface-current-v0.9x/tools/validate_rc_current.ps1" -ExamplePath "extensions/multisurface-current-v0.9x/examples/ana_rc"
python "extensions/multisurface-current-v0.9x/tools/validate_jsonschema.py"
python "extensions/multisurface-current-v0.9x/tools/validate_event_chain.py"
python "extensions/multisurface-current-v0.9x/tools/build_extension_manifest.py" "extensions/multisurface-current-v0.9x"
```

Current local results:

```text
validate_rc_current.ps1: PASS, 9 checks, 0 failures
validate_jsonschema.py: PASS, 4 targets, 0 failures
validate_event_chain.py: PASS, 1 event, 0 failures
```

## Privacy Review

The extension contains only synthetic examples and public-facing schemas.

Private Aster, Claudio, Drive, Bookshelf, client, and runtime material are excluded.

Current local privacy scan only returns negative exclusion statements in `README.md` and `LICENSE-NOTES.md`.

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
- The append-only chain validates hash continuity, but does not yet solve concurrent forks or multi-surface conflict resolution.
- The manifest provides integrity evidence, but not cryptographic signing by a human authority.
- Terminology around `CURRENT`, `surface`, `room`, and `center_profile` may need broader review before public stabilization.

## Out Of Scope

- Production sync engine.
- Google Drive connector.
- Mobile or desktop product UX.
- Runtime authority management.
- Human signing workflow.
- Fork resolution protocol.
- Commercial Aster RC Technologies implementation.

## Reviewer Checklist

- [ ] Confirm the extension is clearly marked as non-normative draft.
- [ ] Confirm no private material is present.
- [ ] Confirm license notes are compatible with repository policy.
- [ ] Run structural validator.
- [ ] Run JSON Schema validator.
- [ ] Run append-only event chain validator.
- [ ] Review terminology for `CURRENT`, `surface`, `room`, `engine`, and `center_profile`.
- [ ] Decide whether this remains v0.9.x extension or becomes part of a future v1.0 proposal.

## Publication Decision

Prepared only.

No push.
No PR opened.
No publication action taken.
