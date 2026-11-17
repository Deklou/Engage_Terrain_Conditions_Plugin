#!/usr/bin/env python3
"""Temporary, reversible Groundswell tests on the installed Emblem_Rework XML."""
import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_ID = "SID_地脈吸収"
CHANGES = {
    "crit": {
        "Timing": "3",
        "Condition": "OverlayActive &gt; 0",
        "ActNames": "必殺値;",
        "ActOperations": "+;",
        "ActValues": "10;",
        "GiveTarget": "0",
        "GiveSids": "",
        "OverlapRange": "",
        "OverlapTerrain": "",
    },
    "heal": {
        "Timing": "26",
        "Condition": "OverlayActive &gt; 0",
        "ActNames": "HP;",
        "ActOperations": "+;",
        "ActValues": "10;",
        "GiveTarget": "0",
        "GiveSids": "",
        "OverlapRange": "",
        "OverlapTerrain": "",
    },
}


def skill_file() -> Path:
    custom = os.getenv("RYUJINX_DIR")
    if custom:
        base = Path(custom)
    else:
        appdata = subprocess.check_output(
            ["cmd.exe", "/c", "echo %APPDATA%"],
            stderr=subprocess.DEVNULL, text=True,
        ).strip()
        if not appdata or "%APPDATA%" in appdata:
            raise ValueError("Dossier Ryujinx introuvable : définis RYUJINX_DIR")
        base = Path(subprocess.check_output(
            ["wslpath", "-u", appdata + r"\Ryujinx"], text=True,
        ).strip())
    return base / "sdcard/engage/mods/Emblem_Rework/patches/xml/Skill.xml"


def modified(original: bytes, mode: str = "crit") -> bytes:
    bom = b"\xef\xbb\xbf"
    content = original.decode("utf-8-sig")
    pattern = re.compile(r'^([ \t]*<Param\b[^\r\n]*\bSid="' + SKILL_ID + r'"[^\r\n]*/>)', re.M)
    matches = list(pattern.finditer(content))
    if len(matches) != 1:
        raise ValueError(f"{SKILL_ID} : {len(matches)} ligne(s) trouvée(s), attendu 1")
    line = matches[0].group(1)
    for key, value in CHANGES[mode].items():
        attr = re.compile(r'(?<![\w.])' + re.escape(key) + r'="[^"]*"')
        if len(attr.findall(line)) != 1:
            raise ValueError(f"Attribut XML introuvable ou ambigu : {key}")
        line = attr.sub(lambda m, k=key, v=value: f'{k}="{v}"', line, count=1)
    result = content[:matches[0].start()] + line + content[matches[0].end():]
    return (bom if original.startswith(bom) else b"") + result.encode("utf-8")


def known_mode(original: bytes, current: bytes) -> str | None:
    if current == original:
        return "original"
    for mode in CHANGES:
        if current == modified(original, mode):
            return mode
    return None


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"enable", "crit", "heal", "restore"}:
        sys.exit("Usage : python3 scripts/groundswell_test.py crit|heal|restore")
    requested = "crit" if sys.argv[1] == "enable" else sys.argv[1]
    path = skill_file()
    backup = path.with_name(path.name + ".groundswell.bak")
    if not path.is_file():
        sys.exit(f"Skill.xml introuvable : {path}")
    current = path.read_bytes()

    if backup.exists():
        original = backup.read_bytes()
        existing_mode = known_mode(original, current)
        if existing_mode is None:
            sys.exit("Arrêt : Skill.xml a changé depuis le test. Aucun fichier modifié.")
        if requested == "restore":
            path.write_bytes(original)
            backup.unlink()
            print("Groundswell original restauré.")
            return
        if existing_mode == requested:
            print(f"Test {requested} déjà actif.")
            return
    else:
        if requested == "restore":
            sys.exit("Aucune sauvegarde du test trouvée. Aucun fichier modifié.")
        original = current
        # Save first; the original is never overwritten by later test switches.
        with backup.open("xb") as f:
            f.write(original)

    patched = modified(original, requested)
    path.write_bytes(patched)
    if requested == "crit":
        print("Test critique : +10 uniquement sur MapOverlap, sans soin.")
    else:
        print("Test soin : +10 PV après l'action sur MapOverlap, sans supprimer le terrain.")
        print("Pendant ce test, le bonus critique est désactivé.")
    print("Sauvegarde conservée :", backup)


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Erreur : {exc}")
