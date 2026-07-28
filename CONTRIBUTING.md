# Contributing to Espina

Thank you for your interest in improving Espina. This repository hosts the public specification and its supporting materials. All contributions are welcome within the boundaries below.

## Reporting issues

Open a [GitHub Issue](../../issues) with:
- A clear description of the problem, inconsistency, or gap.
- The section number (§) where it occurs, if applicable.
- A reproducible example or reference, if possible.

## Proposing changes

1. Fork the repository and create a feature branch.
2. Make your changes.
3. **Verify hashes:** if your change affects any file with a recorded SHA-256 (manifests, examples, appendices), recompute and update the hashes. The CI check will fail on mismatched hashes.
4. Open a Pull Request with a concise description of what changed and why.

## Membrane policy for contributions

This project operates under a strict sensitivity membrane. We **do not accept** contributions that contain:
- Personal data of real individuals (names, identifiers, contact information).
- Credentials, tokens, keys, or secrets of any kind.
- Unverifiable claims presented as fact.
- Content that cannot be checked with standard, offline tools.

All examples in the specification use synthetic data (e.g., "Ana N.", "Carlos R."). Keep it that way.

## Code of conduct

Be precise. Be kind. Be verifiable.
