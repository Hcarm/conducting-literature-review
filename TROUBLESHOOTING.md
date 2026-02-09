# Troubleshooting

Organized by symptom. If your issue is not listed here, check the relevant documentation:
- [docs/api-keys.md](docs/api-keys.md) -- API key acquisition and configuration
- [docs/mcp-setup.md](docs/mcp-setup.md) -- MCP server installation and configuration
- [docs/permissions.md](docs/permissions.md) -- Claude Code permission configuration

---

## MCP Server Issues

### "PubMed: Unavailable" during Phase 0 health check

**Likely cause**: MCP server not configured in `~/.claude.json`, or Node.js/npx not available.

**Resolution**:
1. Verify `~/.claude.json` contains the `pubmed-mcp-server` entry (see `setup/examples/claude-json-snippet.json`)
2. Verify the key name is exactly `"pubmed-mcp-server"` (not `"pubmed"` or `"pubmed-server"`)
3. Verify Node.js is installed: `node --version` (must be v18+)
4. Verify npx is available: `npx --version`
5. Test the server manually: `npx @cyanheads/pubmed-mcp-server --help`

### "Semantic Scholar: Unavailable" during Phase 0 health check

**Likely cause**: Python venv path is incorrect in `~/.claude.json`, or the venv does not exist.

**Resolution**:
1. Verify `~/.claude.json` contains the `semantic-scholar` entry
2. Verify the key name is exactly `"semantic-scholar"` (not `"semanticscholar"` or `"s2"`)
3. Verify the `command` path is **absolute** and points to the venv Python executable:
   - macOS/Linux: `~/.claude/mcp-servers/semantic-scholar-fastmcp/.venv/bin/python`
   - Windows: `C:\Users\<you>\.claude\mcp-servers\semantic-scholar-fastmcp\.venv\Scripts\python.exe`
4. Verify the `args` path to `run.py` is also absolute
5. Verify the venv exists: check that the Python executable at the path exists
6. If missing, re-run the install script or manually create the venv (see [docs/mcp-setup.md](docs/mcp-setup.md))

### "Semantic Scholar: Rate-Limited" on every keyword search

**Likely cause**: This is expected behavior, not a configuration error.

**Explanation**: Semantic Scholar's keyword search endpoints (`paper_relevance_search`, `paper_bulk_search`) are frequently rate-limited (HTTP 429) for unauthenticated access. During validation testing, every keyword search attempt returned 429. The skill is designed for this -- it falls back to DOI lookup + forward citation chaining, which is the validated and reliable workflow.

**When to investigate further**: If `paper_details` (DOI lookup) also fails, the issue may be network-level (firewall, proxy) rather than rate limiting.

### MCP tool calls return "tool not found"

**Likely cause**: Server name mismatch between `~/.claude.json` and SKILL.md.

**Resolution**: The SKILL.md `allowed-tools` field references tools as `mcp__<server-name>__<tool-name>`. The `<server-name>` segment must match the key in your `~/.claude.json` `mcpServers` object. Required names:
- `pubmed-mcp-server` (not `pubmed`, `pubmed_server`, etc.)
- `semantic-scholar` (not `semanticscholar`, `s2`, etc.)

---

## Permission Issues

### Claude denies WebSearch permission

**Resolution**: Add `"WebSearch"` to the `permissions.allow` array in `~/.claude/settings.json`. See `setup/examples/settings-snippet.json`.

### Claude denies WebFetch for a specific domain

**Resolution**: Add `"WebFetch(domain:example.com)"` to the `permissions.allow` array. The settings snippet includes common academic domains. Add additional domains as needed for your research field.

### Claude prompts for permission on every MCP tool call

**Resolution**: Add the specific MCP tool permissions to `settings.json`. See `setup/examples/settings-snippet.json` for the complete list. Alternatively, use a less restrictive permission mode during reviews.

---

## Script Issues

### `init_review.py` fails with "Template not found"

**Likely cause**: The skill symlink is broken or points to the wrong directory.

