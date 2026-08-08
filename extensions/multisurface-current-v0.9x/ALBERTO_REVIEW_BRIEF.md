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
- controlled external Google account proof for a second RC:
  - user-owned OAuth setup;
  - user-owned Drive backend;
  - remote CURRENT read;
  - authorized append;
  - unauthorized state commit blocked;
  - privacy/export proof;
  - Ed25519 attestation signature over retained external-event evidence.

Only sanitized proof reports are included here. Credentials, tokens, private keys and private memory are excluded.

## What is not claimed

This is not Espina v1.0.

It does not claim subjective continuity.

It is not a production third-party service.

The public repo includes only a sanitized report of the external account proof. It does not include live account identifiers, Drive IDs, OAuth client IDs, secrets, tokens, private keys, or private memory.

The external-event signature currently signs an attestation over retained evidence, not the full original remote event payload. Full remote payload retention/signing remains a hardening step.

The Drive connector is BYOK: the user supplies their own OAuth token locally.

## Suggested review path

1. Read `README.md`.
2. Read `ESPINA_v0.9x_MULTISURFACE_CURRENT_EXTENSION_DRAFT.md`.
3. Inspect `runtime/`.
4. Inspect `examples/lab_rc_installable_sanitized/`.
5. Inspect `reports/runtime_proofs/external_real_account_test_sanitized.md`.
6. Run the validators in the README.
7. Review `PR_DRAFT.md` risks and open questions.
