# Contributing to mindpalace

Thanks for helping mindpalace grow! 🧠 All contributions are welcome — bug reports, ideas,
docs, **skills**, plugins, and code.

## Ways to contribute
- **Skills** — add a reference recipe to `mindpalace/skills/global/` (markdown + frontmatter).
  These ship to everyone and are some of the highest-leverage contributions.
- **Plugins** — build an extension (see `mindpalace/plugins/`). Share it as a repo or a PR to
  `contrib/`.
- **Gateways / agents** — new interfaces (`gateways/`) or cognitive agents (`agents/`).
- **Docs** — improve `docs/` or the README.
- **Bugs / features** — open an issue first for anything non-trivial.

## Dev setup
```bash
git clone https://github.com/aashutosh396/mindpalace
cd mindpalace
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[discord]"
python -m mindpalace.cli status     # sanity
```
Use `MINDPALACE_HOME=/tmp/mp-dev` to keep a throwaway data home while developing.

## Ground rules
- Keep the **core ↔ data** separation sacred: the package must never write personal data into
  the repo; everything user-specific resolves through `config.home()`.
- No secrets in the repo, ever. Tokens/creds live in the data home's `secrets/`.
- Match the existing style (concise, typed where it helps, `from __future__ import annotations`).
- Run `python -m py_compile mindpalace/**/*.py` before opening a PR.

## PRs
Small, focused PRs with a clear description. Link the issue. Be kind in review.
