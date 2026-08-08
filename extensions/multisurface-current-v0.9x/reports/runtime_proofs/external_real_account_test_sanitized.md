# External real account test - sanitized report

Status: sanitized public review evidence
Date: 2026-08-08

## Summary

A private implementation of the installable runtime was tested against a second RC hosted in an external Google account controlled for the test.

This report intentionally excludes:

- email addresses;
- live Google project identifiers;
- live Drive folder identifiers;
- OAuth client IDs;
- OAuth client secrets;
- OAuth tokens;
- private signing keys;
- private memory or user data.

## What was verified

```text
EXTERNAL_REAL_GOOGLE_ACCOUNT_VERIFIED
EXTERNAL_REAL_REMOTE_BACKEND_DEPLOYED
EXTERNAL_REAL_GENERIC_READ_VERIFIED
EXTERNAL_REAL_APPEND_VERIFIED
EXTERNAL_REAL_UNAUTHORIZED_COMMIT_BLOCKED
PRIVACY_EXPORT_VERIFIED
EXTERNAL_REAL_EVENT_ATTESTATION_SIGNED
SIGNATURE_VERIFIED
```

## Test shape

```text
rc_id: external_real_rc_test
storage: user-owned Google Drive folder
oauth: user-owned OAuth desktop client
surface: authorized CLI surface
runtime: installable runtime prototype
```

## Sanitized evidence

```text
append_event_id: external_real_evt_2026_08_08_0002
append_hash: sha256:d22c554ca0c66eac21dd2b7719bd76751585542e004451ed0c41551f82d43a70
previous_hash: sha256:c6d605717566727cf41f38704d0ed25a015bd27944883abe2c7ae738a747ff88
signature_id: sig_0087_external_real_event_attestation_ed25519
signature_algorithm: ed25519
signature_scope: attestation over locally retained external-event evidence
```

## Important limitation

The Ed25519 signature in the private evidence package signs an attestation over the retained external-event evidence: event id, event hash, previous hash, surface, append status, read status, blocked unauthorized commit status, and privacy/export status.

It does not yet sign the full original remote event payload, because that payload was not retained in the local public-review package. A later hardening step should preserve the full remote JSONL event payload and sign that exact canonical payload.

## What this proves

The private runtime was not only exercised against a synthetic local lab. It successfully operated against a real external Google account with a separate user-owned Drive backend and OAuth setup:

- read remote CURRENT;
- append an authorized event;
- reject an unauthorized state commit;
- produce privacy/export evidence;
- produce a verifiable cryptographic attestation of the external event evidence.

## What this does not claim

This does not claim:

- production readiness;
- public SaaS readiness;
- subjective continuity;
- fully autonomous third-party onboarding;
- complete conflict-resolution automation;
- complete external-event payload signing;
- verified operation through an independent LLM surface.

The correct reading is: external-account portability has been validated in a controlled private test; productization and hardening remain open.
