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

## Groundswell tests

With the game closed and the plugin deployed, run:

```sh
python3 scripts/groundswell_test.py crit
```

This first test temporarily changes Groundswell in the installed `Emblem_Rework/patches/xml/Skill.xml` to give +10 critical rate only on a map overlay. The dynamic critical bonus was confirmed in-game with a Corrin Dragon Vein, without moving the unit.

For the next test, switch directly from critical to healing (even if the first test is still active):

```sh
python3 scripts/groundswell_test.py heal
```

This sets `Timing=26`, `Condition="OverlayActive &gt; 0"`, `ActNames="HP;"`, `ActValues="10;"` and clears `OverlapRange` and `OverlapTerrain` so the skill should heal after the action without removing the overlay. The critical bonus is **temporarily disabled** to isolate healing.

Test with a damaged unit on a non-healing Dragon Vein and a control without any overlay. Verify that healing happens after the unit acts/waits, **not** when the vein appears or on an ordinary tile, and that the overlay remains afterward. The result is not yet verified.

Switch back to the critical test with `python3 scripts/groundswell_test.py crit` if needed.

Restore the untouched original XML afterward:

```sh
python3 scripts/groundswell_test.py restore
```

All modes use the same `Skill.xml.groundswell.bak` to preserve the original XML. The script refuses to overwrite an unrecognized change. No rebuild is required for XML-only changes. Keep the game closed when switching or restoring a test.

## Status

The fixed-offset `UnitCalculator.AddCommand` hook and `OverlayActive` registration work at startup. The dynamic critical bonus was validated on-map. End-of-action healing, simultaneous critical/healing effects and combat display still require tests.
