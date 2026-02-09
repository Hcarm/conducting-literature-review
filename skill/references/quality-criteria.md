# Quality Criteria Reference

Guidance on evaluating paper quality, determining exemplar status, the Phase 3 processing sequence, and the deduplication protocol.

---

## Relevance Assessment

| Level | Meaning | Action |
|-------|---------|--------|
| **High** | Directly addresses Core Concepts; strong methodological fit | Include; consider for exemplar |
| **Medium** | Related to research question; partial conceptual overlap | Include as supporting |
| **Low** | Tangentially related; provides context only | Include if under budget; exclude otherwise |
| **Exclude** | Not relevant to research question or Core Concepts | Exclude with reason noted |

---

## Exemplar Criteria

A paper qualifies as exemplar when it meets ALL of:

1. **Methodologically aligned**: Uses methods relevant to the user's research needs
2. **Well-executed**: Sound study design with appropriate controls and analysis
3. **Well-reported**: Clear methods section that another researcher could replicate
4. **Contextually relevant**: Applicable to the user's setting, population, or domain
5. **Current**: Not superseded by newer work using better methods (unless foundational)

### Exemplar Designations

| Designation | Meaning | Set When |
|-------------|---------|----------|
| Primary exemplar | Best available paper for this topic | Phase 3C processing |
| Secondary exemplar | Strong paper, complementary to primary | Phase 3C processing |
| Promoted | Discovered to be exemplar during Phase 3B supporting paper processing | Phase 3B (flagged for 3C reprocessing) |
| User-Designated | User identified this paper as exemplar during Phase 1 | Phase 1 artifact intake |

### Promotion Pathway

During Phase 3B supporting paper processing, if a paper meets exemplar criteria:

1. Flag the paper for Phase 3C processing: set Exemplar? = "Promoted" in REVIEW_PROGRESS.md
2. Level 2 annotation from 3B is retained (it is a subset of Level 3)
3. Phase 3C processes both pre-designated exemplars and promoted papers

---

## Study Quality Assessment

### Design Hierarchy (general guidance, not absolute)

1. Randomized controlled trials (parallel, crossover, cluster)
2. Quasi-experimental (regression discontinuity, interrupted time series, difference-in-differences)
3. Observational with causal inference methods (IV, propensity score, matching)
4. Observational without causal inference (cohort, cross-sectional)
5. Case studies, case reports, descriptive analyses

### Reporting Quality Indicators

- Clear research question stated
- Methods reproducible from description
- Effect sizes with confidence intervals (not just p-values)
- Limitations addressing threats to internal and external validity
- Appropriate comparison group or counterfactual
- Sensitivity analyses for key assumptions

### Field-Specific Standards

| Field | Additional Quality Signals |
|-------|---------------------------|
| Health economics | CHEERS checklist adherence; perspective stated; sensitivity analyses; discounting |
| Implementation science | RE-AIM or CFIR framework use; fidelity measurement; contextual factors |
| Clinical research | CONSORT/STROBE adherence; ITT analysis; adequate follow-up |

---

## Red Flags

### Methodological Concerns
- No comparison group when one is feasible
- Selective outcome reporting (methods mention outcomes not in results)
- Underpowered analyses presented as definitive
- Causal language without causal design

### Reporting Concerns
- Missing confidence intervals or standard errors
- P-values without effect sizes
- No limitations section
- Cherry-picked time periods or subgroups

### Context Concerns
- Setting too different to generalize
- Outdated methods superseded by better alternatives
- Conflicts of interest that may bias findings

---

## Quality Note Format

One-line assessment combining design strength and key limitation:

```
Design: [strength]; Limitation: [key limitation]
```

Examples:
- "Design: cluster RCT with adequate power; Limitation: single health system, 12-month follow-up"
- "Design: national registry cohort with IV identification; Limitation: no direct cost data"
- "Design: systematic review with meta-analysis; Limitation: high heterogeneity (I-squared 78%)"

---

## Phase 3 Processing Sequence

Phase 3 decomposes into five sub-steps with boundary conditions:

### Phase 3A: Triage and Deduplication

**Input**: Candidate papers from Phase 2 (REVIEW_PROGRESS.md Paper Tracking table)

**Actions**:
1. Apply deduplication protocol (see below)
2. Fetch metadata via MCP tools or WebFetch
3. Relevance screen on title/abstract against Core Concepts

**Output**: Deduplicated candidate list with metadata; non-relevant papers marked Excluded

**Boundary**: All candidates have metadata; duplicates removed; non-relevant excluded

