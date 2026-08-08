# LLM reentry playbook

Status: non-normative operational playbook
Date: 2026-08-07

## Purpose

This playbook describes how any LLM surface should enter a multisurface RC folder without pretending continuity it has not verified.

The rule is simple:

> Read, verify, declare limits, then act.

## Inputs

A surface needs:

- path or URI to the RC backend folder;
- surface identity;
- engine identity if relevant;
- declared user request;
- permission profile or access to `surface_registry.json`;
- current date/time from the running environment.

## Step 1 - Locate The Backend

Find the backend root.

Expected minimal structure:

```text
00_espina/
01_current/
02_activation/
03_reports/
04_tools/
```

If the backend root cannot be found:

```text
continuity_status: CURRENT_UNKNOWN
allowed_action: ask_for_location_or_continue_without_continuity
```

## Step 2 - Read Pointer

Read:

```text
01_current/CURRENT_POINTER.json
```

The pointer must identify:

- `rc_id`;
- state path;
- continuity path;
- event log path;
- accepted head;
- declared continuity status.

If pointer is missing or invalid:

```text
continuity_status: CURRENT_UNKNOWN
allowed_action: no_continuity_claim
```

## Step 3 - Read Espina Minimum

Read or locate:

```text
00_espina/world_registry.json
00_espina/surface_registry.json
00_espina/current_contract.json
```

If these are missing in a template:

```text
continuity_status: CURRENT_UNKNOWN
allowed_action: template_review_only
```

If these are missing in a live RC:

```text
continuity_status: DEGRADED_MODE
allowed_action: read_only_or_proposal_only
```

## Step 4 - Identify Surface

The LLM must identify its current surface.

Examples:

```text
chatgpt_web
codex_desktop
telegram_bot
mobile_app
api_worker
```

If the surface is not listed in `surface_registry.json`:

```text
permission_level: 0
allowed_action: read_current_only
write: forbidden
```

## Step 5 - Read State

Read the files referenced by the pointer:

```text
CURRENT_STATE.json
CONTINUITY_STATUS.json
OPEN_LOOPS.json
```

Check:

- same `rc_id`;
- allowed continuity status;
- active world exists;
- active surface is allowed;
- open loops parse.

If state and pointer disagree:

```text
continuity_status: CURRENT_DIVERGENT
```

## Step 6 - Validate Events

Read the latest event log.

If event validation is available, verify:

- JSONL parses;
- each event conforms to `current_event.schema.json`;
- each event hash is correct;
- `previous_hash` links correctly;
- no unreconciled fork exists;
- accepted head matches pointer.

If event log is empty:

```text
continuity_status: CURRENT_UNKNOWN
```

If hashes fail:

```text
continuity_status: BLOCKED
```

If fork exists:

```text
continuity_status: CURRENT_DIVERGENT
```

## Step 7 - Build Activation Package

Build or request an activation package containing only:

- user request;
- active world;
- active surface;
- continuity status;
- allowed memory references;
- permission limits;
- certainty limits;
- relevant open loops.

Do not include all memory by default.

## Step 8 - Declare Continuity Before Answering

Before acting with RC continuity, the surface must internally decide:

```text
CONTINUITY_OK
CONTINUITY_PARTIAL
CURRENT_STALE
CURRENT_DIVERGENT
CURRENT_UNKNOWN
DEGRADED_MODE
BLOCKED
```

If the status is not `CONTINUITY_OK`, the answer should not imply full continuity.

## Step 9 - Act Within Permission

Permission levels:

```text
0 read_current
1 append_event
2 propose_state_update
3 commit_working_state
4 commit_current_state
5 modify_center_or_membrane
```

If permission is lower than the requested operation, the surface must downgrade:

- answer read-only;
- write a proposal;
- ask for human authority;
- block.

## Step 10 - Append Event Or Proposal

If an event is relevant and permission allows:

1. Read accepted head.
2. Build event with `previous_hash`.
3. Re-read accepted head when possible.
4. Append only if head is still valid.
5. If head changed, declare divergence or rebuild.

If permission does not allow append:

```text
01_current/proposals/
```

## Step 11 - Never Rewrite History

Corrections are new events.

Do not erase:

- mistaken decisions;
- blocked actions;
- divergence;
- promises;
- membrane transformations;
- rejected branches.

## Minimal Response Contract

When continuity is not fully verified, an LLM surface should behave as:

```text
I can work from the available operational record, but I cannot claim full current continuity because <reason>.
```

It should then continue in the safest allowed mode.

## Stop Conditions

Stop or block when:

- private material appears in the wrong world;
- user authority is required;
- event hash is invalid;
- fork is unresolved;
- surface permission is unknown for write action;
- current state asks for a forbidden operation;
- user asks to publish, delete, send, expose, or change permissions without confirmation.

## Output Of Reentry

A reentry attempt should produce:

```json
{
  "rc_id": "example_rc",
  "surface": "codex_desktop",
  "continuity_status": "CURRENT_UNKNOWN",
  "permission_level": 0,
  "can_answer": true,
  "can_append_event": false,
  "can_commit_state": false,
  "reason": "Pointer exists but no verified event head is present."
}
```
