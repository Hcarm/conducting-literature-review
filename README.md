# Conducting Literature Review

A Claude Code skill that conducts rigorous literature reviews through a 6-phase pipeline: Initialize, Interview, Search, Organize, Antagonize, Synthesize. Integrates PubMed and Semantic Scholar via MCP servers alongside web search for multi-source discovery. Supports multi-session operation with full state persistence in markdown files.

**Two modes**:
- **Narrow Search**: Quick answer to a specific question (8-14 papers, 1 session)
- **Full Review**: Comprehensive background for a project (30-48+ papers, 2-4 sessions)

## What This Is NOT

This is not a systematic review tool. It does not follow PRISMA methodology or produce PRISMA flow diagrams. It is a rigorous but pragmatic literature review that prioritizes finding the right methods over being exhaustive. It uses structured search (Core Concepts framework), cross-disciplinary translation, exemplar identification with deep extraction, and antagonistic self-assessment.

---

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- Node.js 18+ (for PubMed MCP server)
- Python 3.10+ (for Semantic Scholar MCP server and skill scripts)
- Git

---

## Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/<owner>/conducting-literature-review.git
cd conducting-literature-review
```

### 2. Run the install script

**macOS/Linux:**
```bash
bash setup/install.sh
```

**Windows** (PowerShell):
```powershell
powershell -ExecutionPolicy Bypass -File setup\install.ps1
```

The install script:
- Creates a symlink from `~/.claude/skills/conducting-literature-review` to `skill/`
- Clones and configures the Semantic Scholar MCP server (pinned to commit `580ed5a`)
- Verifies Node.js is available

### 3. Configure MCP servers

Add the MCP server entries to `~/.claude.json`. The install script prints the exact paths for your system. See [setup/examples/claude-json-snippet.json](setup/examples/claude-json-snippet.json) for the template.

**Key requirement**: The server names in `~/.claude.json` must be exactly `pubmed-mcp-server` and `semantic-scholar`. The skill's tool references are coupled to these names.

### 4. Obtain API keys

| API | Required? | Free? | Guide |
|-----|-----------|-------|-------|
| NCBI (PubMed) | Recommended | Yes | [docs/api-keys.md](docs/api-keys.md#ncbi-api-key-pubmed) |
| Semantic Scholar | Optional | Yes | [docs/api-keys.md](docs/api-keys.md#semantic-scholar-api-key-optional) |

### 5. Add permissions

Merge the permission entries from [setup/examples/settings-snippet.json](setup/examples/settings-snippet.json) into your `~/.claude/settings.json`. This pre-approves web search, academic publisher domains, and MCP tool access. See [docs/permissions.md](docs/permissions.md) for what each permission does.

### 6. Verify installation

```bash
python setup/test-apis.py
```

Expected output:
```
[PASS] Skill symlink: SKILL.md found
[PASS] Node.js: Found v20.x
[PASS] S2 MCP server: venv and run.py found
[PASS] PubMed API: Reachable (authenticated, 10 req/sec)
[PASS] S2 DOI lookup: Paper found
[WARN] S2 keyword search: Rate-limited (HTTP 429)
[PASS] CrossRef API: DOI resolved

6 passed, 1 warning out of 7 checks.
The skill is ready to use.
```

The WARN for S2 keyword search is expected. See [docs/api-keys.md](docs/api-keys.md#why-keyword-search-is-unreliable-regardless-of-authentication).

### 7. Use the skill

In any project directory, open Claude Code and type:

```
/conducting-literature-review
```

---

## Usage

### Starting a review

The skill begins with an interview:
1. Choose mode (Narrow Search or Full Review)
2. Provide existing project documents (optional but improves results)
3. Build Core Concepts table (the search scaffold)

### During the review

The skill searches across up to 6 source types (web, grey literature, PubMed, Semantic Scholar, citation chaining, seed-based recommendations), then organizes findings into an annotated bibliography with exemplar papers receiving deep extraction.

### Multi-session reviews

Full reviews span multiple Claude Code sessions. All state is persisted in markdown files. On re-invocation, the skill detects the in-progress review and offers to resume.

### Output

The skill creates a `Literature/` folder in your project with:
- `INDEX.md` -- master index of all reviews
- `YYYY-MM-DD_topic/REVIEW_PROGRESS.md` -- state tracking
- `YYYY-MM-DD_topic/Search_Methods.md` -- query execution log
- `YYYY-MM-DD_topic/Literature_Review.md` -- annotated bibliography with evidence tables

---

## Documentation

| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Design rationale for every component |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Symptom-based resolution guide |
| [docs/api-keys.md](docs/api-keys.md) | API key acquisition and verification |
| [docs/mcp-setup.md](docs/mcp-setup.md) | MCP server installation deep-dive |
| [docs/permissions.md](docs/permissions.md) | Why each permission is needed |
| [docs/how-it-works.md](docs/how-it-works.md) | End-to-end 6-phase pipeline walkthrough |

---

## Repository Structure

```
conducting-literature-review/
├── README.md
├── ARCHITECTURE.md
├── TROUBLESHOOTING.md
├── LICENSE
├── skill/                     # The installable skill (symlinked)
│   ├── SKILL.md               # Main definition (6-phase pipeline)
│   ├── references/            # 12 demand-loaded operational modules
│   ├── templates/             # 5 output file templates
│   └── scripts/               # 2 Python scripts (stdlib only)
├── setup/                     # Installation and testing
│   ├── install.sh             # macOS/Linux installer
│   ├── install.ps1            # Windows installer
│   ├── test-apis.py           # API connectivity tests
│   └── examples/              # Configuration snippets
└── docs/                      # Extended documentation
```

---

## How It Works (Brief)

1. **Initialize**: Health-check MCP servers, create review folder, detect prior state
2. **Interview**: Understand research needs, build Core Concepts search scaffold
3. **Search**: Multi-source discovery across 6 source types with budget governance
4. **Organize**: Deduplicate, triage, annotate (3 levels), build evidence tables
5. **Antagonize**: Self-assess for accuracy, bias, gaps, and opposing viewpoints
6. **Synthesize**: Produce final annotated bibliography with recall calibration

See [docs/how-it-works.md](docs/how-it-works.md) for the full walkthrough, or [ARCHITECTURE.md](ARCHITECTURE.md) for design rationale.

---

## Graceful Degradation

The skill adapts to infrastructure failures. If PubMed is down, it uses Semantic Scholar. If both are down, it uses web search. If web search is denied, it uses databases only. Every degradation is reported to the user. No silent failures.

---

## License

MIT. See [LICENSE](LICENSE).