**User-designated exemplars**: Go through dedup (to merge with search-discovered entries) but skip relevance screening (the user has already declared relevance)

### Phase 3B: Process Supporting Papers

**Input**: Non-exemplar candidates passing triage

**Actions**:
1. Level 2 annotation (1-2 sentence summary, quality note)
2. DOI verification
3. **Promotion detection**: If a paper meets exemplar criteria during processing, flag for Phase 3C (Exemplar? = "Promoted")

**Output**: Supporting entries in Literature_Review.md; promoted papers flagged

**Boundary**: All supporting papers have Level 2 annotations and verified DOIs

### Phase 3C: Process Exemplar Papers

**Input**: Pre-designated exemplars + promoted papers from 3B

**Actions**:
1. Content retrieval via fallback chain:
   - MCP metadata (structured abstract + fields) -- always available for indexed papers
   - User PDF in Full_text_references/ -- check for file
   - WebFetch full text -- for open-access papers
   - WebFetch abstract page -- for paywalled papers
   - Flag for user retrieval -- request user provide PDF
2. Level 3 annotation (all Paper_Entry.md fields)
3. Level 4 deep extraction via chunked reading (if full text available)

**Output**: Exemplar entries in Literature_Review.md with Level 3-4 fields

**Boundary**: All exemplar papers have Level 3+ annotations; full-text exemplars have Level 4

**Abstract-only handling**: When full text is unavailable, extract what is possible from the abstract (Level 3 + partial Level 4). Mark unavailable fields: "N/A -- full text required" or "Abstract only: [partial info]"

### Phase 3D: Build Evidence Table

**Input**: Processed exemplar papers

**Actions**: Compile evidence table per topic section from Level 4 fields

**Output**: Evidence tables in Literature_Review.md

**Boundary**: Each topic section has an evidence table

**Abstract-only notation**: Partially populated rows use "Abstract only" notation. Phase 5 synthesis documents: "N of M exemplars were assessed from abstracts only due to access restrictions."

### Phase 3E: Citation Verification

**Input**: All papers with DOIs

**Actions**: Run verify_citations.py batch, reconcile failures

**Output**: DOI verification status on all entries

**Boundary**: Every DOI-bearing paper has verification status recorded

**DOI-absent papers**: Skip verification; document "N/A (no DOI)" in verification status

### Batched Processing

When candidate count exceeds 50, Phase 3 operates in batches of ~25 papers:
- Each batch completes Phases 3A-3B before the next batch begins
- Exemplar candidates from all batches are collected and processed together in Phase 3C after all batches complete 3B
- Track per-batch completion in REVIEW_PROGRESS.md: "Phase 3 Batch 1 (papers 1-25): 3A complete, 3B complete. Batch 2 (papers 26-50): 3A complete, 3B in progress."

---

## Deduplication Protocol

Applied at two points:
1. After each source type completes in Phase 2 (incremental dedup)
2. At Phase 3A triage (comprehensive dedup before processing)

### Primary Match: DOI

- Normalize: lowercase, strip `https://doi.org/`, `http://doi.org/`, and `doi:` prefixes
- Exact match on normalized DOI = duplicate

### Fallback Match: Fuzzy Title (when one or both papers lack DOIs)

- Normalize: lowercase, remove all punctuation, collapse whitespace
- Exact match on normalized title = duplicate
- First 80 characters of normalized title match = flag for manual review (not auto-dedup)

### Resolution on Duplicate

- **Field-level union merge**: Retain the non-empty value for each field. If both entries have a non-empty value for the same field, prefer structured metadata (MCP/database) over unstructured (web snippet)
- **Merge source attributions**: A paper found via web AND database is attributed to both
- **Record in Search_Methods.md**: "Deduplicated: N duplicates removed (N DOI match, N title match)"

---

## User-Designated Exemplar Handling

### During Phase 3A Triage

User-designated exemplars bypass relevance screening (the user has declared relevance) but go through deduplication (to merge with search-discovered entries).

### During Phase 4 Antagonistic Review

Phase 4 can **flag but not unilaterally demote** user-designated exemplars:

1. Antagonist protocol produces a recommendation: "User-designated exemplar [Paper] has [limitation]. Recommend reclassification to supporting paper. Defer to user."
2. Present to user via AskUserQuestion: "The antagonistic review identified potential issues with your designated exemplar [Paper]: [issues]. Would you like to keep it as exemplar, reclassify as supporting, or remove it?"
3. User decision is final

See antagonist-protocol.md for the full demotion protocol.
