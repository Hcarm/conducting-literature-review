# Search Methods: {{TOPIC}}

**Date**: {{DATE}}
**Mode**: {{Narrow Search | Full Review}}

---

## Research Question Decomposition

### Core Concepts

| Concept | Search Terms | Cross-Disciplinary Variants | Target Depth |
|---------|-------------|---------------------------|--------------|
| | | | |

**Question Type**: {{Clinical therapy / Methodological / Cross-disciplinary hybrid / Exploratory}}
**Negative-Framing Modifier**: {{Yes / No}}

---

## Planned Queries by Source

<!-- Planned query lists are written BEFORE execution begins for each source type. This enables resume after interruption by diffing planned vs. executed. -->

### Web Search

**Planned queries**:
1. {{query}}

**Executed**: {{list of completed queries with dates}}
**Remaining**: {{list of queries not yet executed}}

### Grey Literature

**Planned queries**:
1. {{query}}

**Executed**:
**Remaining**:

### PubMed

**Planned queries**:
1. {{query with field tags}}

**Executed**:
**Remaining**:

### Semantic Scholar

**Planned queries**:
1. {{query}}

**Executed**:
**Remaining**:

### Citation Chaining

**Planned seeds**:
1. {{seed citation with DOI/PMID}}

**Executed**: {{per-seed forward/backward results}}
**Remaining**:

### Seed-Based Recommendation

**Seeds used**: {{list of exemplar paper IDs}}
**PubMed Similar Articles**: {{executed / skipped / N/A}}
**Semantic Scholar Multi-Seed**: {{executed / skipped / N/A}}

---

## Search Execution Log

<!-- One entry per round. Documentation format defined in references/search-strategies.md (R-3). -->

### Round {{N}}: {{DATE}}

- **Source Type**: {{Web search / Grey literature / PubMed / Semantic Scholar / Citation chaining / Seed-based recommendation}}
- **Tool**: {{WebSearch / WebFetch / pubmed_search_articles / paper_relevance_search / etc.}}
- **Strategy Module**: {{search-web.md / search-grey-literature.md / search-pubmed.md / search-semantic-scholar.md / search-citation-chaining.md / search-recommendations.md}}
- **Queries Executed**:
  1. {{query}} -- {{N results}}
- **Results**: {{N total, N new unique, N duplicates}}
- **Key Findings**: {{brief summary of what was found}}
- **Rationale for Next Round**: {{why the next round targets what it does}}

---

## Inclusion and Exclusion Criteria

**Include**:
- {{criterion}}

**Exclude**:
- {{criterion}}

---

## Key Databases and Sources

| Source Type | Budget | Actual | Status | Notes |
|-------------|--------|--------|--------|-------|
| Web search | | | | |
| Grey literature | | | | |
| PubMed | | | | |
| Semantic Scholar | | | | |
| Citation chaining | | | | |
| Seed-based recommendation | | | | |

---

## Deduplication Summary

**Total duplicates removed**: {{N}}
- DOI match: {{N}}
- Title match: {{N}}
- Flagged for manual review (partial title match): {{N}}

**Merge protocol**: Field-level union; structured metadata (MCP/database) preferred over unstructured (web snippet). Source attributions merged into list.

---

## Convergence Log

<!-- Convergence calculation excludes pre-populated references from artifact intake. -->

| Round | New Papers (excluding pre-populated) | Overlap with Prior Round (%) | Cumulative New | Notes |
|-------|--------------------------------------|------------------------------|---------------|-------|
| | | | | |

**Pre-populated references excluded from convergence**: {{N}}

---

## File Organization

```
Literature/
  INDEX.md
  {{YYYY-MM-DD}}_{{topic-slug}}/
    REVIEW_PROGRESS.md
    Search_Methods.md (this file)
    Literature_Review.md
    Full_text_references/
```

---

## Version History

| Date | Change | Phase |
|------|--------|-------|
| {{DATE}} | Initial creation | Phase 2 |
