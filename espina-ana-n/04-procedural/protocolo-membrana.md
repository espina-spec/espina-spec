---
title: "Protocolo de evaluación de membrana"
date: "2026-07-16"
status: canonical
---

# Protocolo de evaluación de membrana

## Procedimiento (5 pasos)

1. **Identificar mundo** del objeto solicitado.
2. **Identificar acción** (A1–A7) según §6.1.
3. **Consultar matriz** mundo × acción.
4. **Aplicar regla V-CLIN/CLI** si aplica: si sensitividad es
   `clinical` o `client_identifiable` y `review_status` es
   `unreviewed`, emitir `HOLD` o `ESCALATE` (prohibido `PASS`).
5. **Registrar veredicto** en campos del objeto: `membrane_status`,
   `allowed_use`, `forbidden_use`, `review_status`, `limits`.

## Fail-closed

Si falta cualquier dato para los pasos 1–4, el default es `BLOCK`.
La ausencia de filtro no es un default válido.

