# ESPINA v0.9.x - Multisurface CURRENT Extension Draft

Date: 2026-08-07
Status: draft candidate
Base specification: Espina v0.9

## 1. Scope

This extension adds a portable contract for RC continuity across multiple surfaces, devices, and engines.

It does not replace Espina v0.9. It extends the part that v0.9 explicitly reserves for later work: reentry and re-synchronization of already active instances.

## 2. Core Thesis

An RC does not need to be fully copied into every surface. Each authorized surface must be able to reconstruct a conforming CURRENT from the Espina, with verifiable continuity, proportional memory, membrane governance, and explicit limits.

Formula:

```text
Espina transports portable continuity.
Center governs what remains stable.
CURRENT situates live operation.
Surface expresses the RC under concrete capabilities.
Activation package gives the engine only authorized context.
```

## 3. Terms

### RC

Relational-operational entity composed of identity, memory, worlds, membrane, provenance, continuity, and action rules.

### Espina

Portable and verifiable substrate of the RC.

### Center

Optional or advanced profile for the stable governing nucleus of an RC. In some implementations this may be a lightweight policy object; in relational RCs it may be a stronger constitutional layer.

### CURRENT

Situated, verifiable operational state from which an RC acts now.

It may include:

- active world;
- active surface;
- active room;
- active task;
- continuity status;
- proportional memory references;
- certainty limits;
- capabilities;
- open loops;
- recent events.

CURRENT is not a single magic file. It is a reconstructible state supported by pointers, state files, logs, and verification.

### Surface

Environment where the RC is expressed: chat, agent workspace, messaging bot, mobile app, web app, API, local app, or other interface.

### Engine

Interchangeable model or computational system that generates outputs. The engine does not own the RC.

## 4. Required Extension Components

### 4.1 World Registry

A conforming multisurface Espina SHOULD declare an explicit world registry.

Purpose:

- avoid discovering worlds only by scanning memory objects;
- declare world status;
- declare default sensitivity;
- declare authority;
- declare allowed destinations.

Schema:

```text
schemas/world_registry.schema.json
```

### 4.2 Surface Registry

A conforming multisurface Espina SHOULD declare authorized surfaces and capability profiles.

Purpose:

- separate engine from RC;
- distinguish read, write, tool, and message capabilities;
- assign permission levels;
- define degradation modes.

Schema:

```text
schemas/surface_registry.schema.json
```

### 4.3 CURRENT Contract

A conforming multisurface Espina SHOULD declare how CURRENT is defined, located, verified, updated, and protected.

Schema:

```text
schemas/current_contract.schema.json
```

Required continuity states:

- `CONTINUITY_OK`
- `CONTINUITY_PARTIAL`
- `CURRENT_STALE`
- `CURRENT_DIVERGENT`
- `CURRENT_UNKNOWN`
- `DEGRADED_MODE`
- `BLOCKED`

### 4.4 CURRENT Events

Surfaces SHOULD write or emit append-only events for relevant changes.

Event types include:

- `decision`
- `correction`
- `promise`
- `open_loop`
- `task_change`
- `world_change`
- `surface_reentry`
- `continuity_warning`
- `divergence_detected`
- `state_commit`
- `membrane_block`
- `membrane_transform`
- `canon_candidate`

Schema:

```text
schemas/current_event.schema.json
```

## 5. Permission Model

This extension separates participation from governance.

Permission levels:

```text
0 read_current
1 append_event
2 propose_state_update
3 commit_working_state
4 commit_current_state
5 modify_center_or_membrane
```

Rule:

> Any authorized surface may participate in CURRENT, but not every surface may govern it.

## 6. Minimal Reentry Protocol

A surface reentry SHOULD follow this sequence:

```text
identify_surface
read_espina_minimum
read_world_registry
read_current_pointer
read_current_state
verify_continuity
build_activation_package
act_or_respond
append_event_if_relevant
propose_or_commit_update
```

If continuity cannot be verified, the surface MUST NOT claim full continuity.

## 7. CURRENT Storage

This extension is storage-agnostic.

Allowed storage patterns include:

- local folder;
- user cloud folder;
- private git repository;
- object storage;
- application backend.

Storage stores evidence and state. Espina governs. CURRENT situates. The surface instantiates. The engine responds.

## 8. Degraded Mode

An implementation SHOULD support degraded modes when a surface lacks permissions, storage, recent memory, or synchronization.

Examples:

- read-only;
- proposal-only;
- no recent memory;
- no write access;
- strict membrane;
- blocked by sensitivity.

## 9. Relationship To Espina v0.9

This extension preserves:

- identity portability;
- five memory layers;
- membrane fail-closed behavior;
- provenance and hash discipline;
- activation package as context, not mandate;
- honesty clause about operational record continuity.

It adds:

- explicit world registry;
- surface registry;
- current contract;
- continuity states;
- event/update flow;
- degraded operation;
- foundation for reentry and resynchronization.

## 10. Example

The synthetic example is:

```text
examples/ana_rc/
```

It declares:

- three worlds: `personal`, `professional`, `health`;
- three surfaces: `chatgpt_web`, `codex_desktop`, `telegram_bot`;
- a partial CURRENT;
- one initial reentry event.

## 11. Conformance Sketch

A draft-compatible implementation should verify:

- JSON files parse;
- `rc_id` is consistent;
- `active_world` exists in `world_registry`;
- `active_surface` exists in `surface_registry`;
- `continuity_status` is allowed by `current_contract`;
- events parse as JSONL;
- the active surface has the required permission for attempted operation.

The included validator is:

```text
tools/validate_rc_current.ps1
```

## 12. Open Questions

1. Should `center` be required in v1.0 or remain an advanced profile?
2. Should this remain a v0.9.x extension or become part of v1.0?
3. How should append-only events be signed?
4. How should lock semantics work on non-transactional user cloud storage?
5. What is the minimum activation package extension required for CURRENT?

