"""Generate index.json for the Maya Skills Marketplace.

Scans skills/*/ folders, reads each skill.json, computes the directory sha256
(same algorithm as Maya's skill_installer.dir_sha256) and writes index.json.

Run after adding or editing any skill:  python make_index.py
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
    h = hashlib.sha256()
    for fp in sorted(folder.rglob("*")):
        if fp.is_file():
            rel = fp.relative_to(folder).as_posix()
            h.update(rel.encode("utf-8") + b"\0")
            h.update(fp.read_bytes())
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
    (ROOT / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"\nindex.json written with {len(entries)} skills.")


if __name__ == "__main__":
    main()
