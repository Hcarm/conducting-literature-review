# PubMed Search Strategies

PubMed-specific search guidance for use with the cyanheads/pubmed-mcp-server MCP server. Load this module when executing PubMed database search rounds (source type 3).

---

## Validated Operational Guidance

### Query Syntax

- **Multi-word phrases require quoting or field tags.** Unquoted multi-word queries (e.g., `regression to the mean`) may return 0 results due to automatic term mapping failure. Always use either phrase quotes (`"regression to the mean"`) or field tags (`"regression to the mean"[TIAB]`).
- **Combine field tags with phrases for best results.** Example: `"regression to the mean"[TIAB] AND ("quality improvement"[TIAB] OR "provider performance"[TIAB])`.
- **Boolean operators are case-sensitive.** Use uppercase `AND`, `OR`, `NOT`.

### Metadata Retrieval

- `pubmed_fetch_contents` with `abstract_plus` is the standard retrieval mode. Returns abstract, authors with affiliations, journal info, DOI, publication types, and article dates. Sufficient for Level 2-3 annotation without full text.
- **DOI field may be empty** in ESummary responses. Use `pubmed_fetch_contents` (EFetch) for more reliable DOI retrieval.
- **Batch fetch works well.** Up to 200 PMIDs per call. Tested with 12-13 PMIDs in a single call without issues.
- MeSH terms in `abstract_plus` output are useful for relevance screening and concept mapping.

### Citation Network Tools

- `pubmed_article_connections` with `pubmed_similar_articles` returns topically broad results. Useful for serendipitous discovery but produces many off-topic matches. Apply strict relevance screening.
- `pubmed_article_connections` with `pubmed_citedin` is unreliable. ELink citation databases do not cover all journals. Tested with 4 well-cited seeds across 2 validation tests; all returned 0 citing articles. **Do not rely on this for citation discovery. Use Semantic Scholar `paper_citations` as the primary citation chaining tool.** Attempting `pubmed_citedin` is low-cost (skip on empty results) but should not count toward citation chaining coverage.
- `pubmed_article_connections` with `pubmed_references` was not tested but may have similar coverage limitations.

### Performance

- No rate limiting encountered during validation (unauthenticated, moderate query volume of ~15 queries per session).
- Response times are fast (under 2 seconds per query).

---

## MCP Tools Reference

| Tool | Purpose | Key Parameters |
|------|---------|---------------|
| `pubmed_search_articles` | Keyword search | queryTerm, maxResults, sortBy, dateRange, filterByPublicationTypes |
| `pubmed_fetch_contents` | Retrieve full metadata | pmids, detailLevel (abstract_plus, full_xml, medline_text, citation_data) |
| `pubmed_article_connections` | Citation network and similar articles | sourcePmid, relationshipType (pubmed_similar_articles, pubmed_citedin, pubmed_references) |

---

## Query Construction

### MeSH Terms

PubMed indexes articles with Medical Subject Headings (MeSH). Translating Core Concepts search terms to MeSH equivalents improves precision:

- Use `[MeSH]` field tag for controlled vocabulary terms
- Use `[TIAB]` for title/abstract free-text search
- Combine: `"quality improvement"[MeSH] OR "quality improvement"[TIAB]`

### Field Tags

| Tag | Field | Use |
|-----|-------|-----|
| `[TIAB]` | Title/Abstract | Free-text concept terms |
| `[MeSH]` | MeSH heading | Controlled vocabulary |
| `[AU]` | Author | Known-author search |
| `[PT]` | Publication Type | Filter by study design |
| `[DP]` | Date of Publication | Time range filter |

### Boolean Operators

PubMed supports AND, OR, NOT. Construct queries by combining Core Concepts:
- Within a concept: OR terms (`"audit and feedback" OR "performance feedback"`)
- Between concepts: AND (`("audit and feedback"[TIAB]) AND ("intensive care"[TIAB])`)

---

## Rate Limiting

- **Authenticated**: 10 requests/second
- **Unauthenticated**: 3 requests/second
- On HTTP 429: wait 60 seconds, retry once, skip remaining PubMed queries if retry fails
- Record in Search Status: "PubMed: Rate-Limited after N/M queries"

---

## Documentation

Record PubMed search rounds per the documentation format in search-strategies.md. Source Type: "PubMed". Tool: the specific MCP tool name used.
