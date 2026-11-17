# Engage Terrain Conditions

Skyline plugin for Fire Emblem Engage 2.0.0 / Cobalt.

Adds the `OverlayActive` command for `Skill.xml` conditions. It returns `1` when a unit stands on a `MapOverlap` (such as a Dragon Vein) and `0` otherwise. Natural terrain (forest, fort, etc.) is excluded.

XML condition: `OverlayActive > 0` (stored as `OverlayActive &gt; 0` inside an XML attribute).

## Current status (17 November 2026)

**Validated in-game by the mod author, in the tested scenarios:**

- NRO build/deployment, Cobalt startup and `OverlayActive` command registration.
- Dynamic Crit +10 on an overlay, including the appearance/disappearance of a Dragon Vein under a unit that has not moved.
- End-of-action Groundswell healing on an overlay, and no corresponding heal on a normal tile.
- Combined healing + critical bonus without removing the overlay.
- Groundswell icon in real combat.
- No reported crash during the tested tactical-map scenario, world map, emblem equip/unequip menus, or Somniel arena, after the map-dimension guard was deployed.

These results do **not** prove exhaustive safety for every map, scene or simulated battle position. Fixed offsets and native signatures target **Engage 2.0.0**, not other game versions.

## Build and deploy the plugin

From the plugin repository in WSL, with Rust and cargo-skyline installed:

```sh
bash scripts/deploy.sh
```

**Close the game before deployment.** The script builds `libterrain_conditions.nro` and copies it into an **existing** `sdcard/engage/mods/Terrain_Conditions/` folder under Ryujinx. It saves the original NRO as `.bak` if that backup does not yet exist. It does not create a missing mod directory.

The Ryujinx directory is inferred from Windows `%APPDATA%`. If Ryujinx is installed elsewhere, pass `RYUJINX_DIR` pointing to the directory containing `sdcard/`.

## Permanent Groundswell XML (separate repository)

The matching, version-controlled skill configuration is in [engage_modpack PR #1](https://github.com/Deklou/engage_modpack/pull/1), branch `feat/groundswell-overlay`:

`Emblem_Rework/patches/xml/Skill.xml`

It changes **only two `<Param>` lines**, leaving the rest of the modpack intact:

- `SID_地脈吸収` (Groundswell): `Timing=26`, `Condition="OverlayActive &gt; 0"`, `HP +10`, no terrain removal, and `SyncSids="SID_Groundswell_Crit;"`.
- `SID_Groundswell_Crit`: `Timing=3`, `Condition="OverlayActive &gt; 0"`, Crit +10, `Cycle=0`, `Life=0`.

**Plugin and XML are both required.** Do not ship this XML alone: the `OverlayActive` term is provided by the NRO. Merging a PR or pulling GitHub changes does **not** automatically update Ryujinx's installed mod files.

### Transition from temporary `combo` test to permanent XML

1. **Close Engage in Ryujinx.** Keep a backup of the currently installed `Emblem_Rework/patches/xml/Skill.xml` (and the test-created `Skill.xml.groundswell.bak` if present).
2. In GitHub Desktop, fetch/pull `engage_modpack` branch `feat/groundswell-overlay` after checking for local changes. Locate its versioned `Skill.xml`.
3. Compare that complete versioned file with Ryujinx's installed `Skill.xml`. If they are **byte-for-byte identical**, the running `combo` configuration already equals the permanent XML; no extra XML replacement is needed. If they differ, **stop and review the diff**: there might be other local mod changes or line-ending differences. Never overwrite unrelated changes blindly.
4. After merging the **plugin PR first**, then the **modpack PR**, pull each `main` in GitHub Desktop and repeat the versioned-versus-installed XML comparison. The plugin NRO must still be present.
5. Perform one final launch/quick Groundswell check using the installed XML. Keep backups until the final validation; archive or remove the temporary test backup only after verifying the permanent installation.

**Do not run `groundswell_test.py restore` as part of the final transition.** That command restores the *pre-test XML*, not the permanent version from GitHub.

## Temporary diagnostic test modes (not the installation method)

The reversible test script modifies the **installed** `Emblem_Rework` XML and saves the pre-test bytes as `Skill.xml.groundswell.bak`:

```sh
python3 scripts/groundswell_test.py crit
python3 scripts/groundswell_test.py heal
python3 scripts/groundswell_test.py combo
```

- `crit`: isolated Crit +10 on an overlay, without healing.
- `heal`: isolated Groundswell healing after an action, without Crit +10.
- `combo`: dynamic Crit +10 and end-of-action healing together.

Only for a **temporary diagnostic test**, and only if you explicitly intend to return to the saved pre-test version:

```sh
python3 scripts/groundswell_test.py restore
```

The test script refuses to overwrite unexpected installed XML changes. No NRO rebuild is necessary for XML-only changes. Keep the game closed when changing test modes.

## Related pull requests

- [Terrain Conditions plugin PR #1](https://github.com/Deklou/Engage_Terrain_Conditions_Plugin/pull/1)
- [Permanent Groundswell XML PR #1](https://github.com/Deklou/engage_modpack/pull/1)
