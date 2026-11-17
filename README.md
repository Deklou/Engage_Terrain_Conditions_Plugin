# Engage Terrain Conditions

Skyline plugin for Fire Emblem Engage 2.0.0.

The planned `OverlayActive` command will return `1` when a unit stands on a map overlay and `0` otherwise. Base-map terrain is excluded.

Intended XML condition: `OverlayActive > 0`

## Build and deploy

From WSL, with Rust and cargo-skyline installed:

```sh
bash scripts/deploy.sh
```

Stop the game before running the script. It builds the NRO, copies it to Ryujinx's `sdcard/engage/mods/Terrain_Conditions/` folder and keeps the first existing NRO as `.bak`. The Ryujinx location is detected from Windows `%APPDATA%`.

For a custom Ryujinx location, set `RYUJINX_DIR` to the directory containing `sdcard/`.

To build without deploying:

```sh
cargo skyline build --release
```

## Status

Startup diagnosis: the fixed-offset `UnitCalculator.AddCommand` hook is installed, but `OverlayActive` registration is temporarily disabled until the hook has been tested in game. No gameplay changes are active.
