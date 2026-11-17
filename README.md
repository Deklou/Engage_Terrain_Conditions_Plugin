# Engage Terrain Conditions

Adds the `OverlayActive` condition to Fire Emblem Engage 2.0.0. It returns `1` if a unit is on a map overlay (such as a Dragon Vein), otherwise `0`. Normal terrain is ignored.

In `Skill.xml`:

```xml
Condition="OverlayActive &gt; 0"
```

Build and install from WSL, with Ryujinx closed:

```sh
bash scripts/deploy.sh
```

Requires Cobalt and an existing `sdcard/engage/mods/Terrain_Conditions/` folder. Groundswell uses this condition in `engage_modpack`.
