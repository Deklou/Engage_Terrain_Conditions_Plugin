# Engage Terrain Conditions

Skyline plugin for Fire Emblem Engage 2.0.0.

The planned `OverlayActive` command will return `1` when a unit stands on a map overlay and `0` otherwise. Base-map terrain is excluded.

Intended XML condition: `OverlayActive > 0`

## Build

Requires WSL with Rust and cargo-skyline.

```sh
cargo skyline build --release
```

Output: `target/aarch64-skyline-switch/release/libterrain_conditions.nro`. Install it in its own Cobalt mod folder.

## Status

Startup diagnosis: the fixed-offset `UnitCalculator.AddCommand` hook is installed, but `OverlayActive` registration is temporarily disabled until the hook has been tested in game. No gameplay changes are active.