**Resolution**:
1. Verify the symlink exists: check `~/.claude/skills/conducting-literature-review`
2. Verify it points to the `skill/` directory in the cloned repo (not the repo root)
3. Verify `templates/` exists inside the symlink target: `ls ~/.claude/skills/conducting-literature-review/templates/`
4. If the symlink is broken, remove it and re-create it:
   ```bash
   rm ~/.claude/skills/conducting-literature-review
   ln -s /path/to/repo/skill ~/.claude/skills/conducting-literature-review
   ```

### `verify_citations.py` returns network errors

**Likely cause**: Firewall or proxy blocking access to CrossRef API.

**Resolution**: The script contacts `api.crossref.org` on port 443 (HTTPS). Verify this is accessible:
```bash
curl -s https://api.crossref.org/works/10.1038/nature12373 | head -c 200
```
If blocked, the skill still functions -- DOI verification is reported as "Pending" and can be completed later.

---

## Review State Issues

### Review state appears corrupted or inconsistent

**Likely cause**: A previous session ended unexpectedly, leaving partial writes in state files.

**Resolution**: The skill detects inconsistencies on resume and offers reconstruction:
1. If the Paper Tracking table is inconsistent with Literature_Review.md entries, the skill re-syncs from Literature_Review.md
2. If REVIEW_PROGRESS.md is unreadable, the skill offers to start fresh (the corrupted review remains in its subfolder for reference)
3. Users can manually edit REVIEW_PROGRESS.md between sessions -- the skill accepts reasonable edits

### Multiple in-progress reviews cause confusion

**Resolution**: The skill presents a choice via AskUserQuestion when multiple reviews are in progress. To clean up old reviews, set their Status to "Abandoned" in `Literature/INDEX.md`.

### Mode upgrade (narrow to full) lost state

**Resolution**: Mode upgrade preserves all Phase 2 progress. Completed source types count toward expanded budgets. The upgrade adds supplementary interview questions and expands Phase 4 from abbreviated to complete. If state appears lost, check REVIEW_PROGRESS.md -- the upgrade is recorded in the Mode field and Session Notes.

---

## Performance Issues

### Full review is taking many sessions

**Expected behavior**: Full reviews (30-48+ papers) typically span 2-4 Claude Code sessions. The pipeline is designed for multi-session operation. All state persists in files.

**To reduce session count**:
- Provide artifacts in Phase 1 (reduces interview time)
- Provide known exemplar papers (seeds citation chaining without keyword discovery)
- Start with a narrow search and upgrade if needed

### Phase 3 is slow for many papers

**Expected behavior**: Phase 3 processes each paper individually. For 40+ papers, this takes significant session time.

**Batched processing**: When candidates exceed 50, the skill automatically processes in batches of ~25 to manage context window usage. Each batch completes 3A-3B before the next begins.

---

## Installation Issues

### Windows symlink creation fails

**Cause**: Creating symbolic links on Windows requires either Administrator privileges or Developer Mode.

**Resolution**:
1. Enable Developer Mode: Settings > Privacy & Security > For developers > Developer Mode
2. Or run the install script as Administrator
3. The install script falls back to a directory junction (`mklink /J`) if symlink creation fails. Junctions do not require elevated privileges and work identically for this use case.

### Semantic Scholar venv creation fails

**Possible causes**:
- Python 3.10+ not installed
- `python3` command not in PATH (try `python` on Windows)
- Insufficient disk space for venv (~100 MB)

**Resolution**: Ensure Python 3.10+ is installed and accessible. On Windows, the Python installer adds `python` to PATH by default. On macOS, use `python3` (the system `python` may be Python 2).

### `npx @cyanheads/pubmed-mcp-server` fails

**Possible causes**:
- Node.js not installed or below v18
- npm cache corrupted
- Corporate proxy blocking npm registry

**Resolution**:
1. Verify Node.js: `node --version` (must be v18+)
2. Clear npm cache: `npm cache clean --force`
3. If behind a proxy: configure npm proxy settings (`npm config set proxy http://...`)
