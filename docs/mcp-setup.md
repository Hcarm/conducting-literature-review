# MCP Server Setup

The skill uses two MCP (Model Context Protocol) servers to query academic databases. Each server runs as a separate process that Claude Code communicates with via stdio transport.

---

## How MCP Servers Work with Claude Code

Claude Code can use external tools provided by MCP servers. Each server:

1. Is registered in `~/.claude.json` with a startup command
2. Launches as a child process when Claude Code starts
3. Advertises its tools via the MCP protocol
4. Receives tool calls from Claude Code and returns structured results

The skill's SKILL.md declares which MCP tools it can use via the `allowed-tools` YAML frontmatter field. This acts as a permission boundary -- the skill cannot call tools not in that list.

---

## PubMed MCP Server

**Package**: `@cyanheads/pubmed-mcp-server` (npm)
**Source**: [github.com/cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server)
**Runtime**: Node.js (via npx)
**Transport**: stdio

### Installation

No permanent installation is needed. The `npx` command downloads and runs the package on demand. Ensure Node.js 18+ is installed:

```bash
node --version   # must output v18.x or higher
```

### Configuration

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "pubmed-mcp-server": {
      "command": "npx",
      "args": ["@cyanheads/pubmed-mcp-server"],
      "env": {
        "NCBI_API_KEY": "YOUR_NCBI_API_KEY_HERE"
      }
    }
  }
}
```

### Server name coupling

The key `"pubmed-mcp-server"` in the config must match exactly. The skill's SKILL.md references tools as `mcp__pubmed-mcp-server__pubmed_search_articles` -- the middle segment is this key name. If you rename the server (e.g., to `"pubmed"`), all tool references break silently.

### Tools provided

| Tool | Used by Skill | Purpose |
|------|:---:|---------|
| `pubmed_search_articles` | Yes | Keyword search with MeSH terms, date ranges, publication type filters |
| `pubmed_fetch_contents` | Yes | Retrieve structured metadata (abstract, authors, DOI, MeSH terms) |
| `pubmed_article_connections` | Yes | Similar articles and citation network (forward/backward) |
| `pubmed_generate_chart` | Rarely | Chart generation from PubMed data |
| `pubmed_research_agent` | No | Research plan generation (not used by this skill) |

### Known behaviors

- **`pubmed_article_connections` with `pubmed_citedin` is unreliable.** ELink citation databases do not cover all journals. Tested with well-cited seeds; all returned 0 citing articles. The skill uses Semantic Scholar `paper_citations` as the primary forward citation tool.
- **`pubmed_article_connections` with `pubmed_similar_articles` returns broad results.** Topically adjacent but often off-topic. The skill applies strict relevance screening after retrieval.
- **No rate limiting observed** during testing at moderate query volumes (~15 queries/session) with an API key.

---

## Semantic Scholar MCP Server

**Package**: `zongmin-yu/semantic-scholar-fastmcp` (GitHub, Python)
**Source**: [github.com/zongmin-yu/semantic-scholar-fastmcp](https://github.com/zongmin-yu/semantic-scholar-fastmcp)
**Runtime**: Python 3.10+ (FastMCP framework)
**Transport**: stdio
**Pinned commit**: `580ed5a` (known-working version)

### Installation

The install script automates this. For manual installation:

```bash
# Clone to a dedicated MCP server directory
git clone https://github.com/zongmin-yu/semantic-scholar-fastmcp.git \
    ~/.claude/mcp-servers/semantic-scholar-fastmcp

cd ~/.claude/mcp-servers/semantic-scholar-fastmcp

# Pin to known-working commit
git checkout 580ed5a

# Create isolated Python environment
python3 -m venv .venv

