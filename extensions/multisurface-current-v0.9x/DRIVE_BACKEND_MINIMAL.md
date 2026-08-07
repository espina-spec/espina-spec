# Minimal Drive-style backend

Status: non-normative implementation note
Date: 2026-08-07

## Purpose

This note describes the smallest folder-based backend that can support a multisurface CURRENT.

It uses a user-controlled folder such as Google Drive, but the pattern is storage-agnostic. A local folder, synced cloud folder, private repository, or application backend can use the same contract.

## Minimal Folder

```text
ESPINA_RC_DRIVE_MINIMAL/
  00_espina/
  01_current/
    CURRENT_POINTER.json
    state/
      CURRENT_STATE.json
      CONTINUITY_STATUS.json
      OPEN_LOOPS.json
    events/
      YYYY-MM-DD.jsonl
    proposals/
  02_activation/
  03_reports/
  04_tools/
  DRIVE_BACKEND_PROTOCOL.md
  README.md
```

## Responsibilities

### Drive or folder backend

Stores:

- pointers;
- current state;
- event logs;
- proposals;
- reports;
- validation artifacts.

### Espina

Governs:

- identity;
- worlds;
- surfaces;
- permissions;
- membrane;
- continuity contract.

### Surface

Performs:

- reentry;
- verification;
- activation package construction;
- event append;
- proposal or commit according to permission.

### Engine

Generates output from authorized context.

The engine does not own the RC.

## Minimal Reentry

A surface should:

1. Read `CURRENT_POINTER.json`.
2. Read referenced state.
3. Validate latest event chain if possible.
4. Check its own permission in the surface registry.
5. Build an activation package.
6. Declare continuity status.
7. Act within permission.
8. Append or propose updates only when allowed.

A step-by-step operational playbook for LLM surfaces is provided in:

```text
LLM_REENTRY_PLAYBOOK.md
```

## Minimal Safety Rules

```text
No verified pointer -> no CONTINUITY_OK.
No verified event head -> no CONTINUITY_OK.
Unreconciled fork -> no CONTINUITY_OK.
Unknown surface permission -> no write.
Proposal is not committed state.
Activation package is context, not proof of subjective continuity.
```

## CURRENT_POINTER.json

Recommended minimal fields:

```json
{
  "rc_id": "example_rc",
  "backend": "google_drive_folder",
  "current_version": "current_state_001",
  "state_path": "01_current/state/CURRENT_STATE.json",
  "continuity_path": "01_current/state/CONTINUITY_STATUS.json",
  "open_loops_path": "01_current/state/OPEN_LOOPS.json",
  "latest_events_path": "01_current/events/YYYY-MM-DD.jsonl",
  "accepted_head": null,
  "continuity_status": "CURRENT_UNKNOWN",
  "updated_at": "2026-08-07T00:00:00Z"
}
```

## Write Model

For low-friction user folders, prefer optimistic writing:

1. Read accepted head.
2. Build event with `previous_hash`.
3. Re-read head if possible.
4. Append only if still valid.
5. If changed, rebuild or declare divergence.

This avoids requiring a complex lock service for the minimal backend.

## Non-Goals

This note does not define:

- a Google API connector;
- OAuth;
- production sync;
- mobile UX;
- encrypted storage;
- conflict-free replicated data types;
- commercial onboarding.

Those belong to runtimes and products, not to the minimal public draft.
