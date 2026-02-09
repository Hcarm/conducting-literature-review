# Citation Chaining Strategy

Strategy for discovering papers through forward citations (papers citing a seed) and backward references (papers cited by a seed). Load this module when executing citation chaining rounds (source type 5).

---

## Seed Selection

### Priority Order

Seeds are selected in this priority order:

1. **Exemplar papers from Phase 2 rounds 1-4** (highest priority)
2. **User-provided exemplars from Phase 1 artifact intake**
3. **High-relevance papers from early search rounds**

### Seed Caps

- **Narrow search**: Maximum 10 seeds
- **Full review**: Maximum 20 seeds

### Prioritization Among User-Provided References

When the user provides more references than the seed cap allows:

1. User-designated exemplars are highest priority seeds
2. Remaining references are ranked by recency (newer first) as default
3. Report to user: "You provided N references. I will use [cap] as citation chaining seeds, prioritizing your K exemplars and the [cap-K] most recent remaining references."

### Fallback When No Exemplars Emerge

If no papers are designated as exemplars after Phase 2 rounds 1-4:

- Use the top-ranked papers by relevance (highest relevance scores from triage, minimum 3 papers)
- If fewer than 3 papers have been found by rounds 1-4, citation chaining is **skipped** with documentation: "Insufficient seed papers for citation chaining. Search relied on keyword discovery only."

### DOI-Absent Seeds

Papers without DOIs cannot seed API-based citation chaining (both PubMed ELink and Semantic Scholar require identifiers).

- For DOI-absent papers designated as exemplars: attempt to find the paper in PubMed by title (`pubmed_search_articles`) or Semantic Scholar by title (`paper_title_search`) to obtain an identifier
- If no identifier can be found: document the limitation: "Exemplar [Paper] lacks a DOI/PMID; citation chaining could not use this paper as a seed."

---

## Traversal Protocol

For each seed:

### Step 1: Forward Citations (papers citing the seed)

Forward citations are more likely to yield recent relevant work building on the seed.

- **PubMed**: `pubmed_article_connections` with `relationshipType: "pubmed_citedin"`, `maxRelatedResults: 20`
- **Semantic Scholar**: `paper_citations` with seed's S2 ID, DOI, or PMID, `limit: 50`

### Step 2: Backward References (papers the seed cites)

Backward references yield foundational and methodological sources the seed builds on.

- **PubMed**: `pubmed_article_connections` with `relationshipType: "pubmed_references"`, `maxRelatedResults: 20`
- **Semantic Scholar**: `paper_references` with seed's S2 ID, DOI, or PMID, `limit: 50`

### Hop Depth

- **Default**: 1 hop (direct citations/references only)
- **2 hops**: Only for primary exemplars when first hop yields fewer than 3 new relevant papers. 2-hop means chaining from citations OF the seed's citations -- use sparingly.

### Per-Seed Budget Allocation

Distribute citation chaining budget equally across seeds:
- If 5 seeds and budget of 50, each seed gets ~10 candidate slots
- A seed that yields fewer candidates than its allocation does not transfer unused budget to other seeds

---

## Stopping Criteria

1. **Budget exhausted** (per search-strategies.md allocation for citation chaining)
2. **Convergence**: >80% of new results already in candidate list
3. **All seeds processed**

---

## Deduplication

Apply the deduplication protocol (defined in quality-criteria.md) after each seed's results:

1. DOI match (primary): normalize DOI, exact match
2. Fuzzy title match (fallback): normalize title, compare
3. Merge duplicates: field-level union, source attributions merged

---

## Incremental Persistence

After each seed is processed:

1. Write results to Search_Methods.md (Citation Chaining section, per-seed forward/backward results)
2. Update REVIEW_PROGRESS.md Citation Chaining Progress table
3. Update REVIEW_PROGRESS.md Paper Tracking table with new candidates

---

## Source Attribution

Format: "Forward citation from [Seed Citation]" or "Backward reference from [Seed Citation]"

---

## Web-Based Chaining Fallback

When both MCP servers are unavailable (see search-databases.md compound failure):

- Use WebSearch queries: `"papers citing [seed title]"`, `"[seed title] references"`
- Lower precision than API-based chaining
- Document as: "Web-based citation chaining (MCP servers unavailable)"
- This fallback provides partial functionality; it is not equivalent to API-based traversal
