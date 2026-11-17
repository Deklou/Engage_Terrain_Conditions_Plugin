# Engage Terrain Conditions

Skyline plugin for Fire Emblem Engage 2.0.0.

Adds the experimental `OverlayActive` command for `Skill.xml` conditions. It is intended to return `1` if an unit stands on a map overlay and `0` otherwise. Base-map terrain is excluded.

XML condition: `OverlayActive > 0`

## Build and deploy

From WSL, with Rust and cargo-skyline installed:

```sh
bash scripts/deploy.sh
```

Stop the game before running the script. It builds the NRO, copies it to Ryujinx's `sdcard/engage/mods/Terrain_Conditions/` folder and keeps the first existing NRO as `.bak`. The Ryujinx location is detected from Windows `%APPDATA%`.

For a custom Ryujinx location, set `RYUJINX_DIR` to the directory containing `sdcard/`.

## Status

The fixed-offset `UnitCalculator.AddCommand` hook is validated. `OverlayActive` registration is enabled, but still needs a startup test followed by in-game tests on map overlays, menus and combat forecasts. Groundswell remains unchanged.
