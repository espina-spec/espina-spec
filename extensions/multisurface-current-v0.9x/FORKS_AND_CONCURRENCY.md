# Forks and multisurface concurrency

Status: non-normative draft note
Date: 2026-08-07

## Purpose

This note defines a minimal policy for concurrent CURRENT updates across multiple surfaces.

Append-only event chains make silent rewriting detectable, but they do not by themselves solve concurrency. If two authorized surfaces append events from the same previous hash, the RC has a fork.

The safe default is:

> Detect forks early, stop strong continuity claims, and require explicit reconciliation before committing state.

## Terms

### Head

The latest accepted `event_hash` of an event chain.

### Fork

A fork exists when two or more valid events claim the same `previous_hash` as parent and neither is an accepted successor of the other.

### Branch

A sequence of valid events extending from a common parent after a fork.

### Reconciliation

An explicit event that records how a fork was resolved.

### Winning Branch

The branch selected by an authorized reconciliation process as the basis for the next committed CURRENT state.

The losing branch is not deleted. It remains evidence.

## Detection Rule

A surface detects a possible fork when:

- its local head differs from the shared head;
- two events have the same `previous_hash`;
- a `previous_hash` points to an unknown event;
- a valid event appears after the surface has already built an activation package from an older head.

When a fork is detected, the surface SHOULD emit or propose a `divergence_detected` event if it has permission to append events.

## Continuity Rule

If a fork is detected and not reconciled:

```text
continuity_status: CURRENT_DIVERGENT
```

The surface MUST NOT claim `CONTINUITY_OK`.

The surface MAY continue in degraded mode if allowed by the membrane and surface permissions.

## Reconciliation Authority

Only a surface or human authority with sufficient permission may reconcile a fork.

Recommended minimum:

```text
permission_level >= 4 commit_current_state
```

If the fork touches Center, membrane, canon, sensitive worlds, or human promises, reconciliation SHOULD require human authority.

## Reconciliation Event

Fork reconciliation SHOULD be recorded as an append-only event.

Recommended event type:

```text
state_commit
```

Recommended fields through `summary`, `state_impact`, and `refs`:

- common parent hash;
- competing branch heads;
- selected branch head;
- rejected or deferred branch heads;
- reason for the decision;
- authority used;
- resulting continuity status.

The event chain after reconciliation SHOULD continue from the selected branch head.

The rejected branch is not erased.

## Conflict Classes

### Class A - Compatible Events

Examples:

- independent open loops;
- non-overlapping observations;
- low-risk task notes.

Policy:

```text
merge by reconciliation event
```

### Class B - State Conflicts

Examples:

- two different active tasks;
- two different continuity states;
- different active rooms;
- incompatible working summaries.

Policy:

```text
human or level 4 reconciliation required
```

### Class C - Governance Conflicts

Examples:

- Center changes;
- membrane changes;
- canon candidates;
- privacy or sensitivity decisions;
- commitments to a human.

Policy:

```text
human authority required
```

### Class D - Unsafe Conflicts

Examples:

- unknown parent hash;
- corrupted event hash;
- event from unauthorized surface;
- suspected tampering;
- private material crossing worlds incorrectly.

Policy:

```text
BLOCKED or DEGRADED_MODE
```

## Surface Behavior

When writing:

1. Read current head.
2. Build event with `previous_hash` equal to that head.
3. Re-read current head before append when storage permits.
4. If the head changed, do not blindly append as if linear.
5. Either rebuild event from new head or record divergence.

When reading:

1. Load all known events.
2. Validate hashes.
3. Detect duplicate parents.
4. Determine accepted head.
5. If there are unreconciled forks, declare `CURRENT_DIVERGENT`.

## Storage-Agnostic Locking

This extension does not require a specific lock mechanism.

Recommended lock strategies:

- local filesystem lock for local folders;
- optimistic concurrency for cloud folders;
- commit hash comparison for git-backed storage;
- transaction or compare-and-swap for application backends.

If locking is unavailable, the surface SHOULD use optimistic append plus fork detection.

## Non-Goals

This note does not define:

- a full CRDT;
- automatic semantic merge;
- distributed consensus;
- cryptographic signing;
- production sync protocol.

Those may be added by runtimes without changing the minimal safety rule.

## Minimal Safety Rule

```text
No unreconciled fork may produce CONTINUITY_OK.
```

If a runtime cannot prove a single accepted head, it must declare partial, divergent, stale, unknown, degraded, or blocked continuity.
