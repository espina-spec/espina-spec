# Phase 22 JSON Schema validation

Status: PASS
Targets: 4
Failures: 0

## Results

- PASS `world_registry`
  - schema: `schemas\world_registry.schema.json`
  - instance: `examples\ana_rc\espina\world_registry.json`
  - validation_mode: `fallback_required_and_basic_types`
- PASS `surface_registry`
  - schema: `schemas\surface_registry.schema.json`
  - instance: `examples\ana_rc\espina\surface_registry.json`
  - validation_mode: `fallback_required_and_basic_types`
- PASS `current_contract`
  - schema: `schemas\current_contract.schema.json`
  - instance: `examples\ana_rc\espina\current_contract.json`
  - validation_mode: `fallback_required_and_basic_types`
- PASS `activation_package`
  - schema: `schemas\activation_package.schema.json`
  - instance: `examples\ana_rc\activation\activation_package_001.json`
  - validation_mode: `fallback_required_and_basic_types`
