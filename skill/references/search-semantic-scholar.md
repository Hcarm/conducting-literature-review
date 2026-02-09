# Semantic Scholar Search Strategies

Semantic Scholar-specific search guidance for use with the zongmin-yu/semantic-scholar-fastmcp MCP server. Load this module when executing Semantic Scholar database search rounds (source type 4).

---

## Validated Operational Guidance

### Search Endpoint Behavior

- **`paper_relevance_search` is frequently rate-limited (HTTP 429) when unauthenticated.** Expect this endpoint to fail on first attempt. Plan workflow to attempt S2 keyword search but fall back gracefully to DOI lookup + citation chaining if search is unavailable.
- **Rate limiting is persistent within a session.** Multiple retry attempts within the same session do not resolve 429 errors. Unlike intermittent network failures, S2 rate limiting reflects a quota that resets on a longer cycle.
- **S2 keyword search (`paper_relevance_search`, `paper_bulk_search`) is unvalidated.** During Step 4 validation, every keyword search attempt returned HTTP 429. All S2 contributions (Dun 2024, Dun 2022, Ginn 2021) came through DOI lookup + citation chaining. The degraded-mode workflow is validated; the primary keyword search pathway is not. Re-test when an authenticated API key is available.

### Reliable Endpoints (Unauthenticated)

- **`paper_details` with DOI lookup is the most reliable entry point.** Format: `DOI:10.1000/xyz`. Tested extensively; works consistently. Use this to look up papers discovered via PubMed or web search and obtain S2 paper IDs for citation chaining.
- **`paper_details` with PMID lookup** also works: `PMID:12345678`.
- **`paper_citations` (forward citations) works after obtaining S2 paper IDs.** Tested with multiple seeds; returns structured data including title, year, venue, citation count. This is the primary S2 discovery tool when keyword search is unavailable.
- **`paper_references` may return null for some papers.** Publisher restrictions can block reference data. If `data: null` is returned, skip and note in operational log.

### Field Validation

- **`paper_citations` and `paper_references` do NOT support `externalIds` as a field.** Valid fields: `contexts, isInfluential, paperId, venue, year, title, abstract, intents, citationCount, influentialCitationCount, url, authors`. Attempting `externalIds` produces a validation error.
- **`paper_details` DOES support `externalIds`.** Use this to get PMIDs, DOIs, and other identifiers for papers found via citation chaining.

### Recommended S2 Workflow

1. Look up 2-3 key seed papers via `paper_details` with DOI (get S2 paper IDs)
2. Run `paper_citations` on each seed (limit 30) for forward citation discovery
3. Screen citing papers by title, year, venue, and citation count
4. Look up promising citing papers via `paper_details` for full metadata including `externalIds`
5. Use the PMIDs from `externalIds` to fetch abstracts via PubMed `pubmed_fetch_contents`

### Recommendation Endpoints

- **`get_paper_recommendations_single` returns empty for non-CS fields.** The "recent" pool covers only ~60 days and does not include health sciences papers. For health sciences literature reviews, S2 recommendations are not a viable discovery source. **Use PubMed Similar Articles (via `pubmed_article_connections`) instead.**
- **`get_paper_recommendations_multi`** was not tested but likely has the same pool limitation.

### Key Discovery Value

S2 citation chaining discovers papers that PubMed ELink does not. In validation testing, S2 citation chaining found Ginn 2021, Dun 2024, and Dun 2022 -- none of which were found via PubMed `pubmed_citedin`. S2's citation database has broader journal coverage than PubMed's ELink service.

---

## MCP Tools Reference

| Tool | Purpose | Key Parameters |
|------|---------|---------------|
| `paper_relevance_search` | Relevance-ranked search | query, fields, year, min_citation_count, fields_of_study, venue |
| `paper_bulk_search` | Large-set retrieval with sorting | query, sort, publication_types, year, fields_of_study |
| `paper_title_search` | Find specific paper by title | query, fields |
| `paper_details` | Single paper metadata | paper_id (S2 ID, DOI, ARXIV, PMID formats) |
| `paper_batch_details` | Batch metadata (up to 500) | paper_ids, fields |
| `paper_citations` | Forward citations (papers citing this one) | paper_id, fields, limit |
| `paper_references` | Backward references (papers cited by this one) | paper_id, fields, limit |
| `get_paper_recommendations_single` | Single-seed recommendation | paper_id, from_pool, limit |
| `get_paper_recommendations_multi` | Multi-seed recommendation | positive_paper_ids, negative_paper_ids, limit |

---

## Query Construction

### Search Fields

`paper_relevance_search` matches against titles, abstracts, venue names, and author names. Use natural language terms from Core Concepts:

- Single-concept: `"regression to the mean adjustment methods"`
- Cross-concept: `"instrumental variables quality improvement"`
- Cross-disciplinary: use the Variants column terms

### Useful Filters

- `fields_of_study`: target specific disciplines (e.g., "Medicine", "Economics", "Computer Science")
- `year`: restrict by publication year (e.g., "2015-2025")
- `min_citation_count`: filter for established work
- `publication_types`: filter by type (e.g., "Review", "JournalArticle")

### Paper ID Formats

Semantic Scholar accepts multiple identifier formats:
- `DOI:10.1000/xyz`
- `PMID:12345678`
- `ARXIV:2106.15928`
- Native S2 ID (40-character hex)

---

## Rate Limiting

- **Authenticated**: 1 request/second
- **Unauthenticated**: 100 requests per 5 minutes (~0.33 req/sec)
- Plan query volume to stay within limits
- On HTTP 429: wait 60 seconds, retry once, skip remaining Semantic Scholar queries if retry fails
- Record in Search Status: "Semantic Scholar: Rate-Limited after N/M queries"

---

## Pool Limitations for Recommendations

The `get_paper_recommendations_single` and `get_paper_recommendations_multi` tools have pool restrictions:

| Pool | Coverage | Use When |
|------|----------|----------|
| `recent` (default) | ~60-day window of papers | Non-CS fields; most health sciences searches |
| `all-cs` | All computer science papers | CS-specific topics only |

There is no "all papers" pool for non-CS fields. For health sciences, the "recent" pool limits recommendations to papers from the last ~60 days. PubMed Similar Articles (via search-recommendations.md) covers the full historical corpus and should be preferred for comprehensive recommendation coverage.

---

## Per-Seed Caps

For citation retrieval (`paper_citations`, `paper_references`):
- Limit to first page of results: `limit: 50` per call
- Do not paginate further for any single seed
- This ensures no single seed consumes more than one API call per direction (forward/backward)

---

## Documentation

Record Semantic Scholar search rounds per the documentation format in search-strategies.md. Source Type: "Semantic Scholar". Tool: the specific MCP tool name used.
