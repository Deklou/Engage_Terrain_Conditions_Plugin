#!/usr/bin/env python3
"""Temporary Groundswell XML test; restore the original row afterwards."""
import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_ID = "SID_地脈吸収"
CHANGES = {
    "Timing": "3",
    "Condition": "OverlayActive &gt; 0",
    "ActNames": "必殺値;",
    "ActOperations": "+;",
    "ActValues": "10;",
    "GiveTarget": "0",
    "GiveSids": "",
    "OverlapRange": "",
    "OverlapTerrain": "",
}


def skill_file() -> Path:
    custom = os.getenv("RYUJINX_DIR")
    if custom:
        base = Path(custom)
    else:
        appdata = subprocess.check_output(
            ["cmd.exe", "/c", "echo %APPDATA%"],
            stderr=subprocess.DEVNULL, text=True
        ).strip()
        if not appdata or "%APPDATA%" in appdata:
            raise ValueError("Dossier Ryujinx introuvable : définis RYUJINX_DIR")
        base = Path(subprocess.check_output(
            ["wslpath", "-u", appdata + r"\Ryujinx"], text=True
        ).strip())
    return base / "sdcard/engage/mods/Emblem_Rework/patches/xml/Skill.xml"


def modified(original: bytes) -> bytes:
    bom = b"\xef\xbb\xbf"
    content = original.decode("utf-8-sig")
    pattern = re.compile(r'^([ \t]*<Param\b[^\r\n]*\bSid="' + SKILL_ID + r'"[^\r\n]*/>)', re.M)
    matches = list(pattern.finditer(content))
    if len(matches) != 1:
        raise ValueError(f"{SKILL_ID} : {len(matches)} ligne(s) trouvée(s), attendu 1")
    line = matches[0].group(1)
    for key, value in CHANGES.items():
        attr = re.compile(r'(?<![\w.])' + re.escape(key) + r'="[^"]*"')
        if len(attr.findall(line)) != 1:
            raise ValueError(f"Attribut XML introuvable ou ambigu : {key}")
        line = attr.sub(lambda m, k=key, v=value: f'{k}="{v}"', line, count=1)
    result = content[:matches[0].start()] + line + content[matches[0].end():]
    return (bom if original.startswith(bom) else b"") + result.encode("utf-8")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"enable", "restore"}:
        sys.exit("Usage : python3 scripts/groundswell_test.py enable|restore")
    path = skill_file()
    backup = path.with_name(path.name + ".groundswell.bak")
    if not path.is_file():
        sys.exit(f"Skill.xml introuvable : {path}")
    current = path.read_bytes()

    if sys.argv[1] == "enable":
        if backup.exists():
            expected = modified(backup.read_bytes())
            if current != expected:
                sys.exit("Arrêt : Skill.xml a changé depuis le test. Aucun fichier modifié.")
            print("Test Groundswell déjà actif.")
            return
        patched = modified(current)
        with backup.open("xb") as f:
            f.write(current)
        path.write_bytes(patched)
        print("Test actif : Groundswell = Crit +10 sur MapOverlap, sans soin ni suppression.")
        print("Sauvegarde :", backup)
    else:
        if not backup.is_file():
            sys.exit("Aucune sauvegarde du test trouvée. Aucun fichier modifié.")
        original = backup.read_bytes()
        if current != modified(original):
            sys.exit("Arrêt : Skill.xml a été modifié pendant le test. Restaurer manuellement.")
        path.write_bytes(original)
        backup.unlink()
        print("Groundswell original restauré.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Erreur : {exc}")
