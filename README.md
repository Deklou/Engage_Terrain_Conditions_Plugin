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

With the game closed and the plugin deployed:

```sh
python3 scripts/groundswell_test.py crit
```

`crit` applies a temporary +10 critical rate only on a map overlay. Its dynamic behavior was verified in-game, including when Corrin creates a Dragon Vein under a stationary unit.

```sh
python3 scripts/groundswell_test.py heal
```

`heal` sets `Timing=26`, `Condition="OverlayActive &gt; 0"`, `HP +10` and no `OverlapRange` or `OverlapTerrain`, disabling the crit bonus. End-of-action healing triggers on overlay and not off-overlay; verify the actual amount from HP before/after, and that the overlay persists.

### Combined test (experimental)

```sh
python3 scripts/groundswell_test.py combo
```

`combo` keeps Groundswell as the end-of-action healing skill while adding `SyncSids="SID_Groundswell_Crit;"` to synchronize a separate critical skill with `Timing=3`, `Condition="OverlayActive &gt; 0"`, `Cycle=0` and `Life=0`.

This combination has **not** been validated in-game. On a fresh save/map with Camilla equipped:
1. With the **same weapon**, compare critical rate on normal terrain and after Corrin creates a vein **before Rosado acts**. The bonus must be immediate and disappear when the vein expires.
2. With Rosado missing at least 10 HP, finish an action on a vein. Verify exactly +10 HP, not just a healing animation, and verify the vein remains.
3. End an action on normal terrain to confirm no extra heal.

You can switch between `crit`, `heal`, `combo` without losing the saved original XML. Restore afterwards:

```sh
python3 scripts/groundswell_test.py restore
```

The original is saved once as `Skill.xml.groundswell.bak`; scripts refuse to overwrite a file with unexpected edits. No NRO rebuild is required for XML-only changes. Keep the game closed when switching modes.

## Status

The fixed-offset `UnitCalculator.AddCommand` hook and `OverlayActive` registration work at startup. Dynamic critical rate and isolated healing have both been validated as activating only over an overlay. The combined XML behavior, healing amount, combat display and off-map safety still require tests.