# Install dependencies
# macOS/Linux:
.venv/bin/pip install -r requirements.txt
# Windows:
.venv\Scripts\pip install -r requirements.txt
```

### Configuration

Add to `~/.claude.json`. The `command` path must be **absolute** -- tilde expansion and relative paths do not work.

**macOS/Linux:**
```json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "/Users/yourname/.claude/mcp-servers/semantic-scholar-fastmcp/.venv/bin/python",
      "args": ["/Users/yourname/.claude/mcp-servers/semantic-scholar-fastmcp/run.py"],
      "env": {
        "SEMANTIC_SCHOLAR_API_KEY": "",
        "SEMANTIC_SCHOLAR_ENABLE_HTTP_BRIDGE": "0"
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "C:\\Users\\yourname\\.claude\\mcp-servers\\semantic-scholar-fastmcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\yourname\\.claude\\mcp-servers\\semantic-scholar-fastmcp\\run.py"],
      "env": {
        "SEMANTIC_SCHOLAR_API_KEY": "",
        "SEMANTIC_SCHOLAR_ENABLE_HTTP_BRIDGE": "0"
      }
    }
  }
}
```

### Server name coupling

The key `"semantic-scholar"` must match exactly. Tool references in SKILL.md use `mcp__semantic-scholar__paper_details` -- the middle segment is this key name.

### Python dependencies

Installed into the `.venv` by pip from `requirements.txt`:

- fastmcp (>=2.0.0, <3.0.0) -- MCP server framework
- httpx (>=0.24.0) -- async HTTP client for S2 API calls
- fastapi (>=0.115.0) -- web framework (for optional HTTP bridge, disabled)
- uvicorn (>=0.32.0) -- ASGI server (for optional HTTP bridge, disabled)
- python-dotenv (>=1.0.0) -- environment variable loading

### Tools provided

| Tool | Used by Skill | Purpose |
|------|:---:|---------|
| `paper_relevance_search` | Yes | Relevance-ranked keyword search |
| `paper_bulk_search` | Yes | Large-set retrieval with sort and filter |
| `paper_title_search` | Yes | Find a specific paper by title match |
| `paper_details` | Yes | Single paper metadata (accepts DOI, PMID, ARXIV, S2 ID) |
| `paper_batch_details` | Yes | Batch metadata for up to 500 papers |
| `paper_citations` | Yes | Forward citations (papers citing this one) |
| `paper_references` | Yes | Backward references (papers this one cites) |
| `get_paper_recommendations_single` | Yes | Single-seed recommendations |
| `get_paper_recommendations_multi` | Yes | Multi-seed recommendations with positive/negative examples |
| `author_search` | Yes | Search authors by name |
| `author_details` | Yes | Author profile and metrics |
| `author_papers` | No | List author publications |
| `author_batch_details` | No | Batch author details |

### Known behaviors

- **Keyword search is frequently rate-limited (HTTP 429).** Even within fresh sessions, `paper_relevance_search` and `paper_bulk_search` return 429. This is expected for unauthenticated access and may persist with authentication.
- **The validated workflow is DOI lookup + citation chaining.** During testing, all Semantic Scholar contributions came through `paper_details` (DOI lookup) followed by `paper_citations` (forward chaining). The skill's degraded-mode fallback is the tested, reliable path.
- **`paper_citations` and `paper_references` do not support `externalIds` as a field.** Requesting it produces a validation error. Use `paper_details` to retrieve DOIs and PMIDs for papers found via citation chaining.
- **`paper_references` may return null.** Publisher restrictions block reference data for some papers. The skill skips and documents.
- **Recommendation pool limitation**: The `"recent"` pool covers approximately 60 days for non-CS fields. There is no "all papers" pool for health sciences. PubMed Similar Articles provides historical coverage.

### Rate limits

| Authentication | Rate |
|----------------|------|
| Unauthenticated | 100 requests per 5 minutes (~0.33 req/sec) |
| Authenticated | 1 request per second (sustained) |

### Updating the pinned version

The install script pins to commit `580ed5a`. To update:

```bash
cd ~/.claude/mcp-servers/semantic-scholar-fastmcp
git fetch origin
git log --oneline origin/main -5  # review recent commits
git checkout <new-commit-hash>
.venv/bin/pip install -r requirements.txt  # in case deps changed
```

---

## Verifying MCP Servers

### Without Claude Code

Run `setup/test-apis.py` to verify API connectivity directly:

```bash
python setup/test-apis.py
```

This tests the underlying APIs (NCBI E-utilities, Semantic Scholar REST API, CrossRef) without requiring MCP servers to be running.

### Within Claude Code

The skill performs its own MCP health check during Phase 0. It probes each server with a minimal query and classifies the result as Available, Rate-Limited, or Unavailable. Results are recorded in the review's REVIEW_PROGRESS.md.

### Troubleshooting MCP connection issues

If the skill reports a server as Unavailable:

1. Verify `~/.claude.json` has the correct server entry
2. Check that the server name matches exactly (`pubmed-mcp-server`, `semantic-scholar`)
3. For Semantic Scholar: verify the absolute path to the venv Python executable
4. For PubMed: verify `npx` is available (`npx --version`)
5. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for additional diagnostics
