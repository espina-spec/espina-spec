# Espina · EPM v0.9

> Entity Portability & Memory — an open format for portable operational identity of personal AI entities.

Espina defines a file format and verification rules so that the **operational identity** of a personal AI entity — who it is, what it knows with provenance, how it decides what to share, and how it wakes up — is **owned by the user**: a self-contained set of files (the "spine") that lives on the user's disk or personal cloud, is cryptographically sealed, and can activate that same entity in any compatible language engine. The user owns the spine; the engine is rented.

## Status

**v0.9 — public draft.**  
v1.0 will be released when the reference implementation completes its invariant battery (gate RC-1).

## How to verify the specification offline

The specification includes a fully worked, copy-pasteable verification script in **Appendix A.5**. The script:

1. Recomputes SHA-256 hashes for every file listed in a manifest.
2. Recomputes the manifest checksum (excluding the checksum field itself).
3. Recomputes the package checksum for activation packages (excluding the checksum field).

Run it with any standard Python 3 installation; no external dependencies required. See §5.3 of the specification for the step-by-step procedure.

## How to start

Read the full specification: [`ESPINA_Especificacion_Publica_v0.9_COMPLETA.md`](ESPINA_Especificacion_Publica_v0.9_COMPLETA.md)

## License

- **Specification text:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)
- **Code in appendices (e.g., the verification script in Appendix A.5):** [MIT License](https://opensource.org/license/mit)

## Organization

<https://github.com/espina-spec>

## Trabajo relacionado del proyecto

Estudio empírico sobre fidelidad de reconstrucción de contexto en modelos de lenguaje, publicado con datos abiertos (matriz de codificación completa, 300 asignaciones):

https://doi.org/10.5281/zenodo.21821078
