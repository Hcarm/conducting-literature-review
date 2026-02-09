# Database Search Strategies

Orchestrator for structured database searches via MCP servers. This file provides common concepts; per-database strategies are in dedicated modules loaded on demand.

---

## Per-Database Modules

| Database | Module | MCP Server |
|----------|--------|------------|
| PubMed | [search-pubmed.md](search-pubmed.md) | cyanheads/pubmed-mcp-server |
| Semantic Scholar | [search-semantic-scholar.md](search-semantic-scholar.md) | zongmin-yu/semantic-scholar-fastmcp |

Load the relevant module before executing database queries. Each module contains database-specific query syntax, MCP tool references, rate-limiting guidance, and result handling.

---

## Common Operations

### Translating Core Concepts to Database Queries

1. Take each concept's Search Terms from the Core Concepts table
2. For PubMed: translate terms to MeSH equivalents where possible; use field tags
3. For Semantic Scholar: use natural language terms; leverage fields_of_study filters for cross-disciplinary targeting
4. Execute single-concept and cross-concept queries per search-strategies.md query generation protocol

### Metadata Enrichment

When a paper is found via web search without structured metadata, use database APIs to enrich:
- Search by title to find the database record
- Retrieve: authors, abstract, year, journal, DOI, PMID, MeSH terms, citation count
- Prefer database metadata over web-scraped metadata for accuracy

---

## MCP Server Health Check

Health check is performed in Phase 0 (see SKILL.md). Results are recorded in REVIEW_PROGRESS.md Infrastructure Status table.

**Health check classifications**:

| Classification | Meaning | Action |
|---------------|---------|--------|
| Available | Server responds with structured results | Proceed normally |
| Rate-Limited | Server responds with 429 or throttling indicator | Report: "Server reachable but currently throttled." Attempt during search; if persistent, skip. |
| Unavailable | Server does not respond or returns error | Skip database source type; report degradation |

---

## Degraded Operation

### Single Server Unavailable

If one MCP server is unavailable, the other server's source type proceeds normally. Citation chaining and recommendation use the available server's API only.

### Compound Failure (Both Servers Unavailable)

When both PubMed and Semantic Scholar MCP servers are unavailable:

1. Report: "Both database servers are unavailable. The review will rely on web search and grey literature only, with web-based citation chaining. Database-quality search, API-based citation chaining, and seed-based recommendations are unavailable."
2. Phase 2 proceeds with sources 1-2 (web search, grey literature)
3. Source 5 (citation chaining) uses degraded web-based chaining: "papers citing [title]" as web search query (see search-citation-chaining.md)
4. Source 6 (seed-based recommendation) is skipped entirely
5. Record in REVIEW_PROGRESS.md: "Infrastructure: PubMed unavailable, Semantic Scholar unavailable. Review conducted with web + grey literature only."

### WebSearch Unavailable

When WebSearch/WebFetch are unavailable (user denies permissions):

1. Report: "Web search and web fetch are unavailable. The review will rely on database APIs for discovery and MCP metadata for content retrieval. Grey literature discovery is limited to database-indexed sources. Deep extraction (Level 4) may be limited to abstract-available information."
2. Source ordering adapts: skip sources 1-2, begin with source 3 (PubMed)
3. Content retrieval in Phase 3 uses MCP metadata and user-provided PDFs only
