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
schemas/
examples/ana_rc/
tools/validate_rc_current.ps1
tools/validate_jsonschema.py
tools/validate_event_chain.py
tools/build_extension_manifest.py
reports/
MANIFEST.json
LICENSE-NOTES.md
PR_DRAFT.md
```

## License

- Specification text and synthetic Markdown examples: CC BY 4.0, following the Espina specification text license.
- JSON schemas and structured synthetic examples: MIT, following the Espina tooling license, so implementers can copy them directly into validators and runtimes.
- Tools and scripts: MIT.

If a file mixes explanatory text and machine-readable structure, use the more permissive implementation path for the structured artifact and preserve attribution to Espina.

## Non-goals

This draft does not define a full runtime, product UX, backend connector, sync engine, or commercial onboarding system.

It specifies contracts that an implementation may support.

## Safety Rule

The extension does not claim subjective continuity. It preserves Espina v0.9's honesty clause:

> Activation is continuity of operational record, not proof of continuous subjective experience.
