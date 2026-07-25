# ESPINA v0.9 — Entity Portability & Memory

> **English (10 lines max):** ESPINA is an open file format and verification ruleset for the *operated identity* of personal AI entities — who they are, what they know with provenance, how they decide what to share, and how they wake up. It is not just portable memory: it is governed identity. The user owns the spine; the engine is rented.

## Qué es Espina en 3 frases

1. **Identidad operada, no solo memoria portable:** Espina especifica quién es la entidad, con qué voz opera, qué puede viajar a qué destino, cómo se verifica y cómo despierta — no solo "qué recuerda".
2. **Membrana fail-closed:** Ningún contenido viaja a un destino sin pasar un filtro de sensibilidad definido por el usuario. La ausencia de filtro no es un default válido.
3. **Verificabilidad mecánica sin terceros:** Todo contenido canónico lleva procedencia comprobable por hashes SHA-256; la verificación es posible offline con herramientas estándar.

## Cómo verificar en 3 pasos

```bash
# 1. Clonar
git clone https://github.com/espina-spec/espina-spec.git
cd espina-spec

# 2. Ejecutar verificador
python tools/verificar.py

# 3. Resultado esperado
# "Todos los hashes coinciden"
# "manifest_checksum verificado correctamente"
```

## Estado v0.9

Esta es la especificación pública v0.9, publicada el 2026-07-24.

**Qué SÍ cubre:**
- Estructura de la espina (7 capas)
- Membrana (mundos × sensibilidad × destinos)
- Paquetes de activación con safety frame
- POST (batería de autocomprobación)
- Verificación offline por hashes SHA-256

**Qué NO cubre (declarado explícitamente):**
- Firma criptográfica con clave privada del usuario
- Árboles de hashes (Merkle)
- Re-sincronización en caliente de instancias ya activas

Estos elementos son candidatos a v1.x. Los hashes simples de v0.9 verifican **INTEGRIDAD**, no autoría.

## Gobernanza

- **Autoridad actual:** the Aster project
- **Transferencia planificada:** Aster RC Co. (en constitución) al completarse su registro
- **Proceso:** Propuestas públicas → evaluación contra implementación de referencia → decisión razonada publicada

## Licencias

- **Texto de la especificación (ESPINA_v0.9.md, README.md, documentos de espina):** [CC BY 4.0](./LICENSE-ESPINA)
- **Herramientas, scripts y código (tools/):** [MIT](./LICENSE-TOOLS)

## Aviso sintético

**Ana N.** es una entidad de juguete completamente sintética. Ningún dato real de ninguna persona real aparece en este repositorio. Todos los ejemplos son ficticios.

---

*Espina · Entity Portability & Memory (EPM) v0.9*
