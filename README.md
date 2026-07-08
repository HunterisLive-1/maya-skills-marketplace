# Maya Skills Marketplace

Official skill catalog for [Maya](https://github.com/HunterisLive-1) — the voice-first Windows AI assistant.
Maya installs skills from here by voice ("marketplace se password generator install karo") or from the HUD's **SKILLS** tab.

## Skill types

| Type | File | What it does |
|------|------|--------------|
| `python` | `skill.py` | Executable script Maya runs on demand (sandboxed subprocess, 15s timeout) |
| `prompt` | `SKILL.md` | Knowledge/instructions injected into Maya's system prompt — teaches Maya new behavior without code |

## Package format

```
skills/my_skill/
├── skill.json     # manifest (required for marketplace)
├── skill.py       # python skills
└── SKILL.md       # prompt skills
```

`skill.json`:

```json
{
  "name": "my_skill",
  "description": "One-line description (Hinglish ok)",
  "version": "1.0.0",
  "author": "Your Name",
  "type": "python",
  "requirements": []
}
```

Rules for `python` skills:
- stdlib preferred; must run standalone with **no arguments and empty stdin** (that's the install test)
- print results to stdout; handle all errors (never crash, never `input()`)
- optional stdin input for parameters, with sensible defaults

## Adding a skill

1. Create `skills/<name>/` with `skill.json` + `skill.py` or `SKILL.md`
2. Run `python make_index.py` (regenerates `index.json` with sha256 hashes)
3. Commit + push. Maya verifies the hash before installing.

## Security

Maya hash-verifies every marketplace download against `index.json`, test-runs python skills
in a sandboxed subprocess before install, and never auto-installs pip requirements.
