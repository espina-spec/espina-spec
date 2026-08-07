# Espina v0.9.x - Multisurface CURRENT Extension Draft

Status: public draft candidate
Date: 2026-08-07

This folder is a clean draft candidate for a future Espina v0.9.x extension.

It contains only synthetic examples and public-facing schemas. It does not contain private Aster, Claudio, client, Drive, Bookshelf, or runtime material.

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
```

## Non-goals

This draft does not define a full runtime, product UX, backend connector, sync engine, or commercial onboarding system.

It specifies contracts that an implementation may support.

## Safety Rule

The extension does not claim subjective continuity. It preserves Espina v0.9's honesty clause:

> Activation is continuity of operational record, not proof of continuous subjective experience.

