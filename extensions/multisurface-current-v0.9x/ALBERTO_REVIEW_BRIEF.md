# Alberto Review Brief - Espina Multisurface CURRENT Extension

## What this branch shows

This branch adds an experimental Espina v0.9.x extension for multisurface operation.

The core idea is that an RC can carry enough operational structure to be re-entered from different authorized surfaces without pretending that the model itself owns memory or subjective continuity.

The extension adds:

- CURRENT pointer and continuity status;
- surface capability registry;
- append-only event chain;
- activation package shape;
- minimal Drive-style backend pattern;
- installable runtime tools;
- generic Drive connector with BYOK credentials;
- surface CLI;
- revocation and privacy/export proof.

## What is proven in the lab

The private lab run behind this public branch verified:

- separated remote backend for a second RC;
- remote append with accepted-head check;
- append from an external simulated surface;
- blocked unauthorized state commit;
- Ed25519 signature verification for a remote event;
- minimal remote reentry;
- installable runtime validation.

Only sanitized proof reports are included here. Credentials, tokens, private keys and private memory are excluded.

## What is not claimed

This is not Espina v1.0.

It does not claim subjective continuity.

It is not a production third-party service.

It has not yet been tested with a fully independent Google account in this public repo.

The Drive connector is BYOK: the user supplies their own OAuth token locally.

## Suggested review path

1. Read `README.md`.
2. Read `ESPINA_v0.9x_MULTISURFACE_CURRENT_EXTENSION_DRAFT.md`.
3. Inspect `runtime/`.
4. Inspect `examples/lab_rc_installable_sanitized/`.
5. Run the validators in the README.
6. Review `PR_DRAFT.md` risks and open questions.
