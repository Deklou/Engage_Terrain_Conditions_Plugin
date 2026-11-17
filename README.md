# Engage Terrain Conditions

Skyline plugin for Fire Emblem Engage 2.0.0.

Adds the `OverlayActive` command for `Skill.xml` conditions. It returns `1` if the unit is on a map overlay (Dragon Vein effects, flames, miasma, etc.), and `0` otherwise, including outside tactical maps. Base-map terrain is not counted.

Example condition: `OverlayActive > 0`

## Build

Requires WSL with Rust and cargo-skyline.

```sh
cargo skyline build --release
```

Output: `target/aarch64-skyline-switch/release/libterrain_conditions.nro`. Install the NRO in its own Cobalt mod folder.

## Status

Command registration and overlap detection are experimental and still need an in-game test. Groundswell's critical bonus, end-of-action healing, and battle activation display are not changed by this plugin alone.
