# Engage Terrain Conditions

Skyline plugin for Fire Emblem Engage 2.0.0. The goal is to make map-overlay conditions available to skill expressions.

## Scope

- Detect temporary terrain effects (`MapOverlap`), not base-map terrain.
- Keep passive bonuses in sync with battle forecasts and actual combat.
- Return a neutral value outside tactical maps.
- Keep Groundswell's end-of-action healing separate from passive stat calculations.

## Status

Project skeleton only. No hooks, XML commands, or gameplay changes are implemented yet.

## Build

Requires Rust and cargo-skyline in WSL.

```sh
cargo skyline build --release
```

The expected output is `target/aarch64-skyline-switch/release/libterrain_conditions.nro`. Build and in-game loading still need to be verified. Commit `Cargo.lock` after the first successful build.
