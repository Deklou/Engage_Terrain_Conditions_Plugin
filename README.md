# Engage Terrain Conditions

Skyline plugin for Fire Emblem Engage 2.0.0.

Adds the experimental `OverlayActive` command for `Skill.xml` conditions. It returns 1 when a unit stands on a map overlay, and 0 otherwise. Base-map terrain is excluded.

XML condition: `OverlayActive > 0`

## Build and deploy

From WSL, with Rust and cargo-skyline installed:

```sh
bash scripts/deploy.sh
```

Stop the game before running the script. It builds the NRO, copies it to Ryujinx's `sdcard/engage/mods/Terrain_Conditions/` folder and keeps the first existing NRO as `.bak`. The Ryujinx location is detected from Windows `%APPDATA%`.

For a custom Ryujinx location, set `RYUJINX_DIR` to the directory containing `sdcard/`.

## Groundswell test

With the game closed and the plugin deployed, run:

```sh
python3 scripts/groundswell_test.py enable
```

This temporarily changes Groundswell in the installed `Emblem_Rework/patches/xml/Skill.xml` to grant Crit +10 only on a `MapOverlap` tile. Healing and terrain removal are disabled **during this test**. The original XML is backed up beside the modified file.

Compare combat forecasts with and without a map overlay, then restore the original:

```sh
python3 scripts/groundswell_test.py restore
```

No rebuild is required for XML-only changes. Keep the game closed when enabling or restoring the test.

## Status

The fixed-offset `UnitCalculator.AddCommand` hook and `OverlayActive` registration work at startup. The new XML condition still needs in-game validation, including combat forecasts and returning to a normal tile.
