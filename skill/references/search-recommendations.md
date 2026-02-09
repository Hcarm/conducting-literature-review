# Seed-Based Recommendation Strategy

Strategy for discovering papers through semantic similarity recommendations using exemplar papers as seeds. Load this module when executing seed-based recommendation rounds (source type 6 -- the final source type).

---

## Rationale

Seed-based recommendation surfaces papers that are semantically similar to known exemplars but may use different terminology, preventing them from appearing in keyword search. Evidence suggests seed-based methods contribute ~17% of unique relevant literature not found by other methods (Wohlin 2014).

## Ordering

Seed-based recommendation runs **last** in Phase 2 (source type 6). This ordering is deliberate:

- Prevents recommendation results from biasing upstream keyword search construction (P-0004)
- Even when the user provides exemplars in Phase 1, recommendation waits until all keyword-based sources complete
- User-provided exemplars feed citation chaining (source 5) but recommendation (source 6) runs independently after

---

## PubMed Similar Articles Protocol

For each exemplar paper with a PMID:

1. Call `pubmed_article_connections` with:
   - `sourcePmid`: the exemplar's PMID
   - `relationshipType`: `"pubmed_similar_articles"`
   - `maxRelatedResults`: `20`
2. Deduplicate results against existing candidate list (quality-criteria.md dedup protocol)
3. Add new papers to REVIEW_PROGRESS.md Paper Tracking table

**Coverage**: PubMed Similar Articles covers the full PubMed corpus (~36M citations, all time). No pool restriction.

**Source attribution**: "PubMed Similar Articles from [Exemplar Citation]"

---

## Semantic Scholar Multi-Seed Protocol

Collect all exemplar paper IDs (S2 IDs, DOIs, or PMIDs) and call:

1. `get_paper_recommendations_multi` with:
   - `positive_paper_ids`: list of exemplar identifiers
   - `negative_paper_ids`: list of rejected paper identifiers (if user has rejected papers during review)
   - `limit`: `50`
2. Deduplicate results against existing candidate list
3. Add new papers to REVIEW_PROGRESS.md Paper Tracking table

**Pool limitation**: The "recent" pool (default) covers approximately the last 60 days for non-CS fields. The "all-cs" pool covers all computer science papers. There is no "all papers" pool for health sciences. PubMed Similar Articles provides historical coverage; Semantic Scholar Recommendations provides recency coverage.

**Source attribution**: "Semantic Scholar Recommendations (multi-seed from N exemplars)"

---

## Budget

Seed-based recommendation budget is absorbed into the overall search budget, not additive:

| Mode | Budget |
|------|--------|
| Narrow search | 1-3 papers |
| Full review | 5-10 papers |

---

## Convergence Signal

When recommendation results produce high overlap with existing candidates (>80% already found), this is a **positive convergence signal**, not a source failure. Record: "Seed-based recommendation: N results, M duplicates, K new unique papers. High overlap confirms search convergence."

---

## DOI-Absent Seeds

Papers without DOIs or PMIDs cannot be used as recommendation seeds:

- PubMed Similar Articles requires a PMID
- Semantic Scholar Recommendations requires a paper ID (S2 ID, DOI, or PMID)

For DOI-absent exemplars, attempt title-based lookup (see search-citation-chaining.md DOI-Absent Seeds section). If no identifier is found, exclude from recommendation with documentation.

---

## Degraded Operation

- **PubMed MCP unavailable**: Skip PubMed Similar Articles; proceed with Semantic Scholar Recommendations only
- **Semantic Scholar MCP unavailable**: Skip Semantic Scholar Recommendations; proceed with PubMed Similar Articles only
- **Both MCP servers unavailable**: Skip source type 6 entirely. No web-based fallback for recommendations. Document: "Seed-based recommendation skipped -- MCP servers unavailable."
