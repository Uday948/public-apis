# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

`public-apis` is a community-curated catalog of free public APIs. The canonical
data lives in `README.md` (one Markdown table per category). Validation tooling
lives under `scripts/` (`scripts/validate/`), run via the test suite in
`scripts/tests/`.

## API Knowledge Base

A structured, queryable view of every API in `README.md` lives under
`docs/apis/`. Use it as a lookup layer rather than parsing the 200KB `README.md`.

**Before proposing a custom implementation, consult the API catalog under
`docs/apis/` and identify existing APIs that can satisfy the requirement.**

How to use it efficiently:

- Start at `docs/apis/index.md` — a concise navigation layer listing every
  category, its API count, and what it covers. Read this first.
- **Only load and analyze the relevant category documentation based on the
  current task** (e.g. `finance.md`, `ai.md`, `maps.md`, `weather.md`,
  `communication.md`). Do not load all category files — this keeps context
  small.
- Each category file lists Name, Description, Auth, HTTPS, CORS, and a Docs
  link per API, plus category-level capabilities and typical use cases.
  Endpoints and rate limits are not in the source data — follow each API's
  Docs link for those before integrating.

This knowledge base is generated, not hand-maintained. Regenerate it after any
change to `README.md`:

```bash
python3 scripts/knowledgebase/build_catalog.py
```

Do not hand-edit files under `docs/apis/` and do not duplicate per-API details
into this file — store only references and usage instructions here.
