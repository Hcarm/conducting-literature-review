# Permission Configuration

Claude Code gates tool access through a permission system. The skill needs specific permissions to function. This document explains what each permission category does, why the skill needs it, and how to configure it.

---

## Where Permissions Are Configured

Permissions are set in `~/.claude/settings.json` under the `permissions.allow` array. See [setup/examples/settings-snippet.json](../setup/examples/settings-snippet.json) for the complete allowlist.

---

## Permission Categories

### WebSearch

```json
"WebSearch"
```

**What it does**: Allows Claude Code to perform web searches.

**Why the skill needs it**: WebSearch is the primary discovery tool for Phase 2 search rounds. Source types 1 (web search) and 2 (grey literature) both use WebSearch queries. Without it, the skill relies exclusively on database APIs (PubMed and Semantic Scholar MCP servers) for paper discovery. This is viable but eliminates grey literature discovery and reduces cross-disciplinary coverage.

**Impact of denying**: The skill reports: "Web search and web fetch are unavailable. The review will rely on database APIs for discovery and MCP metadata for content retrieval." The review proceeds with reduced source diversity.

---

### WebFetch (per domain)

```json
"WebFetch(domain:pubmed.ncbi.nlm.nih.gov)"
```

**What it does**: Allows Claude Code to fetch web pages from specific domains.

**Why the skill needs it**: During Phase 3 exemplar processing, the skill retrieves abstracts and open-access full text from publisher websites for Level 4 deep extraction. Without pre-approved domains, Claude Code prompts the user for each new domain encountered during search, interrupting the workflow.

**Domain categories**:

| Category | Domains | Purpose |
|----------|---------|---------|
| NCBI | pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov, ncbi.nlm.nih.gov | PubMed abstracts, PMC full text, NCBI resources |
| Preprints | arxiv.org | Physics, CS, and cross-disciplinary preprints |
| DOI resolution | doi.org | Resolve DOIs to publisher pages |
| Discovery | scholar.google.com | Google Scholar results |
| Publishers | jamanetwork.com, biomedcentral.com, academic.oup.com, onlinelibrary.wiley.com, springer.com, journals.plos.org, sciencedirect.com, nejm.org, thelancet.com, bmj.com | Journal article abstracts and open-access full text |
| Working papers | nber.org | Economics working papers |
| Government | psnet.ahrq.gov, ahrq.gov, hhs.gov | Patient safety, health services research reports |

**Customization**: Add or remove domains based on your research field. The listed domains cover major biomedical and social science publishers. If you work in other fields (e.g., pure CS, engineering), you may want to add domain-specific publishers.

**Impact of denying**: The skill still functions. Claude Code prompts for permission on each new domain encountered. This adds friction but does not block the review.

---

### MCP Tool Permissions

```json
"mcp__pubmed-mcp-server__pubmed_search_articles"
```

**What it does**: Allows the skill to call specific MCP server tools.

**Why the skill needs it**: Each MCP tool performs a distinct function in the search pipeline. The SKILL.md `allowed-tools` frontmatter declares which tools the skill can use, but the user-level permissions in `settings.json` act as an additional gate.

**Tool roles**:

| Tool | Phase | Role |
|------|-------|------|
| `pubmed_search_articles` | 2 | PubMed keyword search |
| `pubmed_fetch_contents` | 3 | Retrieve structured abstracts and metadata |
| `pubmed_article_connections` | 2, 6 | Similar articles (source 6) and citation network |
| `pubmed_generate_chart` | 5 | Chart generation (rarely used) |
| `paper_relevance_search` | 2 | S2 keyword search (often rate-limited) |
| `paper_bulk_search` | 2 | S2 bulk search with sorting |
| `paper_title_search` | 2, 5 | Find specific papers by title |
| `paper_details` | 2, 3 | Paper metadata via DOI/PMID/S2 ID |
| `paper_batch_details` | 3 | Batch metadata retrieval |
| `paper_citations` | 5 | Forward citation chaining |
| `paper_references` | 5 | Backward reference retrieval |
| `get_paper_recommendations_single` | 6 | Single-seed recommendations |
| `get_paper_recommendations_multi` | 6 | Multi-seed recommendations |
| `author_search` | 2 | Author name search |
| `author_details` | 3 | Author profile lookup |

**Impact of denying individual tools**: The skill degrades gracefully. If a tool is unavailable, the skill reports the limitation and skips that source type or falls back to an alternative pathway.

---

### Built-in Tool Permissions

The skill also uses Claude Code's built-in tools:

| Tool | Purpose |
|------|---------|
| `Read` | Read project files, existing reviews, user-provided artifacts |
| `Write` | Create review output files (REVIEW_PROGRESS.md, Literature_Review.md, etc.) |
| `Edit` | Update state files during multi-session reviews |
| `Glob` | Search for existing review folders, PDFs in Full_text_references/ |
| `Grep` | Search within review files for specific papers or status values |
| `Bash` | Execute Python scripts (init_review.py, verify_citations.py) |
| `AskUserQuestion` | Interview phase questions, mode selection, checkpoint confirmations |

These are standard Claude Code tools. Most permission modes allow them by default. If your permission mode is restrictive, you may need to approve them on first use.

---

## Permission Mode Recommendations

Claude Code supports multiple permission modes. For the skill:

- **Default mode**: Works well. Claude Code prompts for approval on first use of each tool category. After approval, subsequent calls proceed without prompting.
- **Allowlist mode**: Add the permissions from `settings-snippet.json` to avoid per-call prompts during the review.
- **Restrictive mode**: The skill functions but prompts frequently, which interrupts the search workflow. Consider temporarily switching to a less restrictive mode during reviews.

---

## Minimal Configuration

If you want the smallest possible permission set, these are the essential permissions:

```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "mcp__pubmed-mcp-server__pubmed_search_articles",
      "mcp__pubmed-mcp-server__pubmed_fetch_contents",
      "mcp__semantic-scholar__paper_details",
      "mcp__semantic-scholar__paper_citations"
    ]
  }
}
```

This enables: web search discovery, PubMed keyword search and metadata, Semantic Scholar DOI lookup and citation chaining. Everything else either falls back or prompts for approval on demand.
