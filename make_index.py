"""Generate index.json for the Maya Skills Marketplace.

Scans skills/*/ folders, reads each skill.json, computes the directory sha256 and
writes index.json.  Run after adding or editing any skill:  python make_index.py

WHY THE HASH IS NORMALISED
--------------------------
This script used to hash the raw bytes of the working copy — the same algorithm
Maya's ``skill_installer.dir_sha256`` uses.  That looks correct and is not: git
rewrites line endings on checkout (``core.autocrlf``), so a skill is CRLF in a
Windows working copy and LF in the zipball ``codeload.github.com`` serves to
Maya.  The two hash differently, and on 2026-08-13 **every one of the ten
published skills** failed installation with "Hash verification FAILED — skill
files index se match nahi karte", which reads to the user like tampering.

So the hash written here normalises every file to LF first.  That value is
checkout-independent: it is what Maya computes over a freshly downloaded zipball
whatever git did to this machine's working copy.

Never hand-edit a sha256 in index.json — run this script.
"""
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SKILLS_DIR = ROOT / "skills"
REPO = "HunterisLive-1/maya-skills-marketplace"
BRANCH = "main"


def dir_sha256(folder: Path) -> str:
    """Deterministic hash of a skill folder: sorted relpaths + LF-normalised bytes."""
    h = hashlib.sha256()
    for fp in sorted(folder.rglob("*")):
        if fp.is_file():
            rel = fp.relative_to(folder).as_posix()
            h.update(rel.encode("utf-8") + b"\0")
            h.update(fp.read_bytes().replace(b"\r\n", b"\n"))
            h.update(b"\0")
    return h.hexdigest()


def main():
    entries = []
    for folder in sorted(SKILLS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        mf = folder / "skill.json"
        if not mf.is_file():
            print(f"SKIP {folder.name}: no skill.json")
            continue
        manifest = json.loads(mf.read_text(encoding="utf-8"))
        entries.append({
            "name": manifest["name"],
            "description": manifest.get("description", ""),
            "version": manifest.get("version", "1.0.0"),
            "author": manifest.get("author", "unknown"),
            "type": manifest.get("type", "python"),
            "path": f"skills/{folder.name}",
            "sha256": dir_sha256(folder),
        })
        print(f"OK   {manifest['name']} ({manifest.get('type', 'python')})")

    index = {
        "marketplace": "Maya Skills Marketplace",
        "version": 1,
        "updated": date.today().isoformat(),
        "repo": REPO,
        "branch": BRANCH,
        "skills": entries,
    }
    # newline="\n": this file is checked out on Windows too, and letting Python
    # translate to CRLF makes every regeneration a whole-file diff.
    with (ROOT / "index.json").open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    print(f"\nindex.json written with {len(entries)} skills.")


if __name__ == "__main__":
    main()
